import scrapy
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://example.com']  # Replace with your target URL

    def parse(self, response):
        # Add your parsing logic here
        pass

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()