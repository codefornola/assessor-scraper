# -*- coding: utf-8 -*-

# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Property(scrapy.Item):
    property_key = scrapy.Field()
    owner_name = scrapy.Field()
    todays_date = scrapy.Field()
    mailing_address = scrapy.Field()
    municipal_district = scrapy.Field()
    location_address = scrapy.Field()
    location = scrapy.Field()
    tax_bill_number = scrapy.Field()
    property_class = scrapy.Field()
    special_tax_district = scrapy.Field()
    subdivision_name = scrapy.Field()
    land_area_sq_ft = scrapy.Field()
    zoning_district = scrapy.Field()
    building_area_sq_ft = scrapy.Field()
    square = scrapy.Field()
    lot_folio = scrapy.Field()
    book = scrapy.Field()
    folio = scrapy.Field()
    line = scrapy.Field()
    parcel_map = scrapy.Field()
    legal_description = scrapy.Field()
    assessment_area = scrapy.Field()
    sales = scrapy.Field()
    values = scrapy.Field()
    revised_bldg_area_sqft = scrapy.Field()
