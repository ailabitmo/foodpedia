# -*- coding: utf-8 -*-
from unittest import TestCase

from rdflib import Namespace, Graph, URIRef, Literal, XSD
from rdflib.namespace import RDF

from goodsmatrix.foodpedia_graph import FoodpediaGraph
from goodsmatrix.good_item import GoodItem


class TestFoodpediaGraph(TestCase):
    def setUp(self):
        self.foodpedia_graph = FoodpediaGraph(Graph())

    def test_bind_default_namespaces(self):
        self.foodpedia_graph.bind_default_namespaces()

        self.assertIn(("food", Namespace("http://purl.org/foodontology#")), self.foodpedia_graph.get_namespaces())
        self.assertIn(("foodpedia-owl", Namespace("http://foodpedia.tk/ontology#")), self.foodpedia_graph.get_namespaces())
        self.assertIn(("gr", Namespace("http://purl.org/goodrelations/v1#")), self.foodpedia_graph.get_namespaces())

    def test_add_good_item_added_uri(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="1111"))

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"), RDF.type, URIRef("http://purl.org/foodontology#Food")
        )

    def test_add_good_item_added_barcode(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="1111"))

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/goodrelations/v1#hasEAN_UCC-13"),
            Literal("1111")
        )

    def test_add_name_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="1111"))

        self.foodpedia_graph.add_name_to_good("1111", "test")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/goodrelations/v1#name"),
            Literal("test", lang="ru")
        )

    def test_add_name_to_not_existing_good(self):
        self.foodpedia_graph.add_name_to_good("2222", "test")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/2222"),
            URIRef("http://purl.org/goodrelations/v1#name"),
            Literal("test", lang="ru")
        )

    def test_add_name_to_good_with_existing_name(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="1111", name="existing_name"))

        self.foodpedia_graph.add_name_to_good("1111", "second_name")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/goodrelations/v1#name"),
            Literal("existing_name", lang="ru")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/goodrelations/v1#name"),
            Literal("second_name", lang="ru")
        )

    def test_add_english_name_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="1111"))

        self.foodpedia_graph.add_name_to_good("1111", "test", "en")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/goodrelations/v1#name"),
            Literal("test", lang="en")
        )

    def test_add_best_before_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="333"))

        self.foodpedia_graph.add_best_before_to_good("333", "6 мес.")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/333"),
            URIRef("http://foodpedia.tk/ontology#best_before"),
            Literal("6 мес.", lang="ru")
        )

    def test_add_comment_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="333"))

        self.foodpedia_graph.add_comment_to_good("333", "кусочки мяса птицы на костях от разных частей тушки")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/333"),
            URIRef("http://purl.org/goodrelations/v1#description"),
            Literal("кусочки мяса птицы на костях от разных частей тушки", lang="ru")
        )

    def test_add_ingridienta_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="333"))

        self.foodpedia_graph.add_ingridients_to_good("333", "мясо птицы")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/333"),
            URIRef("http://purl.org/foodontology#ingredientsListAsText"),
            Literal("мясо птицы", lang="ru")
        )

    def test_add_netto_weight_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="4444"))

        self.foodpedia_graph.add_netto_weight_to_good("4444", "1,00 кг")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/4444"),
            URIRef("http://foodpedia.tk/ontology#netto_mass"),
            Literal("1,00 кг", lang="ru")
        )

    def test_add_standart_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="4444"))

        self.foodpedia_graph.add_standart_to_good("4444", "14192-96, ТУ 9214-212-2347684-10")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/4444"),
            URIRef("http://foodpedia.tk/ontology#standart"),
            Literal("14192-96, ТУ 9214-212-2347684-10", lang="ru")
        )

    def test_add_store_conditions_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="5678"))

        self.foodpedia_graph.add_store_conditions_to_good("5678", "Условия хранения от -18 градусов С")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/5678"),
            URIRef("http://foodpedia.tk/ontology#store_cond"),
            Literal("Условия хранения от -18 градусов С", lang="ru")
        )

    def test_add_esl_as_string_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="9"))

        self.foodpedia_graph.add_esl_as_string_to_good("9", "Белки: не менее 19,00 г Жиры: не более 11,50 г Энергетическая ценность:  179,50 ккал")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/9"),
            URIRef("http://foodpedia.tk/ontology#esl"),
            Literal("Белки: не менее 19,00 г Жиры: не более 11,50 г Энергетическая ценность:  179,50 ккал", lang="ru")
        )

    def test_add_pack_type_to_good(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="0"))

        self.foodpedia_graph.add_pack_type_to_good("0", "Пакет пластиковый, металлизированный, многослойный")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/0"),
            URIRef("http://foodpedia.tk/ontology#pack_type"),
            Literal("Пакет пластиковый, металлизированный, многослойный", lang="ru")
        )

    def test_add_string_object_ru(self):
        self.foodpedia_graph.add_string_object(
            URIRef("http://foodpedia.tk/resource/999"),
            URIRef("http://purl.org/goodrelations/v1#name"),
            "bla-bla-bla",
            "ru"
        )

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/999"),
            URIRef("http://purl.org/goodrelations/v1#name"),
            Literal("bla-bla-bla", lang="ru")
        )

    def test_add_string_object_en(self):
        self.foodpedia_graph.add_string_object(
            URIRef("http://foodpedia.tk/resource/888"),
            URIRef("http://purl.org/goodrelations/v1#"),
            "bla-bla-bla",
            "en"
        )

    def test_add_calories_as_double(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="10"))

        self.foodpedia_graph.add_calories_as_double_to_good("10", 179.5)

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/10"),
            URIRef("http://purl.org/foodontology#energyPer100gAsDouble"),
            Literal(179.5, datatype=XSD.double)
        )

    def test_add_calories_as_double_passed_as_string(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="10"))

        self.foodpedia_graph.add_calories_as_double_to_good ("10", "179.5")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/10"),
            URIRef("http://purl.org/foodontology#energyPer100gAsDouble"),
            Literal(179.5, datatype=XSD.double)
        )

    def test_add_calories_as_double_passed_as_integer(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="10"))

        self.foodpedia_graph.add_calories_as_double_to_good("10", 179)

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/10"),
            URIRef("http://purl.org/foodontology#energyPer100gAsDouble"),
            Literal(179, datatype=XSD.double)
        )

    def test_add_fats_as_double(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="999999999999999999"))

        self.foodpedia_graph.add_fats_as_double_to_good("999999999999999999", 11.5)

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/999999999999999999"),
            URIRef("http://purl.org/foodontology#fatPer100gAsDouble"),
            Literal(11.5, datatype=XSD.double)
        )

    def test_add_proteins_as_double(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="8"))

        self.foodpedia_graph.add_proteins_as_double_to_good("8", 19.00)

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/8"),
            URIRef("http://purl.org/foodontology#proteinsPer100gAsDouble"),
            Literal(19.0, datatype=XSD.double)
        )

    def test_add_carbohydrates_as_double(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="8"))

        self.foodpedia_graph.add_carbohydrates_as_double_to_good("8", 19.00)

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/8"),
            URIRef("http://purl.org/foodontology#carbohydratesPer100gAsDouble"),
            Literal(19.0, datatype=XSD.double)
        )

    def test_add_double_object(self):
        self.foodpedia_graph.add_double_object(
            URIRef("http://foodpedia.tk/resource/678"),
            URIRef("http://purl.org/foodontology#energyPer100gAsDouble"),
            179.5
        )

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/678"),
            URIRef("http://purl.org/foodontology#energyPer100gAsDouble"),
            Literal(179.5, datatype=XSD.double)
        )

    def test_add_eadditive(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="100500"))

        self.foodpedia_graph.add_eadditive_to_good("100500", "E401")

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/100500"),
            URIRef("http://purl.org/foodontology#containsIngredient"),
            URIRef("http://foodpedia.tk/resource/E401")
        )

    def test_convert_eadditive_name_to_uri(self):
        eadditive_name = "E401"
        uri = FoodpediaGraph.convert_eadditive_name_to_uri(eadditive_name)
        self.assertEqual(URIRef("http://foodpedia.tk/resource/E401"), uri)

    def test_convert_string_barcode_to_uri(self):
        barcode = "1234"
        uri = FoodpediaGraph.convert_barcode_to_uri(barcode)
        self.assertEqual(URIRef("http://foodpedia.tk/resource/1234"), uri)

    def test_convert_int_barcode_to_uri(self):
        barcode = 1234
        uri = FoodpediaGraph.convert_barcode_to_uri(barcode)
        self.assertEqual(URIRef("http://foodpedia.tk/resource/1234"), uri)

    def test_add_good_item_added_properties(self):
        good_item = GoodItem()
        good_item["goodsmatrix_url"] = "http://www.goodsmatrix.ru/goods/4600605021002.html"
        good_item["name"] = "supergood"
        good_item["barcode"] = "1111"
        good_item["best_before"] = "24 hours"
        good_item["comment"] = "description?"
        good_item["ingredients"] = "salt"
        good_item["netto_weight"] = "100500"
        good_item["standart"] = "TU-TU-TU"
        good_item["store_conditions"] = "dark side of the World"
        good_item["esl_as_string"] = "bla-bla-bla"
        good_item["proteins_as_double"] = 123.4
        good_item["fats_as_double"] = 56.7
        good_item["carbohydrates_as_double"] = 8.9
        good_item["calories_as_double"] = 0
        good_item["pack_type"] = "do not know"
        self.foodpedia_graph.add_good_item(good_item)

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/goodrelations/v1#name"),
            Literal("supergood", lang="ru")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/goodrelations/v1#hasEAN_UCC-13"),
            Literal("1111")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://foodpedia.tk/ontology#best_before"),
            Literal("24 hours", lang="ru")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/goodrelations/v1#description"),
            Literal("description?", lang="ru")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/foodontology#ingredientsListAsText"),
            Literal("salt", lang="ru")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://foodpedia.tk/ontology#netto_mass"),
            Literal("100500", lang="ru")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://foodpedia.tk/ontology#standart"),
            Literal("TU-TU-TU", lang="ru")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://foodpedia.tk/ontology#store_cond"),
            Literal("dark side of the World", lang="ru")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://foodpedia.tk/ontology#esl"),
            Literal("bla-bla-bla", lang="ru")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/foodontology#proteinsPer100gAsDouble"),
            Literal(123.4, datatype=XSD.double)
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/foodontology#fatPer100gAsDouble"),
            Literal(56.7, datatype=XSD.double)
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/foodontology#carbohydratesPer100gAsDouble"),
            Literal(8.9, datatype=XSD.double)
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/foodontology#energyPer100gAsDouble"),
            Literal(0, datatype=XSD.double)
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://foodpedia.tk/ontology#pack_type"),
            Literal("do not know", lang="ru")
        )

    def test_add_good_item_does_not_add_missed_properties(self):
        self.foodpedia_graph.add_good_item(GoodItem(barcode="1111"))

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"), RDF.type, URIRef("http://purl.org/foodontology#Food")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/goodrelations/v1#hasEAN_UCC-13"),
            Literal("1111")
        )
        self.assertEqual(len(self.foodpedia_graph), 2)

    def test_add_good_item_throws_key_error_on_missed_barcode(self):
        good_item = GoodItem()

        with self.assertRaises(KeyError):
            self.foodpedia_graph.add_good_item(good_item)

    def test_add_good_item_does_not_add_not_correct_property(self):
        good_item_like_dict = {"barcode": "1111", "not_correct_property": "not_correct_property"}

        self.foodpedia_graph.add_good_item(good_item_like_dict)

        self.assertFalse(filter(lambda x: "not_correct_property" in x, self.foodpedia_graph.objects()))

    def test_add_good_item_adds_eadditives_to_graph(self):
        good_item = GoodItem(barcode="1111", e_additives=["E100", "E101"])

        self.foodpedia_graph.add_good_item(good_item)

        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/foodontology#containsIngredient"),
            URIRef("http://foodpedia.tk/resource/E100")
        )
        self.assertTripleInGraph(
            URIRef("http://foodpedia.tk/resource/1111"),
            URIRef("http://purl.org/foodontology#containsIngredient"),
            URIRef("http://foodpedia.tk/resource/E101")
        )

    def assertTripleInGraph(self, *triple):
        def graph_to_string(graph):
            return ",\n".join(str((s, p, o)) for s, p, o in graph)

        self.assertIn(triple, self.foodpedia_graph,
                      msg="the triple \n{0}\n not found in the graph \n{1}\n".format(
                          triple, graph_to_string(self.foodpedia_graph)
                          )
                      )

    def tearDown(self):
        self.foodpedia_graph.close()
