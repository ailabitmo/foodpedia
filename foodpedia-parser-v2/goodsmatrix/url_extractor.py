from goodsmatrix import xpath_extractor
from goodsmatrix import url_transformer


def extract_child_nodes_urls(response):
    return xpath_extractor.extract_child_nodes_urls(response)

def extract_goods_urls(response):
    return (url_transformer.transform_goods_analogues_url_to_goods_url(goods_analogue_url)
            for goods_analogue_url
            in xpath_extractor.extract_goods_analogues_urls(response))

def extract_url_with_list_of_goods(response):
    return url_transformer.transform_catalog_node_url_to_url_with_goods(response.url)
