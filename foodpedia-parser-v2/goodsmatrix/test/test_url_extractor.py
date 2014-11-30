import unittest

from scrapy.http import HtmlResponse

from goodsmatrix import url_extractor


class TestExctractGoodsURLs(unittest.TestCase):
    def test_one_good(self):
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
                list(url_extractor.extract_goods_urls(stub_response)),
                ['http://goodsmatrix.ru/goods/4607055680193.html'])
