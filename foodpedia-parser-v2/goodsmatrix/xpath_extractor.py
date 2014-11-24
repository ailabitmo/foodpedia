import goodsmatrix.url_transformer


def extract_child_nodes_urls(response):
    return response.xpath("//a[contains(@class, 'grtext4') and not(contains(@runat, 'server'))]/@href").extract()


def extract_goods_url_from_list_of_goods(response):
    return (goodsmatrix.url_transformer.transform_goods_analogues_url_to_goods_url(goods_analogue_url)
            for goods_analogue_url
            in extract_goods_analogues_urls_from_list_of_goods(response))


def extract_goods_analogues_urls_from_list_of_goods(response):
    return response.xpath("//a[re:test(@id, 'ctl00_ContentPH_GoodsDG_ctl\d\d_A2$')]//@href").extract()


def extract_goods_properties_dict(response):
    return {property_name: _extract_goods_property(response, xpath_id)
            for property_name, xpath_id
            in GOODS_PROPERTIES_MAP_ON_XPATH_IDS.iteritems()}

def _extract_goods_property(response, xpath_id):
    return ' '.join(response.xpath("//span[@id='{0}']/text()".format(xpath_id)).extract()).strip()

GOODS_PROPERTIES_MAP_ON_XPATH_IDS = {
        'name': 'ctl00_ContentPH_GoodsName',
        'barcode': 'ctl00_ContentPH_BarCodeL',
        'best_before': 'ctl00_ContentPH_KeepingTime',
        'comment': 'ctl00_ContentPH_Comment',
        'ingredients': 'ctl00_ContentPH_Composition',
        'netto_weight': 'ctl00_ContentPH_Net',
        'standart': 'ctl00_ContentPH_Gost',
        'store_conditions': 'ctl00_ContentPH_StoreCond',
        'esl': 'ctl00_ContentPH_ESL',
        'pack_type': 'ctl00_ContentPH_PackingType',
    }
