# -*- coding: utf-8 -*-
import unittest


from goodsmatrix.string_postprocessor import parse_esl, postprocess_extracted_property_string


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


class TestExtractedStringPostprocessing(unittest.TestCase):
    def test_one_line_word(self):
        self.assertEqual(
            postprocess_extracted_property_string("word"),
            "word"
        )
    def test_two_lines(self):
        two_lines_string = (
"""hoho
hihi"""
)

        self.assertEqual(
            postprocess_extracted_property_string(two_lines_string),
            "hoho hihi"
        )

    def test_one_line_is_stripped(self):
        self.assertEqual(
            postprocess_extracted_property_string("   word   "),
            "word"
        )


if __name__ == "__main__":
    unittest.main()
