# -*- coding: utf-8 -*-

import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from scraper import settings

Base = declarative_base()


def db_connect():
    """
    Returns sqlalchemy engine instance
    """
    if 'DATABASE_URL' in os.environ:
        DATABASE_URL = os.environ['DATABASE_URL']
        logging.debug("Connecting to %s", URL)
    else:
        DATABASE_URL = URL(**settings.DATABASE)
        logging.debug("Connecting with settings %s", DATABASE_URL)
    return create_engine(DATABASE_URL)


def create_tables(engine):
    Base.metadata.create_all(engine)


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    property_key = Column(String, nullable=False)
    todays_date = Column(String)
    location = Column(String)
    owner_name = Column(String)
    mailing_address = Column(String)
    municipal_district = Column(String)
    location_address = Column(String)
    tax_bill_number = Column(String)
    property_class = Column(String)
    special_tax_district = Column(String)
    subdivision_name = Column(String)
    land_area_sq_ft = Column(String)
    zoning_district = Column(String)
    building_area_sq_ft = Column(String)
    square = Column(String)
    lot = Column(String)
    book = Column(String)
    folio = Column(String)
    line = Column(String)
    parcel_map = Column(String)
    legal_description = Column(String)
    assessment_area = Column(String)
    values = relationship('PropertyValue')
    transfers = relationship('PropertyTransfer')


class PropertyValue(Base):
    __tablename__ = 'property_values'

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    year = Column(String)
    land_value = Column(String)
    building_value = Column(String)
    total_value = Column(String)
    assessed_land_value = Column(String)
    assessed_building_value = Column(String)
    total_assessed_value = Column(String)
    homestead_exemption_value = Column(String)
    taxable_assessment = Column(String)
    age_freeze = Column(String)
    disability_freeze = Column(String)
    assmnt_change = Column(String)
    tax_contract = Column(String)


class PropertyTransfer(Base):
    __tablename__ = 'property_transfers'

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    sale_transfer_date = Column(String)
    price = Column(String)
    grantor = Column(String)
    grantee = Column(String)
    notarial_archive_number = Column(String)
    instrument_number = Column(String)
