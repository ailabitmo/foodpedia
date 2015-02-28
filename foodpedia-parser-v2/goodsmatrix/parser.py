import scrapy
from scrapy.contrib.spiders import CrawlSpider

from goodsmatrix import xpath_extractor
from goodsmatrix import url_extractor
from goodsmatrix.good_item import GoodItem


from scrapy import log


class GoodsMatrixSpider(CrawlSpider):
    name = 'goodsmatrix'
    allowed_domains = ['goodsmatrix.ru']
    base_start_url = 'http://www.goodsmatrix.ru/goods-catalogue/{0}.html'
    #start_urls = ['http://www.goodsmatrix.ru/goods-catalogue/Frozen-meat-natural-convenience-foods.html']
    #start_urls = ['http://www.goodsmatrix.ru/goods-catalogue/Goods/Foodstuffs.html']

    def __init__(self, category="Foodstuffs", *args, **kwargs):
        super(GoodsMatrixSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.base_start_url.format(category)]

    def parse(self, response):
        return self.parse_catalog_node(response)

    def parse_catalog_node(self, response):
        log.msg("PARSE CATALOG NODE: {0}".format(response.url), level=log.INFO)
        child_nodes_urls = url_extractor.extract_child_nodes_urls(response)
        if child_nodes_urls:
            for child_node_url in child_nodes_urls:
                yield scrapy.Request(child_node_url, callback=self.parse_catalog_node)
        else:
            yield self.parse_catalog_end_node(response)

    def parse_catalog_end_node(self, response):
        """parse catalog node without children.
        return prepeared request to  parse the category's list of goods."""
        log.msg("PARSE CATALOG END NODE: {0}".format(response.url), level=log.INFO)
        return scrapy.Request(
            url_extractor.extract_url_with_list_of_goods(response),
            callback=self.parse_list_of_goods
        )

    def parse_list_of_goods(self, response):
        for goods_url in url_extractor.extract_goods_urls(response):
            yield scrapy.Request(
                goods_url,
                meta={
                        'dont_redirect': True,
                        'handle_httpstatus_list': [302]
                     },
                callback=self.parse_good
            )

    def parse_good(self, response):
        log.msg("PARSE GOOD: {0}".format(response.url), level=log.DEBUG)
        good = GoodItem(xpath_extractor.extract_goods_properties_dict(response))
        if good:
            good['goodsmatrix_url'] = response.url
            return good
        else:
            log.msg("can't parse {0}".format(response.url, level=log.ERROR))
