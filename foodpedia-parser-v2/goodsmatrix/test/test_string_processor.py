# -*- coding: utf-8 -*-
import unittest


from goodsmatrix.string_processor import parse_esl, strip_multiline, parse_e_additives
from goodsmatrix.string_processor import unescape_html_special_entities_case_insensitive
from goodsmatrix.string_processor import lowercase_last_character
from goodsmatrix.string_processor import split_ingredients
from goodsmatrix.string_processor import split_by_list_of_delemiters
from goodsmatrix.string_processor import remove_substring_in_paranthesis
from goodsmatrix.string_processor import remove_weight
from goodsmatrix.string_processor import remove_percents


class TestEslParser(unittest.TestCase):
    def test_signle_protein(self):
        self.assertEqual(parse_esl(u"Белки: 1,23 г"), {'proteins_as_double': 1.23})

    def test_fats_in_lower_case(self):
        self.assertEqual(parse_esl(u"жиры: 4,56 г"), {'fats_as_double': 4.56})

    def test_carbohydrates_no_measuarment(self):
        self.assertEqual(parse_esl(u"Углеводы: 8,90"), {'carbohydrates_as_double': 8.90})

    def test_point_in_number(self):
        self.assertEqual(parse_esl(u"Энергетическая ценность: 123.0 г"), {'calories_as_double': 123.0})

    def test_protein_no_spaces(self):
        self.assertEqual(parse_esl(u"Белки:7,90г"), {'proteins_as_double': 7.90})

    def test_fats_doubled_spaces(self):
        self.assertEqual(parse_esl(u"Жиры  :  1,2  г"), {'fats_as_double': 1.2})

    def test_empty_string(self):
        self.assertEqual(parse_esl(u""), dict())

    def test_started_with_spaces(self):
        self.assertEqual(parse_esl(u"   Углеводы: 8 г"), {'carbohydrates_as_double': 8.0})

    def test_number_is_missed(self):
        self.assertEqual(parse_esl(u"Энергетическая ценность г"), dict())

    def test_trailing_dot(self):
        self.assertEqual(parse_esl(u"Белки: 7.0 г."), {'proteins_as_double': 7.0})

    def test_proteins_and_fats_together(self):
        self.assertEqual(parse_esl(u"Жиры: 1,7 белки :  5 г."), {'proteins_as_double': 5.0, 'fats_as_double': 1.7})

    def test_carbohydrates_and_calories_together(self):
        self.assertEqual(
            parse_esl(u"  углеводы: 3 ; Энергетическая ценность : 1000 ккал"),
            {'carbohydrates_as_double': 3.0, 'calories_as_double': 1000})

    def test_all_esl_together(self):
        self.assertEqual(
            parse_esl(u"Белки:  7,50 г Жиры:  2,90 г Углеводы:  3,00 г Энергетическая ценность:  263,00 ккал"),
            {'proteins_as_double': 7.50, 'fats_as_double': 2.9, 'carbohydrates_as_double': 3.0, 'calories_as_double': 263.0})

    def test_the_not_greater_special_word_matches_and_is_skipped(self):
        self.assertEqual(parse_esl(u"Жиры: не более 11,50 г"), {'fats_as_double': 11.5})

    def test_the_greater_special_word_does_not_match(self):
        self.assertEqual(parse_esl(u"Жиры: более 11,50 г"), dict())

    def test_the_not_less_special_word_matches_and_is_skipped(self):
        self.assertEqual(parse_esl(u"Белки: не менее 19,00 г "), {'proteins_as_double': 19.0})

    def test_the_less_special_word_does_not_match(self):
        self.assertEqual(parse_esl(u"Белки: менее 19,00 г "), dict())


class TestStripMutlilineString(unittest.TestCase):
    def test_one_line_word(self):
        self.assertEqual(
            strip_multiline("word"),
            "word"
        )

    def test_two_lines_are_converted_to_single_line(self):
        two_lines_string = (
"""hoho
hihi"""
)

        self.assertEqual(
            strip_multiline(two_lines_string),
            "hoho hihi"
        )

    def test_one_line_is_stripped(self):
        self.assertEqual(
            strip_multiline("   word   "),
            "word"
        )

    def test_two_lines_with_spaces_are_stripped(self):
        two_lines_string = (
"""    hoho
hihi    """
)

        self.assertEqual(
            strip_multiline(two_lines_string),
            "hoho hihi"
        )


    def test_attribute_error_for_double(self):
        self.assertRaises(AttributeError, strip_multiline, 10.0)

    def test_attribute_error_for_list(self):
        self.assertRaises(AttributeError, strip_multiline, [u'E201', u'E202'])

    def test_empty_string(self):
        self.assertEqual(strip_multiline(""), "")


class TestParseEAdditives(unittest.TestCase):
    def test_one_additive_in_lowercase(self):
        self.assertEqual(parse_e_additives(u"е100"), [u'E100'])

    def test_one_additive_in_uppercase(self):
        self.assertEqual(parse_e_additives(u"Е200"), [u'E200'])

    def test_two_additives_in_lower_and_upper_cases(self):
        self.assertEqual(parse_e_additives(u"е201, Е202"), [u'E201', u'E202'])

    def test_no_additives(self):
        self.assertEqual(parse_e_additives(u"a303"), [])

    def test_no_additives_if_additive_is_not_separate_word(self):
        self.assertEqual(parse_e_additives(u"abce304"), [])

    def test_additive_with_extra_letter(self):
        self.assertEqual(parse_e_additives(u"е201B"), [u'E201b'])

    def test_additive_with_extra_digit(self):
        self.assertEqual(parse_e_additives(u"Е1525"), [u'E1525'])

    def test_additive_with_hyphen(self):
        self.assertEqual(parse_e_additives(u"е-100"), [u'E100'])

    # Е160А is parsed as Е160 #18
    def test_additive_tailing_russian_A(self):
        string_under_test = (
            u"сахар, сироп глюкозы, вода, желатин, ароматические "
            u"вещества, кислота(лимонная), порошок лакриц, "
            u"красители (Е100,Е120,Е133,Е153, Е160А), вещества "
            u"наносимые на поверхность(растительные масла, Е903). "
            u"Возможно незначительное содержание лесного ореха.")
        self.assertEqual(parse_e_additives(string_under_test), [u'E100', u'E120', u'E133', u'E153', u'E160a', u'E903'])

    def test_additive_russian_tailing_russian_a_in_lowercase(self):
        string_under_test = u"Е160а"
        self.assertEqual(parse_e_additives(string_under_test), [u'E160a'])

    def test_additive_russian_tailing_russian_E_in_uppercase(self):
        string_under_test = u"Е160Е"
        self.assertEqual(parse_e_additives(string_under_test), [u'E160e'])

    def test_additive_russian_tailing_russian_e_in_lowercase(self):
        string_under_test = u"E160е"
        self.assertEqual(parse_e_additives(string_under_test), [u'E160e'])

    def test_additive_russian_tailing_russian_C_in_uppercase(self):
        string_under_test = u"Е160С"
        self.assertEqual(parse_e_additives(string_under_test), [u'E160c'])

    def test_additive_russian_tailing_russian_c_in_lowercase(self):
        string_under_test = u"E160с"
        self.assertEqual(parse_e_additives(string_under_test), [u'E160c'])

    def test_additive_russian_leading_russian_E_in_uppercase(self):
        string_under_test = u"Е160"
        self.assertEqual(parse_e_additives(string_under_test), [u'E160'])

    def test_additive_russian_leading_russian_E_in_lowercase(self):
        string_under_test = u"е160"
        self.assertEqual(parse_e_additives(string_under_test), [u'E160'])

    def test_additive_tailing_russian_non_latin_character_is_ignored(self):
        string_under_test = u"E160б"
        self.assertEqual(parse_e_additives(string_under_test), [u'E160'])

    def test_additive_with_space(self):
        string_under_test = (
            u"влагоудерживающий агент E 452, регулятор кислотности E 451, "
            u"специи, декстроза, загустители E 407, E 412; "
        )
        self.assertEqual(parse_e_additives(string_under_test), [u'E452', u'E451', u'E407', u'E412'])


class TestLowercaseLastCharacter(unittest.TestCase):
    def test_with_tailing_character(self):
        self.assertEqual(lowercase_last_character('E160F'), 'E160f')

    def test_with_tailing_number(self):
        self.assertEqual(lowercase_last_character('E1234'), 'E1234')


class TestUnescapeHTMLSpecialEntitiesCaseInsensitive(unittest.TestCase):
    def test_strip_special_character(self):
        name = u'Традиционное датское сдобное печенье &quot;BISCA&quot; ассорти 454 г'

        name_in_plain_text = unescape_html_special_entities_case_insensitive(name)

        self.assertEqual(
            name_in_plain_text,
            u'Традиционное датское сдобное печенье "BISCA" ассорти 454 г'
        )

    def test_strip_special_character_uppercase(self):
        name = u'ТРАДИЦИОННОЕ ДАТСКОЕ СДОБНОЕ ПЕЧЕНЬЕ &QUOT;BISCA&QUOT; АССОРТИ 454 Г'

        name_in_plain_text = unescape_html_special_entities_case_insensitive(name)

        self.assertEqual(
            name_in_plain_text,
            u'ТРАДИЦИОННОЕ ДАТСКОЕ СДОБНОЕ ПЕЧЕНЬЕ "BISCA" АССОРТИ 454 Г'
        )

    def test_strip_special_character_on_not_string(self):
        proteins_as_double = 12.3

        self.assertRaises(
            TypeError,
            unescape_html_special_entities_case_insensitive,
            proteins_as_double
        )


class TestSplitIngridients(unittest.TestCase):
    def test_one_element(self):
        splitted = split_ingredients(u'сахар')
        self.assertEqual(splitted, [u'сахар'])

    def test_two_comma_separated_elements(self):
        splitted = split_ingredients(u'сахар,мука')
        self.assertEqual(splitted, [u'сахар', u'мука'])

    def test_two_comma_separated_elements_with_space(self):
        splitted = split_ingredients(u'сахар, мука')
        self.assertEqual(splitted, [u'сахар', u'мука'])

    def test_lowercase(self):
        splitted = split_ingredients(u'Сахар, мука')
        self.assertEqual(splitted, [u'сахар', u'мука'])

    def test_empty_string(self):
        splitted = split_ingredients(u'')
        self.assertEqual(splitted, [])

    def test_exception_on_non_string(self):
        self.assertRaises(
            AttributeError,
            split_ingredients, 4
        )

    def test_splitted_by_dot(self):
        splitted = split_ingredients(u'Сахар. Мука')
        self.assertEqual(splitted, [u'сахар', u'мука'])

    def test_double_word_fragments(self):
        splitted = split_ingredients(u'пшеничная мука')
        self.assertEqual(splitted, [u'пшеничная мука'])

    def test_tralinging_space(self):
        splitted = split_ingredients(u'соль, пшеничная мука ')
        self.assertEqual(splitted, [u'соль', u'пшеничная мука'])

    def test_real_string(self):
        splitted = split_ingredients(u'Обезжиренное молоко, наполнитель ягодный - малина со злаками (овес), цельное молоко, сухое обезжиренное молоко, с использованием йогуртовой закваски. ')
        self.assertEqual(splitted, [u'обезжиренное молоко', u'наполнитель ягодный - малина со злаками (овес)', u'цельное молоко', u'сухое обезжиренное молоко', u'с использованием йогуртовой закваски'])


class TestSplitByListOfDelimeters(unittest.TestCase):
    def test_one_delimeter(self):
        splitted = split_by_list_of_delemiters('a,b,c', ',')
        self.assertEqual(splitted, ['a', 'b', 'c'])

    def test_two_delimeters(self):
        splitted = split_by_list_of_delemiters('a!b_c', '!_')
        self.assertEqual(splitted, ['a', 'b', 'c'])

    def test_no_delimeters(self):
        splitted = split_by_list_of_delemiters('a!b_c', '')
        self.assertEqual(splitted, ['a!b_c'])

    def test_empty_string(self):
        splitted = split_by_list_of_delemiters('', ',')
        self.assertEqual(splitted, [''])

    def test_no_delimeters_in_string(self):
        splitted = split_by_list_of_delemiters('a!b_c', ',')
        self.assertEqual(splitted, ['a!b_c'])

    def test_trailing_delelimeter(self):
        splitted = split_by_list_of_delemiters('a!b_c', 'c')
        self.assertEqual(splitted, ['a!b_', ''])

    def test_starting_delelimeter(self):
        splitted = split_by_list_of_delemiters('a!b_c', 'a')
        self.assertEqual(splitted, ['a!b_c'])

    def test_two_delimeters_one_by_one(self):
        splitted = split_by_list_of_delemiters('a.,c', ',.')
        self.assertEqual(splitted, ['a', 'c'])

    def test_two_same_delimeters_one_by_one(self):
        splitted = split_by_list_of_delemiters('a..c', ',.')
        self.assertEqual(splitted, ['a', 'c'])


class TestRemoveSubstingInParanthesis(unittest.TestCase):
    def test_one_paranthesis(self):
        no_substring_in_paranthesis = remove_substring_in_paranthesis("abc(ddd)")
        self.assertEqual(no_substring_in_paranthesis, "abc")

    def test_not_closed_paranthesis(self):
        no_substring_in_paranthesis = remove_substring_in_paranthesis("abc(ddd")
        self.assertEqual(no_substring_in_paranthesis, "abc(ddd")

    def test_not_oppened_paranthesis(self):
        no_substring_in_paranthesis = remove_substring_in_paranthesis("abcdd)d")
        self.assertEqual(no_substring_in_paranthesis, "abcdd)d")

    def test_brakets(self):
        no_substring_in_paranthesis = remove_substring_in_paranthesis("abc[ddd]")
        self.assertEqual(no_substring_in_paranthesis, "abc[ddd]")

    def test_nested_paranthesis(self):
        no_substring_in_paranthesis = remove_substring_in_paranthesis("abc(d(e)f)")
        self.assertEqual(no_substring_in_paranthesis, "abcf)")


class TestRemoveWeigth(unittest.TestCase):
    def test_weigth_with_mg(self):
        no_weight = remove_weight(u"кальций - 5 мг")
        self.assertEqual(no_weight, u"кальций")

    def test_weigth_no_mg(self):
        no_weight = remove_weight(u"кальций - 5")
        self.assertEqual(no_weight, u"кальций")

    def test_no_spaces(self):
        no_weight = remove_weight(u"кальций-5 мг")
        self.assertEqual(no_weight, u"кальций")


class TestRemovePercents(unittest.TestCase):
    def test_trailing_percents(self):
        no_percents = remove_percents(u"сыр 13%")
        self.assertEqual(no_percents, u"сыр ")

    def test_space_before_percent_sign(self):
        no_percents = remove_percents(u"сыр 13 %")
        self.assertEqual(no_percents, u"сыр ")



if __name__ == "__main__":
    unittest.main()
