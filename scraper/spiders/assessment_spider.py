import scrapy
import re
import json
import pprint
import csv
import requests
from scraper.items import Property
from urllib.parse import urlparse, parse_qs
from pyproj import Proj, transform

pp = pprint.PrettyPrinter()

URL = "http://qpublic9.qpublic.net/la_orleans_display.php?KEY={}"

# all spiders must subclass scrapy.Spider
# see: https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider
class AssessmentSpider(scrapy.Spider):
    name = "assessment_spider"
    f = open('parcel_ids.txt')
    start_urls = [URL.format(pid.strip()) for pid in f.readlines()]

    def get_address_location(self, parcel_map_link):
        """
        Parses the parcel map link and calculates coordinates from the extent.
        An example link looks like this:
        http://qpublic9.qpublic.net/qpmap4/map.php?county=la_orleans&parcel=41050873&extent=3667340+524208+3667804+524540&layers=parcels+aerials+roads+lakes
        """
        o = urlparse(parcel_map_link)
        query = parse_qs(o.query)
        bbox = query['extent'][0].split(' ')
        x1, y1, x2, y2 = [float(pt) for pt in bbox]
        # get the midpoint of the extent
        midpoint = [(x1 + x2) / 2, (y1 + y2) / 2]
        # transform projected coordinates to latitude and longitude
        in_proj = Proj(init='epsg:3452', preserve_units=True)
        out_proj = Proj(init='epsg:4326')
        return transform(in_proj, out_proj, midpoint[0], midpoint[1])

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
        # get href to parcel map if it exists
        links = response.xpath('//td[@class="owner_value"]/a[contains(@href,"extent")]/@href')
        if len(links) > 0:
            parcel_map_link = links[0].extract()
            [lng, lat] = self.get_address_location(parcel_map_link)
            property['location'] = [lng, lat]
        else:
            print('No parcel map link for {}'.format(property_key))
        # pp.pprint(property)
        yield Property(property)
