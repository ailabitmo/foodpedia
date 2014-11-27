# -*- coding: utf-8 -*-
import unittest


from goodsmatrix.esl_parser import parse_esl


class TestEslParser(unittest.TestCase):
    def test_signle_protein(self):
        self.assertEqual(parse_esl(u"Белки: 7,90 г"), {'proteins': 7.90})

    def test_protein_in_lower_case(self):
        self.assertEqual(parse_esl(u"белки: 7,90 г"), {'proteins': 7.90})

    def test_protein_no_measuarment(self):
        self.assertEqual(parse_esl(u"Белки: 7,90"), {'proteins': 7.90})

    def test_protein_no_spaces(self):
        self.assertEqual(parse_esl(u"Белки:7,90 г"), {'proteins': 7.90})

    def test_protein_doubled_spaces(self):
        self.assertEqual(parse_esl(u"Белки  :  7,90  г"), {'proteins': 7.90})

    def test_empty_string(self):
        self.assertEqual(parse_esl(u""), dict())

    def test_point_in_number(self):
        self.assertEqual(parse_esl(u"Белки: 7.90 г"), {'proteins': 7.90})

    def test_started_with_spaces(self):
        self.assertEqual(parse_esl(u"   Белки: 7.90 г"), {'proteins': 7.90})

    def test_number_is_missed(self):
        self.assertEqual(parse_esl(u"Белки: г"), dict())

    def test_trailing_dot(self):
        self.assertEqual(parse_esl(u"Белки: 7,90 г."), {'proteins': 7.90})

    def test_complete(self):
        self.assertEqual(
            parse_esl(u"Белки:  7,50 г Жиры:  2,90 г Углеводы:  3,00 г Энергетическая ценность:  263,00 ккал: 7,90 г."),
            {'proteins': 7.50, 'fats': 2.9, 'carbohydrates': 3.0, 'calories': 263.0})



if __name__ == "__main__":
    unittest.main()
