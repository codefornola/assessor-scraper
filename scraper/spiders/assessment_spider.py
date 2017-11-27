# -*- coding: utf-8 -*-

import logging
import pprint
import re
import os 
from urllib.parse import urlparse, parse_qs

import requests
import scrapy
from pyproj import Proj, transform

from scraper.items import Property

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
pp = pprint.PrettyPrinter()

URL = "http://qpublic9.qpublic.net/la_orleans_display.php?KEY={}"


class AssessmentSpider(scrapy.Spider):
    """
    All spiders must subclass scrapy.Spider
    https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider
    """
    name = "assessment_spider"
    f = open('parcel_ids.txt')
    start_urls = [URL.format(pid.strip()) for pid in f.readlines()]

    def parse(self, response):
        """
        Default callback function with response for the crawled url
        https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.Spider.parse
        """
        response = response.replace(body=re.sub(r"<br\s*[\/]?>", "\n", response.body.decode('utf=8')))
        property_key = response.url.split('=')[1].replace('&', '')
        # logging.debug("Parsing property_key: %s", property_key)
        property_info = self.parse_property_info(response)
        property_values = self.parse_property_values(response)
        property_sales = self.parse_property_sales(response)
        property_info['property_key'] = property_key
        property_info['sales'] = property_sales
        property_info['values'] = property_values
        yield Property(property_info)

    @staticmethod
    def get_address_location(parcel_map_link):
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

    @staticmethod
    def geocode_address(address):
        if 'MAPZEN_API_KEY' in os.environ:
            MAPZEN_API_KEY = os.environ['MAPZEN_API_KEY']
            resp = requests.get(
                'https://search.mapzen.com/v1/search/structured',
                params={'api_key': MAPZEN_API_KEY, 'size': 1,
                        'locality': 'New Orleans', 'region': 'LA',
                        'address': address})
            res = resp.json()
            if res['features'][0]['properties']['match_type'] == 'fallback':
                logging.warning("Could not get coordinates for " + address)
                return
            else:
                lng, lat = res['features'][0]['geometry']['coordinates']
                return [lng, lat]

    def parse_property_info(self, response):
        hdrs = [h.extract().strip() for h in response.xpath('//td[@class="owner_header"]/font/text()')]
        vals = [v.extract().strip() for v in response.xpath('//td[@class="owner_value"]/text()')]
        keys = [re.sub(r"\(|\)", "", h.lower().replace("\'", "")).replace(" ", "_").strip() for h in hdrs]
        info = dict(zip(keys, vals))
        # get href to parcel map if it exists
        links = response.xpath('//td[@class="owner_value"]/a[contains(@href,"extent")]/@href')
        if len(links) > 0:
            parcel_map_link = links[0].extract()
            [lng, lat] = self.get_address_location(parcel_map_link)
            info['location'] = [lng, lat]
        else:
            logging.warning("No parcel map link for " + info['location_address'])
            info['location'] = self.geocode_address(info['location_address'])
        return info

    def parse_property_sales(self, response):
        hdrs = response.css('td[class="sales_header"] > font::text').extract()
        keys = [h.lower().replace("/", "_").replace(" ", "_") for h in hdrs]
        value_info = response.css('td[class="sales_value"]').xpath('./text()').extract()
        values = [v.replace('\xa0', '').strip().replace('      ', '') for v in value_info]
        sales = []
        for i in range(0, len(values), 6):
            sale = values[i:i + 6]
            sales.append(dict(zip(keys, sale)))
        return sales

    def parse_property_values(self, response):
        hdrs = response.css('td[class="tax_header"] > font::text').extract()
        keys = [h.lower().replace("\n", "_").replace(" ", "_") for h in hdrs]
        value_info = response.css('.tax_value').xpath('./text()').extract()
        values = [v.replace('\xa0', '').replace(' ', '') for v in value_info]
        special_treatment_info = response.css('.tax_value').xpath('./font').extract()
        special_treatment_info = [re.sub('<[^>]*>', '', s) for s in special_treatment_info]
        year1_vals = values[0:9]
        year1_vals.extend(special_treatment_info[0:4])
        year2_vals = values[16:25]
        year2_vals.extend(special_treatment_info[4:8])
        year3_vals = values[32:41]
        year3_vals.extend(special_treatment_info[8:12])
        return [dict(zip(keys, year1_vals)),
                dict(zip(keys, year2_vals)),
                dict(zip(keys, year3_vals))]
