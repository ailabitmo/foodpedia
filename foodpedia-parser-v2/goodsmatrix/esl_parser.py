# -*- coding: utf-8 -*-
import re


LIST_OF_POSSIBLE_ESL = {
        'proteins': u'Белки|белки',
        'fats': u'Жиры|жиры',
        'carbohydrates': u'Углеводы|углеводы',
        'calories': u'Энергетическая\ ценность|энергетическая\ ценность'}


def parse_esl(string):
    parsed_dict = dict()
    for key in LIST_OF_POSSIBLE_ESL:
        m = re.search(ur"({0})\s*:\s*(?P<weight>\d*[,|\.]?\d+)\s*[г|ккал]?".format(LIST_OF_POSSIBLE_ESL[key]),
                      string,
                      flags=re.IGNORECASE)
        if m:
            number = float(m.group('weight').replace(u',', u'.'))
            parsed_dict[key] = number
    return parsed_dict
