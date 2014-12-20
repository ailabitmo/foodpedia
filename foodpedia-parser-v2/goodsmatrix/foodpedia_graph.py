from rdflib import Graph, RDF, Namespace, Literal, URIRef, XSD


class FoodpediaGraph(Graph):
    FOOD_NAMESPACE = Namespace("http://purl.org/foodontology#")
    FOODPEDIA_NAMESPACE = Namespace("http://foodpedia.tk/ontology#")
    GOODRELATIONS_NAMESPACE = Namespace("http://purl.org/goodrelations/v1#")
    BASE_RESOURCE_URI = "http://foodpedia.tk/resource/{0}"
    BASE_EADDITIVE_URI = str(FOOD_NAMESPACE) + "{0}"
    DEFAULT_LANG = 'ru'

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
        self._add_current_items_property_as_string_predicate('name', self.GOODRELATIONS_NAMESPACE.name)
        self._add_current_items_property_as_string_predicate('barcode',
                                                             self.GOODRELATIONS_NAMESPACE['hasEAN_UCC-13'],
                                                             lang=None)
        self._add_current_items_property_as_string_predicate('best_before', self.FOODPEDIA_NAMESPACE.best_before)
        self._add_current_items_property_as_string_predicate('comment', self.GOODRELATIONS_NAMESPACE.description)
        self._add_current_items_property_as_string_predicate('ingredients', self.FOOD_NAMESPACE.ingredientsListAsText)
        self._add_current_items_property_as_string_predicate('netto_weight', self.FOODPEDIA_NAMESPACE.netto_mass)
        self._add_current_items_property_as_string_predicate('standart', self.FOODPEDIA_NAMESPACE.standart)
        self._add_current_items_property_as_string_predicate('store_conditions', self.FOODPEDIA_NAMESPACE.store_cond)
        self._add_current_items_property_as_string_predicate('esl', self.FOODPEDIA_NAMESPACE.esl)
        self._add_current_items_property_as_double_predicate('proteins_as_double',
                                                             self.FOOD_NAMESPACE.proteinsPer100gAsDouble)
        self._add_current_items_property_as_double_predicate('fats_as_double',
                                                             self.FOOD_NAMESPACE.fatPer100gAsDouble)
        self._add_current_items_property_as_double_predicate('carbohydrates_as_double',
                                                             self.FOOD_NAMESPACE.carbohydratesPer100gAsDouble)
        self._add_current_items_property_as_double_predicate('calories_as_double',
                                                             self.FOOD_NAMESPACE.energyPer100gAsDouble)
        self._add_current_items_property_as_string_predicate('pack_type', self.FOODPEDIA_NAMESPACE.pack_type)

        self._add_current_items_e_additives()

    def _add_current_items_uri_as_predicate(self):
        self._graph.add((self._get_current_items_resource_uri(), RDF.type, self.FOOD_NAMESPACE.Food))

    def _add_current_items_property_as_string_predicate(self, property_name, predicate, lang=DEFAULT_LANG):
        self._add_current_items_property_as_predicate(property_name, predicate, datatype=XSD.string, lang=lang)

    def _add_current_items_property_as_double_predicate(self, property_name, predicate):
        self._add_current_items_property_as_predicate(property_name, predicate, datatype=XSD.double, lang=None)

    def _add_current_items_property_as_predicate(self,
                                                 property_name,
                                                 predicate,
                                                 datatype,
                                                 lang):
        if property_name in self.current_item:
            literal = self._current_items_property_to_literal(property_name, datatype, lang)
            self._graph.add(
                (self._get_current_items_resource_uri(),
                 predicate,
                 literal)
            )

    def _current_items_property_to_literal(self, property_name, literal_datatype, lang):
        property_value = self.current_item[property_name]
        if literal_datatype == XSD.string:
            if lang:
                return PatchedLiteralToReturnFullDatatype(property_value, lang=lang)
            else:
                return PatchedLiteralToReturnFullDatatype(property_value)
        else:
            return PatchedLiteralToReturnFullDatatype(property_value, datatype=literal_datatype)

    def _add_current_items_e_additives(self):
        if 'e_additives' in self.current_item:
            for eadditive in self.current_item['e_additives']:
                self.add_eadditive_as_current_item_predicate(eadditive)

    def add_eadditive_as_current_item_predicate(self, eadditive):
        obj = self._get_current_items_resource_uri()
        predicate = self.FOOD_NAMESPACE.containsIngredient
        subj = URIRef(self.BASE_RESOURCE_URI.format(eadditive))
        self._graph.add(
            (obj, predicate, subj)
        )

    def _get_current_items_resource_uri(self):
        return URIRef(self.BASE_RESOURCE_URI.format(self.current_item['barcode']))


class PatchedLiteralToReturnFullDatatype(Literal):
    """Patch the rdflib.Literal class to ignore the use_plain option for n3 representation.

    The rdflib.plugins.serializers.turtle.TurtleSerializer class
    invokes the _literal_n3 method with use_plain=True on serialization.
    We always want to return datatype together with the value.
    """
    def _literal_n3(self, use_plain=False, qname_callback=None):
        return super(PatchedLiteralToReturnFullDatatype, self)._literal_n3(
                use_plain=False, qname_callback=qname_callback)
