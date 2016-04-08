from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from userve.items import UserveItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import html2text
import scrapy

class KhanSpider(CrawlSpider):
    name = "khan"
    allowed_domains = ["khanacademy.org"]
    start_urls = [
        "https://www.khanacademy.org/"
    ]

    rules = [
            Rule(SgmlLinkExtractor(allow = ['/math/']), callback='parse_item', follow = True),
            Rule(SgmlLinkExtractor(allow = ['/science/']), callback='parse_item', follow=True),
            Rule(SgmlLinkExtractor(allow = ['/economics-finance-domain/']), callback='parse_item', follow=True),
            Rule(SgmlLinkExtractor(allow = ['/humanities/']), callback='parse_item', follow=True),
            Rule(SgmlLinkExtractor(allow = ['/computing/']), callback='parse_item', follow=True),
            Rule(SgmlLinkExtractor(allow = ['/test-prep/']), callback='parse_item', follow=True),
            Rule(SgmlLinkExtractor(allow = ['/partner-content/']), callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        responseSelector = Selector(response)
        item = UserveItem()
        title = responseSelector.xpath('//title/text()').extract()[0]
        if title.endswith(' | Khan Academy'):
            title = title[:-15]
        item['title'] = title
        summary = responseSelector.xpath('//meta[@name="description"]/@content').extract()[0]
        item['summary'] = summary
        item['article'] = summary
        url = response.url
        url = url.replace("https://www.khanacademy.org/","http://localhost:8008/learn/khan/")
        item['url'] = url
        if summary == ' ' or summary == '' or summary == '\n':
            yield "no summary"
        else:
            yield item
