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
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    tax_bill_number = scrapy.Field()
    property_class = scrapy.Field()
    special_tax_district = scrapy.Field()
    subdivision_name = scrapy.Field()
    land_area_sq_ft = scrapy.Field()
    zoning_district = scrapy.Field()
    building_area_sq_ft = scrapy.Field()
    square = scrapy.Field()
    lot = scrapy.Field()
    book = scrapy.Field()
    folio = scrapy.Field()
    line = scrapy.Field()
    parcel_map = scrapy.Field()
    legal_description = scrapy.Field()


class PropertyValue(scrapy.Item):
    year = scrapy.Field()
    land_value = scrapy.Field()
    building_value = scrapy.Field()
    total_value = scrapy.Field()
    assessed_land_value = scrapy.Field()
    assessed_building_value = scrapy.Field()
    assessed_total_value = scrapy.Field()
    homestead_exemption_value = scrapy.Field()
    taxable_assessment = scrapy.Field()

class PropertyTransfer(scrapy.Item):
    date = scrapy.Field()
    grantor = scrapy.Field()
    grantee = scrapy.Field()
    price = scrapy.Field()
    notarial_archive_number = scrapy.Field()
    instrument_number = scrapy.Field()
