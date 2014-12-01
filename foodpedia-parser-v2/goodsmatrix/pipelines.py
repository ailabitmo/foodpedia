import json
import codecs

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF
from rdflib import Namespace


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
    FOOD = Namespace("http://purl.org/foodontology#")
    FOOD_NOT_IMPLEMENTED = Namespace("http://purl.org/foodontology/extention#")
    GOODRELATIONS = Namespace("http://purl.org/goodrelations/v1#")
    def __init__(self):
        self.graph = Graph(store='default')
        self.graph.bind('food', self.FOOD)
        self.graph.bind('food_not_implemented', self.FOOD_NOT_IMPLEMENTED)
        self.graph.bind('gr', self.GOODRELATIONS)
        self.current_item = None

    def process_item(self, item, spider):
        self.current_item = item
        self._add_current_item_to_graph()

    def _add_current_item_to_graph(self):
        self.graph.add((self._get_current_items_resource_url(), RDF.type, self.FOOD.Food))
        self._add_current_items_property_as_predicate(self.GOODRELATIONS.name, 'name')
        self._add_current_items_property_as_predicate(self.GOODRELATIONS['hasEAN_UCC-13'], 'barcode')
        self._add_current_items_property_as_predicate(self.FOOD_NOT_IMPLEMENTED.best_before, 'best_before')
        self._add_current_items_property_as_predicate(self.GOODRELATIONS.description, 'comment')
        self._add_current_items_property_as_predicate(self.FOOD.ingredientsListAsText, 'ingredients')
        self._add_current_items_property_as_predicate(self.FOOD_NOT_IMPLEMENTED.netto_mass, 'netto_weight')
        self._add_current_items_property_as_predicate(self.FOOD_NOT_IMPLEMENTED.standart, 'standart')
        self._add_current_items_property_as_predicate(self.FOOD_NOT_IMPLEMENTED.store_cond, 'store_conditions')
        self._add_current_items_property_as_predicate(self.FOOD_NOT_IMPLEMENTED.esl, 'esl')
        self._add_current_items_property_as_predicate(self.FOOD_NOT_IMPLEMENTED.pack_type, 'pack_type')

    def _get_current_items_resource_url(self):
        return URIRef(self.current_item['url'])

    def _add_current_items_property_as_predicate(self, predicate, property_name):
        if self.current_item[property_name]:
            self.graph.add(
                (
                    self._get_current_items_resource_url(),
                    predicate,
                    self._items_property_to_literal(property_name)
                )
            )

    def _items_property_to_literal(self, property_name):
        return Literal(self.current_item[property_name], lang='ru')

    def close_spider(self, spider):
        with open('dump.ttl', 'w') as output_file:
            self.graph.serialize(output_file, format='turtle')
            self.graph.close()
