# -*- coding: utf-8 -*-
import lxml
import re
import htmlentitydefs
from HTMLParser import HTMLParser
import string
import fileinput


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
    found_additives_list = re.findall(ur"\b([ЕE]-?\s?\d\d\d\w?)\b", string, flags=re.IGNORECASE|re.UNICODE)
    return list(convert_to_asci_without_unnecessary_characters(additive) for additive in found_additives_list)


def convert_to_asci_without_unnecessary_characters(extracted_additive_string):
    REPLACEMENT_DICT = {
        ' ': '',
        '-': '',
        u'Е': u'E',
        u'С': u'c',
        u'А': u'a',
    }
    pattern = re.compile('|'.join(REPLACEMENT_DICT.keys()))
    result = pattern.sub(lambda x: REPLACEMENT_DICT[x.group()], extracted_additive_string)
    result = lowercase_last_character(result)
    return result.encode('ascii', 'ignore')


def lowercase_last_character(s):
    return s[:-1] + s[-1].lower()


def unescape_html_special_entities_case_insensitive(s):
    name2codepoint = htmlentitydefs.name2codepoint
    name2codepoint_case_insensitive = htmlentitydefs.name2codepoint
    name2codepoint_case_insensitive.update(
            {name.upper(): name2codepoint[name] for name in name2codepoint})
    htmlentitydefs.name2codepoint = name2codepoint_case_insensitive

    unescaped_str = HTMLParser().unescape(s)

    htmlentitydefs.name2codepoint = name2codepoint

    return unescaped_str


def remove_substring_in_paranthesis(s):
    return re.sub(r'\([^)]*\)', '', s)


def remove_weight(ingredients_as_string):
    return re.sub(r'\s*-\s*\d.*', '', ingredients_as_string)


def remove_percents(ingredients_as_string):
    return re.sub(r'\d\d?\d?\s*\%', '', ingredients_as_string)


def split_ingredients(s):
    s = s.strip()
    delimeters = '.,!?;'
    if s:
        fragments = [fragment.strip().lower()
                     for fragment
                     in split_by_list_of_delemiters(s, delimeters)]
        fragments_without_blanks = [fragment for fragment in fragments if fragment]
        return fragments_without_blanks
    else:
        return []

def split_by_list_of_delemiters(s, delimeters=string.punctuation):
    if delimeters:
        delimeters_regexp = '[{0}]+'.format(
            '|'.join('\\{0}'.format(d) for d in delimeters))
        return re.split(delimeters_regexp, s, flags=re.IGNORECASE|re.UNICODE)
    else:
        return [s]


def replace_in_file(filepath, old, new):
    for line in fileinput.input(filepath, inplace=True):
        print line.replace(old, new),


def escape_special_chars_in_sparq_query_unicode(s):
    return re.sub(r'([\.\\\+\*\?\[\^\]\$\(\)\{\}\!\<\>\|\:\-])', r'\\\\\1', s)


if __name__ == "__main__":
    replace_in_file("/tmp/tmpT2HJCp/agrovoc_2014-07-23_lod.nt", r"exactMatch >", r"exactMatch>")
