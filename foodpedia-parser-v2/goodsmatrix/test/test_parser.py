from unittest import TestCase
from mock import patch
from scrapy.http import HtmlResponse

from goodsmatrix.parser import GoodsMatrixSpider
from goodsmatrix.good_item import GoodItem


class TestGoodsMatrixSpider(TestCase):
    def setUp(self):
        self.spider = GoodsMatrixSpider()

    @patch('goodsmatrix.url_extractor.extract_child_nodes_urls')
    def test_parse_catalog_node_with_one_child(self, mock_extract_method):
        mock_extract_method.return_value = ['http://test.com']
        stub_response = HtmlResponse(url="")

        requests = self.spider.parse_catalog_node(stub_response)

        request = requests.next()
        self.assertEqual(request.url, 'http://test.com')
        self.assertEqual(request.callback, self.spider.parse_catalog_node)
        with self.assertRaises(StopIteration):
            requests.next()

    @patch('goodsmatrix.url_extractor.extract_child_nodes_urls')
    def test_parse_catalog_node_with_two_children(self, mock_extract_method):
        mock_extract_method.return_value = ['http://test.com', 'http://test2.com']
        stub_response = HtmlResponse(url="")

        requests = self.spider.parse_catalog_node(stub_response)

        request = requests.next()
        self.assertEqual(request.url, 'http://test.com')
        self.assertEqual(request.callback, self.spider.parse_catalog_node)
        request = requests.next()
        self.assertEqual(request.url, 'http://test2.com')
        self.assertEqual(request.callback, self.spider.parse_catalog_node)
        with self.assertRaises(StopIteration):
            requests.next()

    @patch('goodsmatrix.url_extractor.extract_child_nodes_urls')
    def test_parse_catalog_node_without_children(self, mock_extract_method):
        mock_extract_method.return_value = []
        stub_response = HtmlResponse(url="http://goodsmatrix.ru")

        requests = self.spider.parse_catalog_node(stub_response)

        request = requests.next()
        self.assertEqual(request.callback, self.spider.parse_list_of_goods)
        with self.assertRaises(StopIteration):
            requests.next()

    def test_parse_catalog_end_node_with_correct_url(self):
        stub_response = HtmlResponse(url=r"http://www.goodsmatrix.ru/goods-catalogue/Dishwashing-detergent/Dishwashing-gel.html")

        request = self.spider.parse_catalog_end_node(stub_response)

        self.assertEqual(request.url, r"http://www.goodsmatrix.ru/map/Dishwashing-detergent/Dishwashing-gel.html")
        self.assertEqual(request.callback, self.spider.parse_list_of_goods)

    @patch('goodsmatrix.url_extractor.extract_goods_urls')
    def test_parse_list_of_goods_with_one_item(self, mock_extract_method):
        mock_extract_method.return_value = ['http://goodsmatrix.ru/goods/4607055680193.html']
        stub_response = HtmlResponse(url="http://goodsmatrix.ru")

        requests = self.spider.parse_list_of_goods(stub_response)

        request = requests.next()
        self.assertEqual(request.url, 'http://goodsmatrix.ru/goods/4607055680193.html')
        self.assertEqual(request.callback, self.spider.parse_good)
        with self.assertRaises(StopIteration):
            requests.next()

    @patch('goodsmatrix.url_extractor.extract_goods_urls')
    def test_parse_list_of_goods_with_two_items(self, mock_extract_method):
        mock_extract_method.return_value = [
            'http://goodsmatrix.ru/goods/4607055680193.html',
            'http://goodsmatrix.ru/goods/4607055680194.html'
        ]
        stub_response = HtmlResponse(url="http://goodsmatrix.ru")

        requests = self.spider.parse_list_of_goods(stub_response)

        request = requests.next()
        self.assertEqual(request.url, 'http://goodsmatrix.ru/goods/4607055680193.html')
        self.assertEqual(request.callback, self.spider.parse_good)
        request = requests.next()
        self.assertEqual(request.url, 'http://goodsmatrix.ru/goods/4607055680194.html')
        self.assertEqual(request.callback, self.spider.parse_good)
        with self.assertRaises(StopIteration):
            requests.next()

    @patch('goodsmatrix.xpath_extractor.extract_goods_properties_dict')
    def test_parse_good_with_common_properties(self, mock_extracted_dict):
        mock_extracted_dict.return_value = {
                'name': 'ice cream',
                'barcode': '2220066000747',
                'best_before': '13',
                'comment': 'comment',
                'ingredients': 'one, two, three',
                'netto_weight': '1000,00 g',
                'standart': 'TU 919191291',
                'store_conditions': '+25',
                'esl_as_string': 'esl',
                'pack_type': 'test',
            }
        stub_response = HtmlResponse(url="http://goodsmatrix.ru")

        good = self.spider.parse_good(stub_response)

        self.assertTrue(mock_extracted_dict.called)
        self.assertEqual(good['goodsmatrix_url'], 'http://goodsmatrix.ru')
        self.assertEqual(good['name'], 'ice cream')
        self.assertEqual(good['barcode'], '2220066000747')
        self.assertEqual(good['best_before'], '13')
        self.assertEqual(good['comment'], 'comment')
        self.assertEqual(good['ingredients'], 'one, two, three')
        self.assertEqual(good['netto_weight'], '1000,00 g')
        self.assertEqual(good['standart'], 'TU 919191291')
        self.assertEqual(good['store_conditions'], '+25')
        self.assertEqual(good['esl_as_string'], 'esl')
        self.assertEqual(good['pack_type'], 'test')
