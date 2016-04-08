# uscrape
Scraper to index Simple Wikipedia and Khan Academy to elasticsearch for the uServe project. For more details on uServe see https://github.com/imbenclifford/userve

## Contact
Ben - imbenclifford@gmail.com

## How to use
I have written spiders for Khan Academy and Wikipedia that will scrape the relevant fields and index them to elasticsearch.

To scrape a site and index this to elasticsearch, first look at the settings.py and make sure that the ELASTICSEARCH_TYPE is set correctly.

For example, if you are indexing Wikipedia this should read:
ELASTICSEARCH_TYPE = 'wikipedia'

If you are indexing Khan Academy, this should read:
ELASTICSEARCH_TYPE = ‘khan'

There may be a way to change this, depending on the spider, but I haven’t figured out a way to do this yet.

Then run  scrapy crawl wikipedia
or  scrapy crawl khan

This will start scraping the actual khanacademy and simple.wikipedia sites, but change the urls to the urls of your local servers.

## Scrapy
Scrapy is a tool for scraping the web. Scrapy documentation: http://doc.scrapy.org/en/0.20/
You may also find this article useful, which I used as a basis to index with scrapy: http://blog.florian-hopf.de/2014/07/scrapy-and-elasticsearch.html


If you find that you make a mistake with your index, or you index something twice, you can delete individual documents from that index. If you want to delete all documents of one type (e.g. all the wikipedia documents had the wrong url) then run the file I have provided delete_es_type.py. It is currently set to delete documents of type ‘wikipedia’, but you can go in and change this to ‘khan’.
