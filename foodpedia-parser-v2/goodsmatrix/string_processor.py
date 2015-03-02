# -*- coding: utf-8 -*-
import lxml
import re
import htmlentitydefs
from HTMLParser import HTMLParser


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


def strip_multiline(multiline_string):
    return ' '.join(line.strip() for line in multiline_string.split('\n'))


def parse_e_additives(string):
    string = string.upper()
    found_additives_list = re.findall(ur"\b([ЕE]-?\d\d\d[\wА]?)\b", string, flags=re.IGNORECASE|re.UNICODE)
    return list(convert_to_asci_without_hyphen(additive) for additive in found_additives_list)


def convert_to_asci_without_hyphen(extracted_additive_string):
    extracted_additive_string = 'E' + extracted_additive_string[1:]
    extracted_additive_string = re.sub('-', '', extracted_additive_string)
    extracted_additive_string = re.sub(u'А', u'A', extracted_additive_string)
    extracted_additive_string = re.sub(u'Е', u'E', extracted_additive_string)
    return extracted_additive_string.encode('ascii', 'ignore')


def unescape_html_special_entities_case_insensitive(s):
    name2codepoint = htmlentitydefs.name2codepoint
    name2codepoint_case_insensitive = htmlentitydefs.name2codepoint
    name2codepoint_case_insensitive.update(
            {name.upper(): name2codepoint[name] for name in name2codepoint})
    htmlentitydefs.name2codepoint = name2codepoint_case_insensitive

    unescaped_str = HTMLParser().unescape(s)

    htmlentitydefs.name2codepoint = name2codepoint

    return unescaped_str
