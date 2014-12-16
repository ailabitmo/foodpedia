import unittest


from goodsmatrix import url_transformer


class TestUrlTransformers(unittest.TestCase):
    def test_transform_catalog_node_url_to_url_with_goods(self):
        self.assertEqual(
            url_transformer.transform_catalog_node_url_to_url_with_goods(
                "http://www.goodsmatrix.ru/goods-catalogue/Bread-sticks/Gorodskoy-bread-stics.html"),
            "http://www.goodsmatrix.ru/map/Bread-sticks/Gorodskoy-bread-stics.html")

    def test_not_correct_catalog_node_url_is_not_changed(self):
        self.assertEqual(
            url_transformer.transform_catalog_node_url_to_url_with_goods(
                "http://www.goodsmatrix.ru/t/Bread-sticks/Gorodskoy-bread-stics.html"),
            "http://www.goodsmatrix.ru/t/Bread-sticks/Gorodskoy-bread-stics.html")

    def test_transform_goods_analogues_url_to_goods_url(self):
        self.assertEqual(
            url_transformer.transform_goods_analogues_url_to_goods_url(
                "http://www.goodsmatrix.ru/goods-analogue/4602977002184.html"),
            "http://www.goodsmatrix.ru/goods/4602977002184.html")

    def test_not_correct_goods_analogues_url_is_not_changed(self):
        self.assertEqual(
            url_transformer.transform_goods_analogues_url_to_goods_url(
                "http://www.goodsmatrix.ru/ttttt/4602977002184.html"),
            "http://www.goodsmatrix.ru/ttttt/4602977002184.html")


if __name__ == "__main__":
    unittest.main()
