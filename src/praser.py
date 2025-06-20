import re
from typing import Dict, Any, List
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class DataParser:
    """Parse and clean scraped data"""
    
    @staticmethod
    def parse_price(price_str: str) -> Optional[Decimal]:
        """Extract numeric price from string"""
        if not price_str:
            return None
        
        # Remove currency symbols and extract numbers
        price_cleaned = re.sub(r'[^\d.,]', '', price_str)
        price_cleaned = price_cleaned.replace(',', '')
        
        try:
            return Decimal(price_cleaned)
        except:
            logger.warning(f"Could not parse price: {price_str}")
            return None
    
    @staticmethod
    def parse_rating(rating_str: str) -> Optional[float]:
        """Extract rating from string"""
        if not rating_str:
            return None
        
        match = re.search(r'(\d+\.?\d*)', rating_str)
        if match:
            try:
                return float(match.group(1))
            except:
                pass
        return None
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove special characters if needed
        text = text.strip()
        
        return text
    
    @staticmethod
    def validate_url(url: str, base_url: str = "") -> str:
        """Ensure URL is absolute"""
        if not url:
            return ""
        
        if url.startswith('http'):
            return url
        elif url.startswith('/'):
            return base_url.rstrip('/') + url
        else:
            return base_url.rstrip('/') + '/' + url