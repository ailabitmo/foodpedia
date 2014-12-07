def extract_child_nodes_urls(response):
    return response.xpath("//a[contains(@class, 'grtext4') and not(contains(@runat, 'server'))]/@href").extract()


def extract_goods_analogues_urls(response):
    return response.xpath("//a[re:test(@id, 'ctl00_ContentPH_GoodsDG_ctl\d\d_A2$')]//@href").extract()


def extract_goods_properties_dict(response):
    result_dict = dict()
    for property_name in GOODS_PROPERTIES_MAP_ON_XPATH_IDS:
        xpath_id = GOODS_PROPERTIES_MAP_ON_XPATH_IDS[property_name]
        extracted_value = _extract_goods_property(response, xpath_id)
        if extracted_value is not None:
            result_dict[property_name] = extracted_value
    return result_dict


def _extract_goods_property(response, xpath_id):
    xpath_pattern = "//span[@id='{0}']/text()".format(xpath_id)
    extracted_list = response.xpath(xpath_pattern).extract()
    extracted_list = list(string for string in extracted_list if string.strip())
    return '\n'.join(extracted_list) if extracted_list else None

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
