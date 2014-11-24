import unittest

from goodsmatrix.esl_parser import parse_esl


class TestEslParser(unittest.TestCase):
    def test_signle_protein(self):
        actual_esl_dict = parse_esl("Белки: 7,90 г")
        self.assertEqual({'proteins': 7.90}, actual_esl_dict)

    def test_protein_in_lower_case(self):
        actual_esl_dict = parse_esl("белки:  7,90 г")
        self.assertEqual({'proteins': 7.90}, actual_esl_dict)

    def test_protein_no_measuarment(self):
        actual_esl_dict = parse_esl("белки:  7,90")
        self.assertEqual({'proteins': 7.90}, actual_esl_dict)

    def test_protein_no_spaces(self):
        actual_esl_dict = parse_esl("белки:7,90 г")
        self.assertEqual({'proteins': 7.90}, actual_esl_dict)

    def test_protein_doubled_spaces(self):
        actual_esl_dict = parse_esl("белки  :  7,90  г")
        self.assertEqual({'proteins': 7.90}, actual_esl_dict)

    def test_empty_string(self):
        actual_esl_dict = parse_esl("")
        self.assertEqual(dict(), actual_esl_dict)

    def test_point_in_number(self):
        actual_esl_dict = parse_esl("Белки:  7.90 г")
        self.assertEqual({'proteins': 7.90}, actual_esl_dict)

    def test_started_with_spaces(self):
        actual_esl_dict = parse_esl("   Белки:  7.90 г")
        self.assertEqual({'proteins': 7.90}, actual_esl_dict)

    def test_number_is_missed(self):
        actual_esl_dict = parse_esl("Белки:  г")
        self.assertEqual(dict(), actual_esl_dict)

    def test_trailing_dot(self):
        actual_esl_dict = parse_esl("Белки:  7,90 г.")
        self.assertEqual({'proteins': 7.90}, actual_esl_dict)


if __name__ == "__main__":
    unittest.main()
