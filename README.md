# Lowe's Crawler

A crawling project based on Lowe's website.[Birdie's Techinal Test]

I'm interested in cralwing and storing data from refrigerator's on [lowe's website](https://www.lowes.com/). To achieve that, i'm going to use scrapy with splash and docker. For every refrigerator, i'm storing its id, url, description, title, price, item number, model, if it on sale, and how much it used to cost.

The folder exmples has two files:
	* A json for product description, required by the page javascript
	* A json for product on sale description, required by the page javascript

The resulsts can be found on [refrigerators.json](refrigerators.json)


## Requirements
	
	* Scrapy==2.4.0
	* scrapy-splash==0.7.2
	* [Docker](https://docs.docker.com/get-docker/)

## Usage

1. Pull docker container 
	docker pull scrapinghub/splash

2. Run docker
	docker run -it -p 8050:8050 scrapinghub/splash --max-timeout 300

3. Run scrapy
	scrapy crawl lowesProductSpider --loglevel=INFO -O output.json

