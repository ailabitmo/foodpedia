import scrapy
from scrapy.contrib.spiders import CrawlSpider

#from goodsmatrix.url_transformer import transform_catalog_node_url_to_url_with_goods
from goodsmatrix.url_transformer import transform_catalog_node_url_to_url_with_goods
from goodsmatrix import xpath_extractor
from goodsmatrix.good_item import GoodItem


class GoodsMatrixSpider(CrawlSpider):
    name = 'goodsmatrix'
    allowed_domains = ['goodsmatrix.ru']
    start_urls = ['http://www.goodsmatrix.ru/goods-catalogue/Goods/Bakeries-products/Bread-sticks.html']
    #start_urls = ['http://www.goodsmatrix.ru/goods-catalogue/Goods/Foodstuffs.html']

    def parse(self, response):
        return self.parse_catalog_node(response)

    def parse_catalog_node(self, response):
        child_nodes_urls = xpath_extractor.extract_child_nodes_urls(response)
        if child_nodes_urls:
            for child_node_url in child_nodes_urls:
                yield scrapy.Request(child_node_url, callback=self.parse_catalog_node)
        else:
            url_with_list_of_goods = transform_catalog_node_url_to_url_with_goods(response.url)
            yield scrapy.Request(url_with_list_of_goods, callback=self.parse_list_of_goods)

    def parse_list_of_goods(self, response):
        for goods_url in xpath_extractor.extract_goods_url_from_list_of_goods(response):
            yield scrapy.Request(goods_url, callback=self.parse_good)

    def parse_good(self, response):
        good = GoodItem(xpath_extractor.extract_goods_properties_dict(response))
        good['url'] = response.url
        return good
