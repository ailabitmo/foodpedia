# -*- coding: utf-8 -*-
import logging
import os
import re
import shutil
from tempfile import mkdtemp
import urllib
import zipfile

from rdflib import Graph, ConjunctiveGraph
from rdflib.namespace import SKOS, Namespace
from scrapy import log
#from rdflib.store import NO_STORE, VALID_STORE
from SPARQLWrapper import SPARQLWrapper, JSON, XML

from goodsmatrix.string_processor import replace_in_file
from goodsmatrix.string_processor import escape_special_chars_in_sparq_query_unicode


LAST_VERSION_NAME = r"agrovoc_2014-07-23_lod"
ZIP_FILENAME = "{0}.zip".format(LAST_VERSION_NAME)
AGROVOC_GRAPH_URL = r"https://bitbucket.org/aims-fao/agrovoc/downloads/{0}".format(ZIP_FILENAME)
EXACT_MATCH_CASE_INSENSITIVE_QUERY_STRING = u"""
PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>

SELECT ?x
WHERE 
{{
  ?x skosxl:prefLabel ?prefLabel.
  ?prefLabel skosxl:literalForm ?literalPrefLabel.
  OPTIONAL
    {{
        ?x skosxl:altLabel ?altLabel.
        ?altLabel skosxl:literalForm ?literalAltLabel.
    }}
    FILTER (regex(?literalPrefLabel, '^{0}$', 'i') || regex(?literalAltLabel, '^{0}$', 'i') )
}}
LIMIT 1
"""

CONTAINS_CASE_INSENSITIVE_QUERY_STRING = u"""
PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>

SELECT ?x
WHERE 
{{
  ?x skosxl:prefLabel ?prefLabel.
  ?prefLabel skosxl:literalForm ?literalPrefLabel.
  OPTIONAL
    {{
        ?x skosxl:altLabel ?altLabel.
        ?altLabel skosxl:literalForm ?literalAltLabel.
    }}
    FILTER (regex(?literalPrefLabel, '{0}', 'i') || regex(?literalAltLabel, '{0}', 'i') )
}}
LIMIT 1
"""
AGROVOC_ENDPOINT = "http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc"


def agrovoc_graph_factory(local=True, nt_dump_file_path=None, endpoint_url=AGROVOC_ENDPOINT):
    if local:
        return LocalAGROVOCGraph(nt_dump_file_path)
    else:
        return RemoteAGROVOCGraph(endpoint_url)


class AbstractAGROVOCGraph(object):
    def find_ingredient_by_name(self, ingredient_name):
        #log.msg(u"search '{0}'".format(ingredient_name))
        ingredient_name = ingredient_name.replace('\\', '\\\\')
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

    def clean_up(self):
        pass


class LocalAGROVOCGraph(AbstractAGROVOCGraph):
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
        log.msg('query: {0}'.format(query_string))
        results = self.rdf_graph.query(query_string, initNs={"skos": SKOS})
        log.msg('results: {0}'.format(results))
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


class RemoteAGROVOCGraph(AbstractAGROVOCGraph):
    def __init__(self, endpoint_url=AGROVOC_ENDPOINT):
        self.sparql = SPARQLWrapper(endpoint_url)

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


class ConstructedAGROVOCGraph(AbstractAGROVOCGraph):
    CONSTRUCT_QUERY_STRING = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>

        CONSTRUCT
        {
          ?x  a  skos:Concept .
          ?x skosxl:prefLabel ?prefLabel.
          ?x skosxl:altLabel ?altLabel.
          ?prefLabel skosxl:literalForm ?literalPrefLabel.
          ?altLabel skosxl:literalForm ?literalAltLabel.
        }
        WHERE {
          ?x  a  skos:Concept .
          {
            ?x skos:broader* <http://aims.fao.org/aos/agrovoc/c_6211>
          }
          UNION
          {
            ?x skos:broader* <http://aims.fao.org/aos/agrovoc/c_330705>
          }.
          ?x skosxl:prefLabel ?prefLabel.
          ?prefLabel skosxl:literalForm ?literalPrefLabel.
          OPTIONAL
          {
            ?x skosxl:altLabel ?altLabel.
            ?altLabel skosxl:literalForm ?literalAltLabel.
            FILTER((langMatches(lang(?literalPrefLabel), "EN") && langMatches(lang(?literalAltLabel), "EN")) ||
              (langMatches(lang(?literalPrefLabel), "RU") && langMatches(lang(?literalAltLabel), "RU"))).
          }
          FILTER(langMatches(lang(?literalPrefLabel), "EN") || langMatches(lang(?literalPrefLabel), "RU")).
        }
    """
    def __init__(self):
        self.remote_endpoint = SPARQLWrapper(AGROVOC_ENDPOINT)
        self.local_rdf_graph = self._constract_local_graph()

    def _constract_local_graph(self):
        log.msg('constructing local in-memory graph')
        self.remote_endpoint.setReturnFormat(XML)
        self.remote_endpoint.setQuery(ConstructedAGROVOCGraph.CONSTRUCT_QUERY_STRING)
        response = self.remote_endpoint.query().response
        g = Graph()
        g.parse(response)
        log.msg('constructed')
        return g

    def find_ingredient_by_exact_match(self, ingredient_name):
        return self._find_ingredient_by_sparql_query(
            EXACT_MATCH_CASE_INSENSITIVE_QUERY_STRING.format(ingredient_name))

    def find_first_ingredients_which_contains_name(self, ingredient_name):
        return self._find_ingredient_by_sparql_query(
            CONTAINS_CASE_INSENSITIVE_QUERY_STRING.format(ingredient_name))

    def _find_ingredient_by_sparql_query(self, query_string):
        log.msg('query: {0}'.format(query_string))
        results = self.local_rdf_graph.query(query_string, initNs={
            "skos" : SKOS,
            "skosxl": Namespace(r"http://www.w3.org/2008/05/skos-xl#")})
        log.msg('results: {0}'.format(results))
        log.msg('results: {0}'.format(str(results)))
        for rr in results:
            log.msg(rr)
        log.msg(dir(results))
        log.msg(results.bindings)
        #log.msg(results.bindings)
        #log.msg(list(results.bindings))
        if results:
            return results.bindings[0]['x']
        else:
            return None

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    print('starting')
    #agrovoc_graph = RemoteAGROVOCGraph("http://192.168.126.137:3030/agrovoc/query")
    agrovoc_graph = RemoteAGROVOCGraph("http://192.168.126.139:3030/agrovoc/query")
    try:
        #for row in agrovoc_graph.local_rdf_graph:
            #log.msg(row)
        print('initialized. search sugar')
            #nt_dump_file_path=r'/tmp/tmpGvStE3/agrovoc_2014-07-23_lod.nt')
        found = agrovoc_graph.find_ingredient_by_name(ur'мука пшеничная в\с')
        print(found)
    finally:
        agrovoc_graph.clean_up()
