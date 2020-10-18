import scrapy

class LowesproductspiderSpider(scrapy.Spider):
	name = "lowesProductSpider"
	allowed_domains = ["lowes.com/"]
	start_urls = ["https://www.lowes.com/pl/French-door-refrigerators-Refrigerators-Appliances/4294857963"]

	def parse(self, response):
		next_page = response.xpath('//link[contains(@rel, "next")]/@href').get()

		print(next_page)

		if next_page is not None:
			yield response.follow(next_page, callback=self.parse, dont_filter=True) 



	# 	path = "//div[@class="grid-par-nested parsys"]/div[position()>0 and position()<3]/div/div//a/@href"
	#     refri_links = response.xpath(path).getall() 

	#     for link in refri_links:
	#     	print(link)

	# def parse(self, response):
	# 	pass
