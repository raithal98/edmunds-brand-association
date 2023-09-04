import scrapy
from scraper.items import ScraperItem
from scrapy.selector import Selector
import requests
import re
import urllib.request
from urllib.parse import urlparse
from w3lib.html import  remove_tags
import unicodedata
import datetime
from urllib.parse import urljoin
from scraper import settings
import logging
from w3lib.http import basic_auth_header
from scrapy import signals
from pydispatch import dispatcher
from scrapy.http import FormRequest
from lxml.html import fromstring
from bs4 import BeautifulSoup


class scraper(scrapy.Spider):
    name="scraper"
    allowed_domains = ["forums.edmunds.com"]
    
    PROJECT_ROOT=settings.PROJECT_ROOT

    def start_requests(self):
        urllist=[]
        pages= range(7,107)
        for i in pages:
            urllist.append('https://forums.edmunds.com/discussion/2864/general/x/entry-level-luxury-performance-sedans/p{}'.format(i))
        
        for i in urllist:
            yield scrapy.Request(i, callback=self.parse)


    def parse(self, response):
        hxs = Selector(response)
        for quote in hxs.xpath('//div[@class="Comment"]'):
            bodies = BeautifulSoup(' '.join(quote.xpath('.//div[@class="Message userContent"]//text()').extract()))
            bodies = bodies.get_text().strip()
            dates= quote.xpath('.//div//time/@title').extract_first()
            dates=' '.join(dates.split(' ')[:-1])
            authors= quote.xpath('.//div//span[@class="Author"]//@title').extract_first()
            item= ScraperItem()
            item["author"]=authors
            item["body"]=bodies
            item["dates"]=dates
            yield item
        
            