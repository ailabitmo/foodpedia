# -*- coding: utf-8 -*-
import re


LIST_OF_POSSIBLE_ESL = {
        'proteins': u'Белки|белки',
        'fats': u'Жиры',
        'carbohydrates': u'Углеводы',
        'calories': u'Энергетическая ценность'}


def parse_esl(string):
    parsed_dict = dict()
    for key in LIST_OF_POSSIBLE_ESL:
        m = re.search(ur"({0})\s*:\s*(?P<weight>\d*[,|\.]?\d+)\s*г?".format(LIST_OF_POSSIBLE_ESL[key]),
                      string,
                      flags=re.IGNORECASE)
        if m:
            #print m.group('weight')
            number = float(m.group('weight').replace(u',', u'.'))
            parsed_dict[key] = number
    return parsed_dict
