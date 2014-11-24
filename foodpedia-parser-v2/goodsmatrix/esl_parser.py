# -*- coding: utf-8 -*-
import re


LIST_OF_POSSIBLE_ESL = {
        'proteins': u'Белки',
        'fats': u'Жиры',
        'carbohydrates': u'Углеводы',
        'calories': u'Энергетическая ценность'}


def parse_esl(string):
    parsed_dict = dict()
    for key in LIST_OF_POSSIBLE_ESL:
        m = re.search(ur"{0}\s*:\s*(\d*[,|\.]?\d+)\s*г?".format(LIST_OF_POSSIBLE_ESL[key]),
                      string,
                      flags=re.IGNORECASE)
        if m:
            number = float(m.group(1).replace(',', '.'))
            parsed_dict[key] = number
    return parsed_dict
