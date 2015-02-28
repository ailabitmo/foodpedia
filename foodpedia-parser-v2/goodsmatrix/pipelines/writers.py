import json
import codecs

import os
from tempfile import mktemp

from rdflib import ConjunctiveGraph
from rdflib.store import NO_STORE, VALID_STORE
from scrapy.utils.project import get_project_settings
from scrapy import log

from goodsmatrix.foodpedia_graph import FoodpediaGraph


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class InMemoryRDFPipeline(object):
    def __init__(self):
        self.graph = FoodpediaGraph(ConjunctiveGraph(store="IOMemory"))
        self.graph.bind_default_namespaces()

    def process_item(self, item, spider):
        self.graph.add_good_item(item)

    def close_spider(self, spider):
        output_filename = spider.settings.get("OUTPUT_FILENAME")
        output_filename = output_filename if output_filename else "data.ttl"

        with open(output_filename, 'w') as output_file:
            log.msg("serialize the graph to {0}".format(output_filename))
            self.graph.serialize(output_file, format='turtle')
        self.graph.close()

class PersistentRDFPipeline(object):
    def __init__(self):
        self.tempdir = mktemp()
        self.graph = FoodpediaGraph(ConjunctiveGraph(store="Sleepycat"))

        rt = self.graph.open(self.tempdir, create=False)
        if rt == NO_STORE:
            # There is no underlying Sleepycat infrastructure, create it
            self.graph.open(self.tempdir, create=True)
            self.graph.bind_default_namespaces()
        else:
            assert rt == VALID_STORE, "The underlying store is corrupt"
        log.msg("Temporal directory for persistent storage of parsed items: {0}".format(self.tempdir), level=log.INFO)
        log.msg("Triples in graph before add: {0}".format(len(self.graph)), level=log.INFO)

    def process_item(self, item, spider):
        self.graph.add_good_item(item)
        self.graph.commit()

    def close_spider(self, spider):
        output_filename = spider.settings.get("OUTPUT_FILENAME")
        output_filename = output_filename if output_filename else "data.ttl"

        log.msg("Triples in graph after add: {0}".format(len(self.graph)), level=log.INFO)
        with open(output_filename, 'w') as output_file:
            log.msg("serialize the graph to {0}".format(output_filename))
            self.graph.serialize(output_file, format='turtle')
        self.graph.close()

        log.msg("Clean up the temp directory '{0}' to remove the Sleepycat database files".format(self.tempdir),
                level=log.INFO)
        for f in os.listdir(self.tempdir):
            os.unlink(os.path.join(self.tempdir, f))
        os.rmdir(self.tempdir)
