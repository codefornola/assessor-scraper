# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, mock_open

class AssessmentSpiderTestCase(unittest.TestCase):
    def setUp(self):
        with patch("builtins.open", mock_open(read_data="data1\ndata2")) as mock_file:
            from scraper.spiders.assessment_spider import AssessmentSpider
            self.spider = AssessmentSpider()

    def test_clean_key__lot_folio(self):
        result = self.spider._clean_key('Lot / Folio')
        self.assertEqual(
            result,
            'lot_folio'
        )

    def test_clean_key__land_area(self):
        result = self.spider._clean_key('Land Area (sq ft)	')
        self.assertEqual(
            result,
            'land_area_sq_ft'
        )
