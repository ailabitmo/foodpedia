# -*- coding: utf-8 -*-
import re


LIST_OF_POSSIBLE_ESL = {
        'proteins_as_double': u'Белки|белки',
        'fats_as_double': u'Жиры|жиры',
        'carbohydrates_as_double': u'Углеводы|углеводы',
        'calories_as_double': u'Энергетическая\ ценность|энергетическая\ ценность'}


def parse_esl(string):
    parsed_dict = dict()
    for key in LIST_OF_POSSIBLE_ESL:
        posible_esl_component_word = LIST_OF_POSSIBLE_ESL[key]
        m = re.search(ur"({0})\s*:\s*(не более|не менее)?\s*(?P<weight>\d*[,|\.]?\d+)\s*[г|ккал]?".format(
                          posible_esl_component_word),
                      string,
                      flags=re.IGNORECASE|re.UNICODE)
        if m:
            number = float(m.group('weight').replace(u',', u'.'))
            parsed_dict[key] = number
    return parsed_dict


def postprocess_extracted_property_string(string):
    return ' '.join(line.strip() for line in string.split('\n'))


def parse_e_additives(string):
    found_additives_list = re.findall(ur"\b([Е|E]-?\d\d\d\w?)\b", string, flags=re.IGNORECASE|re.UNICODE)
    return list(convert_to_asci_without_hyphen(additive) for additive in found_additives_list)

def convert_to_asci_without_hyphen(extracted_additive_string):
    extracted_additive_string = 'E' + extracted_additive_string[1:]
    extracted_additive_string = re.sub('-', '', extracted_additive_string)
    return extracted_additive_string.encode('ascii', 'ignore')
