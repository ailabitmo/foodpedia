from goodsmatrix import string_processor


class ExtractEsl(object):
    def process_item(self, good_item, spider):
        if 'esl_as_string' in good_item:
            esl_as_string = good_item['esl_as_string']
            good_item.update(string_processor.parse_esl(esl_as_string))
        return good_item


class ExtractEAdditives(object):
    def process_item(self, good_item, spider):
        if 'ingredients' in good_item:
            ingridients_as_string = good_item['ingredients']
            extracted_e_additives = string_processor.parse_e_additives(
                ingridients_as_string)
            good_item['e_additives'] = extracted_e_additives
        return good_item


class StripMultilineStringProperties(object):
    def process_item(self, good_item, spider):
        for key in good_item:
            try:
                good_item[key] = string_processor.strip_multiline(good_item[key])
            except AttributeError:
                pass
        return good_item
