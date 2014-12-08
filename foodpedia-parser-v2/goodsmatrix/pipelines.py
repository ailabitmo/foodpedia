import json
import codecs

from rdflib import Graph
from scrapy.utils.project import get_project_settings

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


class RDFPipeline(object):
    def __init__(self):
        self.graph = FoodpediaGraph(Graph(store='default'))

    def process_item(self, item, spider):
        self.graph.add_good_item(item)

    def close_spider(self, spider):
        output_filename = spider.settings.get("OUTPUT_FILENAME")
        output_filename = output_filename if output_filename else "data.ttl"
        with open(output_filename, 'w') as output_file:
            self.graph.serialize(output_file, format='turtle')
            self.graph.close()
