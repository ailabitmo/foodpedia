from rdflib import Graph, RDF, Namespace, Literal, URIRef


class FoodpediaGraph(Graph):
    FOOD_NAMESPACE = Namespace("http://purl.org/foodontology#")
    FOODPEDIA_NAMESPACE = Namespace("http://foodpedia.tk/ontology#")
    GOODRELATIONS_NAMESPACE = Namespace("http://purl.org/goodrelations/v1#")
    BASE_RESOURCE_URI = "http://foodpedia.tk/page/resource/{0}"

    def __init__(self, graph):
        self._graph = graph
        self._graph.bind('food', self.FOOD_NAMESPACE)
        self._graph.bind('foodpedia-owl', self.FOODPEDIA_NAMESPACE)
        self._graph.bind('gr', self.GOODRELATIONS_NAMESPACE)
        self.current_item = None

    def __getattr__(self, name):
        return getattr(self._graph, name)

    def get_namespaces(self):
        return self._graph.namespace_manager.namespaces()

    def add_good_item(self, item):
        self.current_item = item
        self._add_current_item_to_graph()

    def _add_current_item_to_graph(self):
        self._add_current_items_uri_as_predicate()
        self._add_current_items_property_as_predicate('name', self.GOODRELATIONS_NAMESPACE.name)
        self._add_current_items_property_as_predicate('barcode', self.GOODRELATIONS_NAMESPACE['hasEAN_UCC-13'])
        self._add_current_items_property_as_predicate('best_before', self.FOODPEDIA_NAMESPACE.best_before)
        self._add_current_items_property_as_predicate('comment', self.GOODRELATIONS_NAMESPACE.description)
        self._add_current_items_property_as_predicate('ingredients', self.FOOD_NAMESPACE.ingredientsListAsText)
        self._add_current_items_property_as_predicate('netto_weight', self.FOODPEDIA_NAMESPACE.netto_mass)
        self._add_current_items_property_as_predicate('standart', self.FOODPEDIA_NAMESPACE.standart)
        self._add_current_items_property_as_predicate('store_conditions', self.FOODPEDIA_NAMESPACE.store_cond)
        self._add_current_items_property_as_predicate('esl', self.FOODPEDIA_NAMESPACE.esl)
        self._add_current_items_property_as_predicate('proteins_as_double', self.FOOD_NAMESPACE.proteinsPer100gAsDouble)
        self._add_current_items_property_as_predicate('fats_as_double', self.FOOD_NAMESPACE.fatPer100gAsDouble)
        self._add_current_items_property_as_predicate('carbohydrates_as_double', self.FOOD_NAMESPACE.carbohydratesPer100gAsDouble)
        self._add_current_items_property_as_predicate('calories_as_double', self.FOOD_NAMESPACE.energyPer100gAsDouble)
        self._add_current_items_property_as_predicate('pack_type', self.FOODPEDIA_NAMESPACE.pack_type)

    def _add_current_items_uri_as_predicate(self):
        self._graph.add((self._get_current_items_resource_uri(), RDF.type, self.FOOD_NAMESPACE.Food))

    def _get_current_items_resource_uri(self):
        return URIRef(self.BASE_RESOURCE_URI.format(self.current_item['barcode']))

    def _add_current_items_property_as_predicate(self, property_name, predicate):
        if property_name in self.current_item:
            self._graph.add(
                (
                    self._get_current_items_resource_uri(),
                    predicate,
                    self._items_property_to_literal(property_name)
                )
            )

    def _items_property_to_literal(self, property_name):
        property_value = self.current_item[property_name]
        if isinstance(property_name, basestring):
            return Literal(property_value, lang='ru')
        else:
            return Literal(property_value)
