import scrapy
import re
import json
import pprint
from scraper.items import Property
import csv
import requests

pp = pprint.PrettyPrinter()

# all spiders must subclass scrapy.Spider
# see: https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider
class AssessmentSpider(scrapy.Spider):
    name = "assessment_spider"
    start_urls = ['http://qpublic9.qpublic.net/la_orleans_display.php?KEY=2336-OCTAVIAST']

    def parse(self, response):
        # replace all br tags with newline characters
        response = response.replace(body=re.sub(r"<br\s*[\/]?>", "\n", response.body.decode('utf=8')))
        property_key = response.url.split('=')[1].replace('&','')
        self.log("Parsing property_key: " + property_key)
        # parse property info
        hdrs = [h.extract().strip() for h in response.xpath('//td[@class="owner_header"]/font/text()')]
        vals = [v.extract().strip() for v in response.xpath('//td[@class="owner_value"]/text()')]
        keys = [re.sub(r"\(|\)", "", h.lower().replace("\'","")).replace(" ", "_").strip() for h in hdrs]
        property = dict(zip(keys, vals))
        property['property_key'] = property_key
        # geocode address to get lng/lat
        resp = requests.get(
            'https://search.mapzen.com/v1/search/structured',
            params = {'api_key': 'mapzen-hfgbW3U', 'size': 1,
                      'locality': 'New Orleans', 'region': 'LA',
                      'address': property['location_address']})
        lng,lat = resp.json()['features'][0]['geometry']['coordinates']
        property['longitude'] = lng
        property['latitude'] = lat
        # pp.pprint(property)
        yield Property(property)
        # crawl to next page
        next_page = response.xpath('//td[@class="header_link"]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
