# -*- coding: utf-8 -*-
import unittest


from goodsmatrix.esl_parser import parse_esl


class TestEslParser(unittest.TestCase):
    def test_signle_protein(self):
        self.assertEqual(parse_esl(u"Белки: 1,23 г"), {'proteins': 1.23})

    def test_fats_in_lower_case(self):
        self.assertEqual(parse_esl(u"жиры: 4,56 г"), {'fats': 4.56})

    def test_carbohydrates_no_measuarment(self):
        self.assertEqual(parse_esl(u"Углеводы: 8,90"), {'carbohydrates': 8.90})

    def test_point_in_number(self):
        self.assertEqual(parse_esl(u"Энергетическая ценность: 123.0 г"), {'calories': 123.0})

    def test_protein_no_spaces(self):
        self.assertEqual(parse_esl(u"Белки:7,90г"), {'proteins': 7.90})

    def test_fats_doubled_spaces(self):
        self.assertEqual(parse_esl(u"Жиры  :  1,2  г"), {'fats': 1.2})

    def test_empty_string(self):
        self.assertEqual(parse_esl(u""), dict())

    def test_started_with_spaces(self):
        self.assertEqual(parse_esl(u"   Углеводы: 8 г"), {'carbohydrates': 8.0})

    def test_number_is_missed(self):
        self.assertEqual(parse_esl(u"Энергетическая ценность г"), dict())

    def test_trailing_dot(self):
        self.assertEqual(parse_esl(u"Белки: 7.0 г."), {'proteins': 7.0})

    def test_proteins_and_fats_together(self):
        self.assertEqual(parse_esl(u"Жиры: 1,7 белки :  5 г."), {'proteins': 5.0, 'fats': 1.7})

    def test_carbohydrates_and_calories_together(self):
        self.assertEqual(
            parse_esl(u"  углеводы: 3 ; Энергетическая ценность : 1000 ккал"),
            {'carbohydrates': 3.0, 'calories': 1000})

    def test_all_esl_together(self):
        self.assertEqual(
            parse_esl(u"Белки:  7,50 г Жиры:  2,90 г Углеводы:  3,00 г Энергетическая ценность:  263,00 ккал"),
            {'proteins': 7.50, 'fats': 2.9, 'carbohydrates': 3.0, 'calories': 263.0})



if __name__ == "__main__":
    unittest.main()
