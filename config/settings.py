import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Scraping settings
    USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    RETRY_TIMES = int(os.getenv('RETRY_TIMES', 3))
    DELAY_BETWEEN_REQUESTS = float(os.getenv('DELAY_BETWEEN_REQUESTS', 1.0))
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/products.db')
    
    # Output settings
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'csv')  # csv, json, database
    OUTPUT_PATH = os.getenv('OUTPUT_PATH', 'data/processed/')
    
    # Target website
    TARGET_URL = os.getenv('TARGET_URL', 'https://example-shop.com')
    
    # Proxy settings (optional)
    USE_PROXY = os.getenv('USE_PROXY', 'False').lower() == 'true'
    PROXY_URL = os.getenv('PROXY_URL', '')