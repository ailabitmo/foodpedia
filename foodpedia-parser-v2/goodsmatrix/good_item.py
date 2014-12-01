import scrapy

class GoodItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    barcode = scrapy.Field()
    best_before = scrapy.Field()
    comment = scrapy.Field()
    ingredients = scrapy.Field()
    netto_weight = scrapy.Field()
    standart = scrapy.Field()
    store_conditions = scrapy.Field()
    esl = scrapy.Field()
    pack_type = scrapy.Field()
    proteins_as_double = scrapy.Field()
    fats_as_double = scrapy.Field()
    carbohydrates_as_double = scrapy.Field()
    calories_as_double = scrapy.Field()
