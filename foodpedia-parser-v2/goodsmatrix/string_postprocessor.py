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
                      flags=re.IGNORECASE)
        if m:
            number = float(m.group('weight').replace(u',', u'.'))
            parsed_dict[key] = number
    return parsed_dict


def postprocess_extracted_property_string(string):
    return ' '.join(line.strip() for line in string.split('\n'))
