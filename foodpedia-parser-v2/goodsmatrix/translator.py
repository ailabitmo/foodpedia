import requests
from scrapy import log


YANDEX_TRANSLATE_API_URI = r"https://translate.yandex.net/api/v1.5/tr.json/translate"


class BadKeyException(Exception):
    pass


class YandexTranslator(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def translate_ru_to_en(self, ru_str):
        request_payload = {
            'key': self.api_key,
            'text': ru_str,
            'lang': 'ru-en',
        }
        r = requests.get(YANDEX_TRANSLATE_API_URI, params=request_payload)
        #TODO: add tests and error handling
        status_code = r.status_code
        if status_code == 200:
            return ' '.join(r.json()['text'])
        if status_code in (401, 402, 403, 404):
            raise BadKeyException(r.text)
