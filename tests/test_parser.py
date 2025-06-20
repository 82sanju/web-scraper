import pytest
from decimal import Decimal
from src.parser import DataParser

class TestDataParser:
    def test_parse_price(self):
        parser = DataParser()
        
        # Test valid prices
        assert parser.parse_price('$99.99') == Decimal('99.99')
        assert parser.parse_price('€1,234.56') == Decimal('1234.56')
        assert parser.parse_price('123') == Decimal('123')
        
        # Test invalid prices
        assert parser.parse_price('') is None
        assert parser.parse_price('abc') is None
    
    def test_parse_rating(self):
        parser = DataParser()
        
        # Test valid ratings
        assert parser.parse_rating('4.5 out of 5') == 4.5
        assert parser.parse_rating('Rating: 3.0') == 3.0
        assert parser.parse_rating('5') == 5.0
        
        # Test invalid ratings
        assert parser.parse_rating('') is None
        assert parser.parse_rating('no rating') is None
    
    def test_clean_text(self):
        parser = DataParser()
        
        assert parser.clean_text('  Hello   World  ') == 'Hello World'
        assert parser.clean_text('Line\n\nBreak') == 'Line Break'
        assert parser.clean_text('') == ''
        assert parser.clean_text(None) == ''
    
    def test_validate_url(self):
        parser = DataParser()
        base_url = 'https://example.com'
        
        assert parser.validate_url('https://example.com/page', base_url) == 'https://example.com/page'
        assert parser.validate_url('/page', base_url) == 'https://example.com/page'
        assert parser.validate_url('page', base_url) == 'https://example.com/page'
        assert parser.validate_url('', base_url) == ''