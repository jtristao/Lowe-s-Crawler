# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RefrigeratorItem(scrapy.Item):
	# define the fields for your item here like:
	prod_id = scrapy.Field()
	url = scrapy.Field()
	description = scrapy.Field()
	title = scrapy.Field()
	specifications = scrapy.Field()
	price = scrapy.Field()
	item = scrapy.Field()
	model = scrapy.Field()
	sale = scrapy.Field()
	old_value = scrapy.Field()


