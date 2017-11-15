# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker

from scraper.models import Property, PropertyTransfer, PropertyValue, db_connect, create_tables


class PostgresPipeline(object):
    """Pipeline for storing scraped items in postgres"""

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        This method is called for every item emitted by the spider.
        """
        session = self.Session()
        sales = item['sales']
        values = item['values']
        del item['sales']
        del item['values']
        property = Property(**item)

        try:
            session.add(property)
            # flush to obtain the id of property to be used as the foreign key
            session.flush()

            for sale in sales:
                sale['property_id'] = property.id
                session.add(PropertyTransfer(**sale))
            for value in values:
                value['property_id'] = property.id
                session.add(PropertyValue(**value))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
