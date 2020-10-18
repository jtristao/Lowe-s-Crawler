# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LowesItem(scrapy.Item):
    # define the fields for your item here like:
   	url = scrapy.Field()
   	title = scrapy.Field()
   	price = scrapy.Field()
   	sku = scrapy.Field()