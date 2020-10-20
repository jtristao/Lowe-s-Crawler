import scrapy
import json
from scrapy_splash import SplashRequest

class LowesproductspiderSpider(scrapy.Spider):
	""" 
		A scrapy spider used to carwl refrigerators on Lowe's.com

		Attributes:
			name : str
				The spider name
			allowed_domains : list
				The allowed domains
			start_urls : list
				List of urls to starting scraping from
	"""

	name = "lowesProductSpider"
	allowed_domains = ["lowes.com/"]
	start_urls = ["https://www.lowes.com/pl/French-door-refrigerators-Refrigerators-Appliances/4294857963"]

	def start_requests(self):
		""" Performs an initial request using splash """

		yield SplashRequest(url="https://www.lowes.com/pl/French-door-refrigerators-Refrigerators-Appliances/4294857963", callback=self.parse)
	
	def parse(self, response):
		products_list = self.get_products_urls(response)
		
		print(products_list)

		next_page = response.xpath('//link[contains(@rel, "next")]/@href').get()

		# if next_page is not None:
			# yield SplashRequest(next_page, callback=self.parse, dont_filter=True)


	def get_products_urls(self, response):
		""" Search for the products urls inside a scrapy Response object 
			
			Returns:
				A list of urls
		"""

		data = response.xpath('//script[contains(.,"pdURL")]').extract()[0]

		data = data.replace('<script charset="UTF-8">window.__PRELOADED_STATE__ =', '')
		data = data.replace('</script>', '')

		data_obj = json.loads(data)

		products_urls = list()
		for prod in data_obj['itemList']:
			url = prod['product']['pdURL']
			products_urls.append(url)

		return products_urls
	