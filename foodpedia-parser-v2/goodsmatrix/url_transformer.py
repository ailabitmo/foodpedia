def transform_catalog_node_url_to_url_with_goods(catalog_node_url):
    return catalog_node_url.replace('goods-catalogue', 'map')


def transform_goods_analogues_url_to_goods_url(goods_analogues_url):
    return goods_analogues_url.replace("goods-analogue", "goods")
