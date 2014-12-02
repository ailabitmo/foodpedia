from unittest import TestCase

from rdflib import Namespace

from goodsmatrix.pipelines import RDFPipeline


class TestRDFPipeline(TestCase):
    def setUp(self):
        self.pipeline = RDFPipeline()

    def test_needed_namespaces_are_binded(self):
        get_namespaces = self.pipeline.graph.namespace_manager.namespaces #Low of Demetra is violated
                                                                          #redesign the RDFPipeline???
        self.assertIn(('food', Namespace("http://purl.org/foodontology#")), get_namespaces())
        self.assertIn(('foodpedia-owl', Namespace("http://foodpedia.tk/ontology#")), get_namespaces())
        self.assertIn(('gr', Namespace("http://purl.org/goodrelations/v1#")), get_namespaces())

    def tearDown(self):
        self.pipeline.graph.close()
