"""utility functions to transforms goodmatrix.ru's specific urls"""
def transform_catalog_node_url_to_url_with_goods(catalog_node_url):
    """transofrm catalog's end node's url with pagination
    to a url with a single-page list of products for the category.
    """
    return catalog_node_url.replace('goods-catalogue', 'map')


def transform_goods_analogues_url_to_goods_url(goods_analogues_url):
    """transform url with a list of analogues for a good
    to a url with description for the good
    """
    return goods_analogues_url.replace("goods-analogue", "goods")
