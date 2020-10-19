import scrapy
from scrapy_splash import SplashRequest

class LowesproductspiderSpider(scrapy.Spider):
	name = "lowesProductSpider"
	allowed_domains = ["lowes.com/"]
	start_urls = ["https://www.lowes.com/pl/French-door-refrigerators-Refrigerators-Appliances/4294857963"]

	def start_requests(self):
		yield SplashRequest(url="https://www.lowes.com/pl/French-door-refrigerators-Refrigerators-Appliances/4294857963", callback=self.parse)

	def parse(self, response):
		next_page = response.xpath('//link[contains(@rel, "next")]/@href').get()

		print(next_page.text)


		# if next_page is not None:
			# yield SplashRequest(next_page, callback=self.parse, dont_filter=True)