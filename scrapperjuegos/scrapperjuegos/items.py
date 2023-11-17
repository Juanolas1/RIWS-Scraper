# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class juegosItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    developer_company = scrapy.Field()
    publisher_company = scrapy.Field()
    date_release = scrapy.Field()
    image = scrapy.Field()
    genre_type = scrapy.Field()
    score = scrapy.Field()
    pegi = scrapy.Field()
    web = scrapy.Field()




