# -*- coding: utf-8 -*-
import logging
import os
import re
import shutil
from tempfile import mkdtemp
import urllib
import zipfile

from rdflib import ConjunctiveGraph
from rdflib.namespace import SKOS
from scrapy import log
#from rdflib.store import NO_STORE, VALID_STORE
from SPARQLWrapper import SPARQLWrapper, JSON

from goodsmatrix.string_processor import replace_in_file
from goodsmatrix.string_processor import escape_special_chars_in_sparq_query_unicode


LAST_VERSION_NAME = r"agrovoc_2014-07-23_lod"
ZIP_FILENAME = "{0}.zip".format(LAST_VERSION_NAME)
AGROVOC_GRAPH_URL = r"https://bitbucket.org/aims-fao/agrovoc/downloads/{0}".format(ZIP_FILENAME)
EXACT_MATCH_CASE_INSENSITIVE_QUERY_STRING = u"""
SELECT ?x
WHERE 
{{
  ?x  a  skos:Concept .
  ?x skos:prefLabel ?prefLabel.
  ?x skos:altLabel ?altLabel.
  FILTER (regex(?prefLabel, '^{0}$', 'i') || regex(?altLabel, '^{0}$', 'i')).
}}
limit 1
"""

CONTAINS_CASE_INSENSITIVE_QUERY_STRING = u"""
SELECT ?x
WHERE 
{{
  ?x  a  skos:Concept .
  ?x skos:altLabel ?altLabel.
  FILTER (regex(?prefLabel, '{0}', 'i') || regex(?altLabel, '{0}', 'i')).
}}
limit 1
"""
AGROVOC_ENDPOINT = "http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc"


def agrovoc_graph_factory(local=True, nt_dump_file_path=None):
    if local:
        return LocalAGROVOCGraph(nt_dump_file_path)
    else:
        return RemoteAGROVOCGraph()


class AGROVOCGraph(object):
    def find_ingredient_by_name(self, ingredient_name):
        log.msg(u"search '{0}'".format(ingredient_name))
        exact_matched_ingredient = self.find_ingredient_by_exact_match(
            escape_special_chars_in_sparq_query_unicode(ingredient_name))
        # link only exact matches.
        # do not use fallback search with the 'contains' statement
        # because 'соль' could be linked to 'фасоль' or 'сольволиз'
        """
        if exact_matched_ingredient:
            return exact_matched_ingredient
        else:
            first_ingredient_contains_name = self.find_first_ingredients_which_contains_name(
                ingredient_name)
            return first_ingredient_contains_name
        """
        return exact_matched_ingredient

    def find_ingredient_by_exact_match(self, ingredient_name):
        pass

    def find_first_ingredients_which_contains_name(self, ingredient_name):
        pass

class LocalAGROVOCGraph(AGROVOCGraph):
    def __init__(self, nt_dump_file_path=None):
        self.tempdir = mkdtemp()
        self.zip_file_path = os.path.join(self.tempdir, ZIP_FILENAME)
        if nt_dump_file_path:
            self.nt_dump_file_path = nt_dump_file_path
            self.tempdir = os.path.dirname(self.nt_dump_file_path)
        else:
            nt_filename = "{0}.nt".format(LAST_VERSION_NAME)
            self.nt_dump_file_path = os.path.join(self.tempdir, nt_filename)
            self._download_dump()
        self._fix_strings_in_dump()
        self.rdf_graph = self._create_graph()
        self._parse_dump()
        log.msg("number of tripples:{0}".format(len(self.rdf_graph)))

    def _download_dump(self):
        self._download_dump_zip()
        self._unzip_dump()

    def _download_dump_zip(self):
        log.msg("download '{0}' to '{1}'".format(AGROVOC_GRAPH_URL, self.zip_file_path))
        urllib.urlretrieve(AGROVOC_GRAPH_URL, self.zip_file_path)

    def _unzip_dump(self):
        log.msg("unzip '{0}' to '{1}'".format(self.zip_file_path, self.tempdir))
        with zipfile.ZipFile(self.zip_file_path, "r") as z:
            z.extractall(self.tempdir)

    def _fix_strings_in_dump(self):
        """the dump contains typos which leads to fail on parsing"""
        log.msg("fixing '{0}'; drop space character in 'exactMatch >'".format(
            self.nt_dump_file_path))
        replace_in_file(self.nt_dump_file_path, r"exactMatch >", r"exactMatch>")

    def _create_graph(self):
        """the dump is huge and in-memory parsing consumes too much RAM
        use Sleepcat storage to store graph during parsing
        """
        sleepycat_path = os.path.join(self.tempdir, "sleepycat")
        log.msg("create graph with sleepycat store '{0}'".format(sleepycat_path))
        if not os.path.exists(sleepycat_path):
            log.msg("create '{0}'".format(sleepycat_path))
            os.makedirs(sleepycat_path)
        graph = ConjunctiveGraph(store="Sleepycat")
        graph.open(sleepycat_path, create=True)
        """
        rt = graph.open(sleepycat_path, create=False)
        if rt == NO_STORE:
            graph.open(sleepycat_path, create=True)
        else:
            assert rt == VALID_STORE, "The underlying store is corrupt"
        """
        return graph

    def _parse_dump(self):
        log.msg("parsing graph '{0}'".format(self.nt_dump_file_path))
        self.rdf_graph.parse(self.nt_dump_file_path, format="nt")

    def find_ingredient_by_exact_match(self, ingredient_name):
        return self._find_ingredient_by_sparql_query(
            EXACT_MATCH_CASE_INSENSITIVE_QUERY_STRING.format(ingredient_name))

    def find_first_ingredients_which_contains_name(self, ingredient_name):
        return self._find_ingredient_by_sparql_query(
            CONTAINS_CASE_INSENSITIVE_QUERY_STRING.format(ingredient_name))

    def _find_ingredient_by_sparql_query(self, query_string):
        results = self.rdf_graph.query(query_string, initNs={"skos": SKOS})
        if results:
            return results.bindings[0]['x']
        else:
            return None

    def clean_up(self):
        """drop leftovers --- they may take ~2GB"""
        self.rdf_graph.close()
        self._remove_directory_silently(self.tempdir)

    def _remove_directory_silently(self, dir_path):
        if os.path.exists(dir_path):
            log.msg("removing the directory '{0}' recursively".format(dir_path))
            shutil.rmtree(dir_path)


class RemoteAGROVOCGraph(AGROVOCGraph):
    def __init__(self):
        self.sparql = SPARQLWrapper(AGROVOC_ENDPOINT)

    def find_ingredient_by_exact_match(self, ingredient_name):
        return self._find_ingredient_by_sparql_query(
            EXACT_MATCH_CASE_INSENSITIVE_QUERY_STRING.format(ingredient_name))

    def find_first_ingredients_which_contains_name(self, ingredient_name):
        return self._find_ingredient_by_sparql_query(
            CONTAINS_CASE_INSENSITIVE_QUERY_STRING.format(ingredient_name))

    def _find_ingredient_by_sparql_query(self, query_string):
        results = self._execute_query(query_string)
        if results:
            return results[0]['x']['value']
        else:
            return None

    def _execute_query(self, query_string):
        self.sparql.setQuery(query_string)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        return results["results"]["bindings"]

    def clean_up(self):
        pass


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    try:
        agrovoc_graph = agrovoc_graph_factory(local=False)
            #nt_dump_file_path=r'/tmp/tmpGvStE3/agrovoc_2014-07-23_lod.nt')
        found = agrovoc_graph.find_ingredient_by_name(u'со(ль')
        log.msg(found)
    finally:
        agrovoc_graph.clean_up()
