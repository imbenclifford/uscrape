from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from userve.items import UserveItem
from os import listdir
from os.path import isfile, join
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import html2text
import scrapy

class WikipediaSpider(CrawlSpider):
    name = "wikipedia"
    allowed_domains = ["wikipedia.org"]
    start_urls = [
        "https://simple.wikipedia.org/wiki/Main_Page"
    ]
    rules = [
            Rule(SgmlLinkExtractor(allow = ['simple.wikipedia.org/wiki/']), callback='parse_item', follow = True)
    ]

    def parse_item(self, response):
        print "url: " + response.url
        responseSelector = Selector(response)
        body = responseSelector.css('div#content')
        item = UserveItem()
        item['title'] = body.css('h1#firstHeading::text').extract()
        url = response.url
        url = url.replace("https://","http://localhost:8007/") + ".html"
        item['url'] = url

        summary = body.css('div#mw-content-text > p:first-of-type').extract()
        article = responseSelector.css("div#mw-content-text").extract()

        converter = html2text.HTML2Text()
        converter.ignore_links = True

        if summary and article:
            item['summary'] = converter.handle(summary[0])
            item['article'] = converter.handle(article[0])
            yield item
        else:
            print "either no summary or no article"
