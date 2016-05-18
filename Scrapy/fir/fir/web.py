import scrapy
from scrapy.spiders import CrawlSpider, Rule
from items import FirItem

class firSpider(CrawlSpider):
    name = "fir"
    allowed_domains = ["jobbole.com"]
    start_urls = [
        "http://group.jobbole.com/16718/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = FirItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            yield item