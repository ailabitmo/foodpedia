from unittest import TestCase

from rdflib import Namespace, Graph, URIRef, Literal
from rdflib.namespace import RDF

from goodsmatrix.foodpedia_graph import FoodpediaGraph
from goodsmatrix.good_item import GoodItem


class TestFoodpediaGraph(TestCase):
    def setUp(self):
        self.foodpedia_graph = FoodpediaGraph(Graph())

    def test_needed_namespaces_are_binded(self):
        self.assertIn(("food", Namespace("http://purl.org/foodontology#")), self.foodpedia_graph.get_namespaces())
        self.assertIn(("foodpedia-owl", Namespace("http://foodpedia.tk/ontology#")), self.foodpedia_graph.get_namespaces())
        self.assertIn(("gr", Namespace("http://purl.org/goodrelations/v1#")), self.foodpedia_graph.get_namespaces())

    def test_add_good_item_added_reference(self):
        good_item = GoodItem()
        good_item["url"] = "http://hohoho.com/1111"
        self.foodpedia_graph.add_good_item(good_item)

        self.assertIn(
            (URIRef("http://hohoho.com/1111"), RDF.type, URIRef("http://purl.org/foodontology#Food")),
            self.foodpedia_graph
        )

    def test_add_good_item_added_properties(self):
        good_item = GoodItem()
        good_item["url"] = "http://hohoho.com/1111"
        good_item["name"] = "supergood"
        good_item["barcode"] = "1111"
        good_item["best_before"] = "24 hours"
        good_item["comment"] = "description?"
        good_item["ingredients"] = "salt"
        good_item["netto_weight"] = "100500"
        good_item["standart"] = "TU-TU-TU"
        good_item["store_conditions"] = "dark side of the World"
        good_item["esl"] = "bla-bla-bla"
        good_item["proteins_as_double"] = 123.4
        good_item["fats_as_double"] = 56.7
        good_item["carbohydrates_as_double"] = 8.9
        good_item["calories_as_double"] = 0
        good_item["pack_type"] = "do not know"
        self.foodpedia_graph.add_good_item(good_item)

        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://purl.org/goodrelations/v1#name"),
                Literal("supergood", lang="ru")
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://purl.org/goodrelations/v1#hasEAN_UCC-13"),
                Literal("1111", lang="ru")
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://foodpedia.tk/ontology#best_before"),
                Literal("24 hours", lang="ru")
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://purl.org/goodrelations/v1#description"),
                Literal("description?", lang="ru")
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://purl.org/foodontology#ingredientsListAsText"),
                Literal("salt", lang="ru")
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://foodpedia.tk/ontology#netto_mass"),
                Literal("100500", lang="ru")
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://foodpedia.tk/ontology#standart"),
                Literal("TU-TU-TU", lang="ru")
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://foodpedia.tk/ontology#store_cond"),
                Literal("dark side of the World", lang="ru")
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://foodpedia.tk/ontology#esl"),
                Literal("bla-bla-bla", lang="ru")
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://purl.org/foodontology#proteinsPer100gAsDouble"),
                Literal(123.4)
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://purl.org/foodontology#fatPer100gAsDouble"),
                Literal(56.7)
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://purl.org/foodontology#carbohydratesPer100gAsDouble"),
                Literal(8.9)
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://purl.org/foodontology#energyPer100gAsDouble"),
                Literal(0)
            ),
            self.foodpedia_graph
        )
        self.assertIn(
            (
                URIRef("http://hohoho.com/1111"),
                URIRef("http://foodpedia.tk/ontology#pack_type"),
                Literal("do not know", lang="ru")
            ),
            self.foodpedia_graph
        )

    def test_add_good_item_does_not_add_missed_properties(self):
        good_item = GoodItem()
        good_item["url"] = "http://hohoho.com/1111"
        self.foodpedia_graph.add_good_item(good_item)

        foodpedia_graph_iter = iter(self.foodpedia_graph)
        self.assertEqual(
            (URIRef("http://hohoho.com/1111"), RDF.type, URIRef("http://purl.org/foodontology#Food")),
            foodpedia_graph_iter.next()
        )
        self.assertRaises(StopIteration, foodpedia_graph_iter.next)

    def test_add_good_item_throws_key_error_on_missed_url(self):
        good_item = GoodItem()

        with self.assertRaises(KeyError):
            self.foodpedia_graph.add_good_item(good_item)

    def test_add_good_item_does_not_add_not_correct_property(self):
        good_item = dict()
        good_item["url"] = "http://hohoho.com/1111"
        good_item["test"] = "test"

        self.foodpedia_graph.add_good_item(good_item)

        foodpedia_graph_iter = iter(self.foodpedia_graph)
        self.assertEqual(
            (URIRef("http://hohoho.com/1111"), RDF.type, URIRef("http://purl.org/foodontology#Food")),
            foodpedia_graph_iter.next()
        )
        self.assertRaises(StopIteration, foodpedia_graph_iter.next)


    def tearDown(self):
        self.foodpedia_graph.close()
