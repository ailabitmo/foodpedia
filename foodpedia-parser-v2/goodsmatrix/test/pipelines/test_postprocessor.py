from unittest import TestCase
from mock import patch

from goodsmatrix.pipelines.postprocessors import ExtractEsl
from goodsmatrix.pipelines.postprocessors import ExtractEAdditives
from goodsmatrix.pipelines.postprocessors import StripMultilineStringProperties
from goodsmatrix.pipelines.postprocessors import UnescapeSpecialHTMLEntities


class TestExtractEsl(TestCase):
    def setUp(self):
        self.pipeline = ExtractEsl()

    @patch('goodsmatrix.string_processor.parse_esl')
    def test_process_item_with_esl(self, mock_parsed_esl_dict):
        mock_parsed_esl_dict.return_value = {
                'proteins_as_double': 7.50,
                'carbohydrates_as_double': 3.0,
                'calories_as_double': 263.0
            }
        good_item = self.pipeline.process_item({'esl_as_string': 'mocked_value'}, None)

        self.assertTrue(mock_parsed_esl_dict.called)
        self.assertEqual(good_item['proteins_as_double'], 7.50)
        self.assertEqual(good_item['carbohydrates_as_double'], 3.0)
        self.assertEqual(good_item['calories_as_double'], 263.0)
        self.assertNotIn('fats_as_double', good_item)

    @patch('goodsmatrix.string_processor.parse_esl')
    def test_process_item_without_esl(self, mock_parsed_esl_dict):
        good_item = self.pipeline.process_item(dict(), None)

        self.assertFalse(mock_parsed_esl_dict.called)
        self.assertEqual(good_item, dict())


class TestExtractEAdditives(TestCase):
    def setUp(self):
        self.pipeline = ExtractEAdditives()

    @patch('goodsmatrix.string_processor.parse_e_additives')
    def test_process_item_with_ingridients_as_string(self, mock_parsed_e_additives):
        mock_parsed_e_additives.return_value = [u'E201', u'E202']
        good_item = self.pipeline.process_item({'ingredients': 'mocked_value'}, None)

        self.assertTrue(mock_parsed_e_additives.called)
        self.assertEqual(good_item['e_additives'], [u'E201', u'E202'])

    @patch('goodsmatrix.string_processor.parse_e_additives')
    def test_process_item_with_ingridients_as_string_without_eadditives(self, mock_parsed_e_additives):
        mock_parsed_e_additives.return_value = []
        good_item = self.pipeline.process_item({'ingredients': 'mocked_value'}, None)

        self.assertTrue(mock_parsed_e_additives.called)
        self.assertEqual(good_item['e_additives'], [])

    @patch('goodsmatrix.string_processor.parse_e_additives')
    def test_process_item_without_ingridients(self, mock_parsed_e_additives):
        good_item = self.pipeline.process_item(dict(), None)

        self.assertFalse(mock_parsed_e_additives.called)
        self.assertEqual(good_item, dict())


class TestStripMultilineProperties(TestCase):
    def setUp(self):
        self.pipeline = StripMultilineStringProperties()

    @patch('goodsmatrix.string_processor.strip_multiline')
    def test_process_item_with_string(self, mock_stripped_multiline):
        mock_stripped_multiline.return_value = 'abcdef'
        good_item = self.pipeline.process_item({'comment': 'mocked_value'}, None)

        self.assertTrue(mock_stripped_multiline.called)
        self.assertEqual(good_item, {'comment': 'abcdef'})

    @patch('goodsmatrix.string_processor.strip_multiline')
    def test_process_item_without_string(self, mock_stripped_multiline):
        mock_stripped_multiline.side_effect = AttributeError()
        good_item = self.pipeline.process_item({'proteins_as_double': 0.0, 'e_additives': [u'E100']}, None)

        self.assertTrue(mock_stripped_multiline.called)
        self.assertEqual(good_item, {'proteins_as_double': 0.0, 'e_additives': [u'E100']})


class TestUnescapeSpecialHTMLEntities(TestCase):
    def setUp(self):
        self.pipeline = UnescapeSpecialHTMLEntities()

    @patch('goodsmatrix.string_processor.unescape_html_special_entities_case_insensitive')
    def test_process_item_with_special_html_entity(self, mock_unescaped_string):
        mock_unescaped_string.return_value = '&quote;'

        good_item = self.pipeline.process_item({'name': 'mocked_value'}, None)

        self.assertTrue(mock_unescaped_string.called)
        self.assertEqual(good_item, {'name': '&quote;'})

    @patch('goodsmatrix.string_processor.unescape_html_special_entities_case_insensitive')
    def test_process_item_with_special_html_entity(self, mock_unescaped_string):
        mock_unescaped_string.side_effect = TypeError()

        good_item = self.pipeline.process_item({'proteins_as_double': 0.0, 'e_additives': [u'E100']}, None)

        self.assertTrue(mock_unescaped_string.called)
        self.assertEqual(good_item, {'proteins_as_double': 0.0, 'e_additives': [u'E100']})
