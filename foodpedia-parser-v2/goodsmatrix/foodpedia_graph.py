from rdflib import RDF, Namespace, Literal, URIRef, XSD
from scrapy import log


class FoodpediaGraph:
    FOOD_NAMESPACE = Namespace("http://purl.org/foodontology#")
    FOODPEDIA_NAMESPACE = Namespace("http://foodpedia.tk/ontology#")
    GOODRELATIONS_NAMESPACE = Namespace("http://purl.org/goodrelations/v1#")
    FOODPEDIA_RESOURCE_NAMESPACE = Namespace("http://foodpedia.tk/resource/")
    DEFAULT_LANG = 'ru'

    def __init__(self, graph):
        self._graph = graph

    def __getattr__(self, attr_name):
        return getattr(self._graph, attr_name)

    def bind_default_namespaces(self):
        self._graph.bind('food', self.FOOD_NAMESPACE)
        self._graph.bind('foodpedia-owl', self.FOODPEDIA_NAMESPACE)
        self._graph.bind('gr', self.GOODRELATIONS_NAMESPACE)

    def get_namespaces(self):
        return self._graph.namespace_manager.namespaces()

    def add_good_item(self, item):
        item_barcode = item['barcode']
        self._init_good_item(item_barcode)

        if 'name' in item:
            self.add_name_to_good(item_barcode, item['name'])

        if 'name_en' in item:
            self.add_name_to_good(item_barcode, item['name_en'], lang='en')

        if 'best_before' in item:
            self.add_best_before_to_good(item_barcode, item['best_before'])

        if 'comment' in item:
            self.add_comment_to_good(item_barcode, item['comment'])

        if 'comment_en' in item:
            self.add_comment_to_good(item_barcode, item['comment_en'], lang='en')

        if 'ingredients' in item:
            self.add_ingridients_to_good(item_barcode, item['ingredients'])

        if 'netto_weight' in item:
            self.add_netto_weight_to_good(item_barcode, item['netto_weight'])

        if 'standart' in item:
            self.add_standart_to_good(item_barcode, item['standart'])

        if 'store_conditions' in item:
            self.add_store_conditions_to_good(item_barcode, item['store_conditions'])

        if 'esl_as_string' in item:
            self.add_esl_as_string_to_good(item_barcode, item['esl_as_string'])

        if 'pack_type' in item:
            self.add_pack_type_to_good(item_barcode, item['pack_type'])

        if 'proteins_as_double' in item:
            self.add_proteins_as_double_to_good(item_barcode, item['proteins_as_double'])

        if 'fats_as_double' in item:
            self.add_fats_as_double_to_good(item_barcode, item['fats_as_double'])

        if 'carbohydrates_as_double' in item:
            self.add_carbohydrates_as_double_to_good(item_barcode, item['carbohydrates_as_double'])

        if 'calories_as_double' in item:
            self.add_calories_as_double_to_good(item_barcode, item['calories_as_double'])

        if 'e_additives' in item:
            for eadditive_name in item['e_additives']:
                self.add_eadditive_to_good(item_barcode, eadditive_name)

        if 'agrovoc_ingredients' in item:
            for ingredient_uri in item['agrovoc_ingredients']:
                self.add_ingredient_uri(item_barcode, ingredient_uri)

    def _init_good_item(self, barcode):
        self._add_good_uri(barcode)
        self._add_good_barcode(barcode)

    def _add_good_uri(self, good_barcode):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self._graph.add((good_item_uri, RDF.type, self.FOOD_NAMESPACE.Food))

    def _add_good_barcode(self, good_barcode):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.GOODRELATIONS_NAMESPACE['hasEAN_UCC-13'], good_barcode, lang=None)

    def add_name_to_good(self, good_barcode, name, lang=DEFAULT_LANG):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.GOODRELATIONS_NAMESPACE.name, name, lang)

    def add_best_before_to_good(self, good_barcode, best_before, lang=DEFAULT_LANG):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.FOODPEDIA_NAMESPACE.best_before, best_before, lang)

    def add_comment_to_good(self, good_barcode, comment, lang=DEFAULT_LANG):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.GOODRELATIONS_NAMESPACE.description, comment, lang)

    def add_ingridients_to_good(self, good_barcode, ingridients_list_as_text, lang=DEFAULT_LANG):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.FOOD_NAMESPACE.ingredientsListAsText, ingridients_list_as_text, lang)

    def add_netto_weight_to_good(self, good_barcode, netto_weight, lang=DEFAULT_LANG):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.FOODPEDIA_NAMESPACE.netto_mass, netto_weight, lang)

    def add_standart_to_good(self, good_barcode, standart, lang=DEFAULT_LANG):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.FOODPEDIA_NAMESPACE.standart, standart, lang)

    def add_store_conditions_to_good(self, good_barcode, store_conditions, lang=DEFAULT_LANG):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.FOODPEDIA_NAMESPACE.store_cond, store_conditions, lang)

    def add_esl_as_string_to_good(self, good_barcode, esl_as_string, lang=DEFAULT_LANG):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.FOODPEDIA_NAMESPACE.esl, esl_as_string, lang)

    def add_pack_type_to_good(self, good_barcode, pack_type, lang=DEFAULT_LANG):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_string_object(good_item_uri, self.FOODPEDIA_NAMESPACE.pack_type, pack_type, lang)

    def add_string_object(self, subject_uri, predicate_uri, string_to_add, lang):
        literal = PatchedLiteralToReturnFullDatatype(string_to_add, lang=lang)
        self._graph.add(
            (subject_uri,
             predicate_uri,
             literal)
        )

    def add_calories_as_double_to_good(self, good_barcode, calories_as_double):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_double_object(good_item_uri, self.FOOD_NAMESPACE.energyPer100gAsDouble, calories_as_double)

    def add_fats_as_double_to_good(self, good_barcode, fats_as_double):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_double_object(good_item_uri, self.FOOD_NAMESPACE.fatPer100gAsDouble, fats_as_double)

    def add_proteins_as_double_to_good(self, good_barcode, proteins_as_double):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        self.add_double_object(good_item_uri, self.FOOD_NAMESPACE.proteinsPer100gAsDouble, proteins_as_double)

    def add_carbohydrates_as_double_to_good(self, barcode, carbohydrates_as_double):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(barcode)
        self.add_double_object(good_item_uri, self.FOOD_NAMESPACE.carbohydratesPer100gAsDouble, carbohydrates_as_double)

    def add_double_object(self, subject_uri, predicate_uri, double_value):
        literal = PatchedLiteralToReturnFullDatatype(double_value, datatype=XSD.double)
        self._graph.add(
            (subject_uri,
             predicate_uri,
             literal)
        )

    def add_eadditive_to_good(self, good_barcode, eadditive_name):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        eadditive_uri = FoodpediaGraph.convert_eadditive_name_to_uri(eadditive_name)
        self._graph.add(
            (good_item_uri,
             self.FOOD_NAMESPACE.containsIngredient,
             eadditive_uri)
        )

    @staticmethod
    def convert_barcode_to_uri(barcode):
        return FoodpediaGraph.FOODPEDIA_RESOURCE_NAMESPACE[str(barcode)]

    @staticmethod
    def convert_eadditive_name_to_uri(eadditive_name):
        return FoodpediaGraph.FOODPEDIA_RESOURCE_NAMESPACE[eadditive_name]

    def add_ingredient_uri(self, good_barcode, ingredient_uri):
        good_item_uri = FoodpediaGraph.convert_barcode_to_uri(good_barcode)
        #log.msg("adding '{0}' to the graph".format(URIRef(ingredient_uri)))
        self._graph.add(
            (good_item_uri,
             self.FOOD_NAMESPACE.containsIngredient,
             URIRef(ingredient_uri))
        )



class PatchedLiteralToReturnFullDatatype(Literal):
    """Patch the rdflib.Literal class to ignore the use_plain option for n3 representation.

    The rdflib.plugins.serializers.turtle.TurtleSerializer class
    invokes the _literal_n3 method with use_plain=True on serialization.
    We always want to return datatype together with the value.
    """
    def _literal_n3(self, use_plain=False, qname_callback=None):
        return super(PatchedLiteralToReturnFullDatatype, self)._literal_n3(
                use_plain=False, qname_callback=qname_callback)
