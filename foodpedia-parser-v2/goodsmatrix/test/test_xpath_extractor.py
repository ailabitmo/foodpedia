import unittest
from scrapy.http import HtmlResponse

from goodsmatrix import xpath_extractor


class TestExtractChildNodesURLs(unittest.TestCase):
    def test_one_child_node(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<a href='http://test.com' class='grtext4'>test</a>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
            xpath_extractor.extract_child_nodes_urls(stub_response),
            [r'http://test.com'])

    def test_two_child_nodes(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<a href='http://test1.com' class='grtext4'>test</a>"
                r"<a href='http://test2.com' class='grtext4'>test</a>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
            xpath_extractor.extract_child_nodes_urls(stub_response),
            [r'http://test1.com', r'http://test2.com'])

    def test_no_child_nodes(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<a href='http://test1.com' class='grtext3'>test</a>"
                r"<a href='http://test2.com' class='grtext5'>test</a>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
            xpath_extractor.extract_child_nodes_urls(stub_response),
            [])

    def test_supporting_urls_are_not_detected_as_child(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<a href='http://test1.com' class='grtext4' runat='server'>test</a>"
                r"<a href='http://test2.com' class='grtext4'>test</a>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
            xpath_extractor.extract_child_nodes_urls(stub_response),
            [r'http://test2.com'])


class TestExtractGoodsAnaloguesURLsFromListOfGood(unittest.TestCase):
    def test_one_good_analogue(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<a href='http://goodsmatrix.ru/goods-analogue/4607055680193.html'"
                r"id='ctl00_ContentPH_GoodsDG_ctl03_A2'>4607055680193</a>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
                xpath_extractor.extract_goods_analogues_urls(stub_response),
                ['http://goodsmatrix.ru/goods-analogue/4607055680193.html'])

    def test_two_good_analogues(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<a href='http://test.com/1.html' id='ctl00_ContentPH_GoodsDG_ctl03_A2'>1</a>"
                r"<a href='http://test.com/2.html' id='ctl00_ContentPH_GoodsDG_ctl14_A2'>text</a>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
                xpath_extractor.extract_goods_analogues_urls(stub_response),
                ['http://test.com/1.html',
                 'http://test.com/2.html'])

    def test_no_good_analogues(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<a href='http://test.com/1.html' id='ctl00_ContentPH_GoodsDG_ctl03_A3'>1</a>"
                r"<a href='http://test.com/2.html' id='ctl00_ContentPH_GoodsDG_ctl03_A4'>text</a>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
                xpath_extractor.extract_goods_analogues_urls(stub_response),
                [])

    def test_corrupted_ids(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<a href='http://test.com/1.html' id='ctl00_ContentPH_GoodsDG_ctl3_A2'>1</a>"
                r"<a href='http://test.com/2.html' id='ct00_ContentPH_GoodsDG_ctl03_A2'>text</a>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
                xpath_extractor.extract_goods_analogues_urls(stub_response),
                [])


class TestExtractGoodsProperties(unittest.TestCase):
    def test_all_properties_exists(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<span id='ctl00_ContentPH_GoodsName'>ice cream</span>"
                r"<span id='ctl00_ContentPH_BarCodeL'>2220066000747</span>"
                r"<span id='ctl00_ContentPH_KeepingTime'>13</span>"
                r"<span id='ctl00_ContentPH_Comment'>comment</span>"
                r"<span id='ctl00_ContentPH_Composition'>one, two, three</span>"
                r"<span id='ctl00_ContentPH_Net'>1000,00 g</span>"
                r"<span id='ctl00_ContentPH_Gost'>TU 919191291</span>"
                r"<span id='ctl00_ContentPH_StoreCond'>+25</span>"
                r"<span id='ctl00_ContentPH_ESL'>Proteins: 10,00 g</span>"
                r"<span id='ctl00_ContentPH_PackingType'>test</span>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
            xpath_extractor.extract_goods_properties_dict(stub_response),
            {
                'name': 'ice cream',
                'barcode': '2220066000747',
                'best_before': '13',
                'comment': 'comment',
                'ingredients': 'one, two, three',
                'netto_weight': '1000,00 g',
                'standart': 'TU 919191291',
                'store_conditions': '+25',
                'esl': 'Proteins: 10,00 g',
                'pack_type': 'test',
            })

    def test_if_property_does_not_exist_then_it_is_not_added_to_dict(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"<span id='ctl00_ContentPH_GoodsName'>ice cream</span>"
                r"<span id='ctl00_ContentPH_BarCodeL'>2220066000747</span>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
            xpath_extractor.extract_goods_properties_dict(stub_response),
            {
                'name': 'ice cream',
                'barcode': '2220066000747',
            })

    def test_no_goods_properties_in_response(self):
        stub_response = HtmlResponse(
            url="",
            body=(
                r"<html>"
                r"<body>"
                r"</body>"
                r"</html>"))
        self.assertEqual(
            xpath_extractor.extract_goods_properties_dict(stub_response),
            dict()
            )


if __name__ == "__main__":
    unittest.main()
