import scrapy
import json
import re
import sys
import logging
from scrapy_splash import SplashRequest
from ..items import RefrigeratorItem

class LowesproductspiderSpider(scrapy.Spider):
	""" 
		A scrapy spider used to carwl refrigerators on Lowe's.com

		Attributes:
			name : str
				The spider name
			allowed_domains : list
				The allowed domains
			start_urls : list
				List of urls of differentt kinds of regrigerators
	"""

	name = "lowesProductSpider"
	allowed_domains = ["lowes.com"] 
	start_urls = ["https://www.lowes.com/pl/French-door-refrigerators-Refrigerators-Appliances/4294857963",
				  "https://www.lowes.com/pl/Top-freezer-refrigerators-Refrigerators-Appliances/4294789497",
				  "https://www.lowes.com/pl/Bottom-freezer-refrigerators-Refrigerators-Appliances/4294789499",
				  "https://www.lowes.com/pl/Mini-fridges-Refrigerators-Appliances/290928573",
				  "https://www.lowes.com/pl/Counter-depth--Refrigerators-Appliances/4294857973?&refinement=2032108662"
				  "https://www.lowes.com/pl/Side-by-side-refrigerators-Refrigerators-Appliances/4294857970",
				  "https://www.lowes.com/pl/Freezerless-refrigerators-Refrigerators-Appliances/4294788929"]

	def start_requests(self):
		""" Performs an initial request using splash """
		for url in self.start_urls:
			yield SplashRequest(url, callback=self.parse)

	def parse(self, response):
		""" Given a initial response(search page for a kind of product), searches and extracts products from the page

			Arguments:
				response: Response object
					Page with a list of products

			Method:
				Get all product from the page
				For every product, extract informations
				if a next page exists, got there

			Returns:
				Yields a product
		"""

		products_list = self.get_products_urls(response)
		
		if products_list is not None:
			base_url = "https://www.lowes.com"
			for product in products_list:
				url = base_url + product
				yield SplashRequest(url=url, callback=self.parse_product, meta={'cnt':0})

		next_page = response.xpath('//link[contains(@rel, "next")]/@href').get()

		if next_page is not None:
			yield SplashRequest(next_page, callback=self.parse, dont_filter=True)


	def parse_product(self, response):
		"""	Given a product page, tries to find the product description.
			If not found, tries again with a new request

			Arguments:
				response: Reponse Object
					Page with a product description

			Returns:
				if found, yields a refrierator object
				if not, returns None
		"""
		try:
			data = get_page_json(response, '//script[contains(.,"productDetails")]')

			if data is not None:
				refrigerator = parse_product_json(data, response)
				prod_id = data["productId"] 

				yield refrigerator

			else:
				yield None

		except Exception:
			cnt = response.meta['cnt'] + 1

			refrigerator = page_regex(response.text, response.url)

			if refrigerator:
				yield refrigerator
				return None

			if cnt <= 3:
				yield SplashRequest(response.url, callback=self.parse_product, meta={'cnt':cnt}, dont_filter=True)
			else:
				yield None

	def get_products_urls(self, response):
		""" Search for the products urls inside a scrapy Response object 
			
			Returns:
				A list of products urls
		"""
		expression = "//script[contains(.,'pdURL')]"
		data = get_page_json(response, expression)

		if data:
			products_urls = list()
			for prod in data['itemList']:
				url = prod['product']['pdURL']
				products_urls.append(url)

			return products_urls
	
		else:
			return None

def get_page_json(response, expression):
	""" Given a response object and a regex expression, 
		searches for the expression in the response.

		Arguments:
			reponse: Response Object
				A product page reponse object 
			expression : string
				The expression to be found in the page
		Returns:
			If the expression is matched, returns the correponsing json
			If not, returns none 

	"""

	data = response.xpath(expression).extract()

	if len(data) == 0:
		return None
	else:
		data = data[0]
		data = data.replace('<script charset="UTF-8">window.__PRELOADED_STATE__ =', '')
		data = data.replace('</script>', '')

		return json.loads(data)


def parse_product_json(product_json, response=None):
	""" Given a json holding product details, try to parse the information to a RefrigeratorItem
		If a field it's missing, tries to found it on the page html 
	"""

	refrigerator = RefrigeratorItem()

	prod_id = product_json["productId"] 
			
	refrigerator['prod_id'] = prod_id
	refrigerator['url'] = product_json['productDetails'][prod_id]['product']['pdURL']
	refrigerator['description'] = product_json['productDetails'][prod_id]['product']['description']
	refrigerator['title'] = product_json['productDetails'][prod_id]['product']['title']
	refrigerator['item'] = product_json['productDetails'][prod_id]['product']['itemNumber']
	refrigerator['model'] = product_json['productDetails'][prod_id]['product']['modelId']
	refrigerator['old_value'] = -1
	refrigerator['sale'] = False
	# refrigerator['specifications'] = product_json['productDetails'][prod_id]['product']['specs']

	if 'price' in product_json['productDetails'][prod_id]:
		price = product_json['productDetails'][prod_id]['price']
		
		if price is not None and 'itemPrice' in product_json['productDetails'][prod_id]['price']:
			refrigerator['price'] = product_json['productDetails'][prod_id]['price']['itemPrice']
		else:
			refrigerator['price'] = -1

		if price is not None and 'wasPrice' in product_json['productDetails'][prod_id]['price']:
			refrigerator['sale'] = True
			refrigerator['old_value'] = int(product_json['productDetails'][prod_id]['price']['wasPrice'])

	elif response:
		refrigerator['price'] = int(response.xpath("//span[@class='aPrice large']/span/text()").extract()[0])


	return refrigerator

def page_regex(page_source, url=None):
	""" Given a page html, tries to find a product.

		In a last resort, tries to find information that has not been properly
		 loaded inside the page html.

		If not found, raises an error msg pointing the fault url.
	"""

	content = re.search('{"productDetails":.+?()"pd"}', page_source)
	
	if content:
		data = content.group(0)
		product_json = json.loads(data)

		refrigerator = parse_product_json(product_json)

		return refrigerator
	
	else:
		msg = "Error: " + url
		logging.debug(msg)
		
		return None
