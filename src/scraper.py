import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from typing import Dict, List, Optional
import logging
from config.settings import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.config = Config()
        self._setup_session()
    
    def _setup_session(self):
        """Configure session with headers and proxies"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        if self.config.USE_PROXY and self.config.PROXY_URL:
            self.session.proxies = {
                'http': self.config.PROXY_URL,
                'https': self.config.PROXY_URL
            }
    
    def fetch_page(self, url: str, retries: int = None) -> Optional[requests.Response]:
        """Fetch a single page with retry logic"""
        retries = retries or self.config.RETRY_TIMES
        
        for attempt in range(retries):
            try:
                logger.info(f"Fetching: {url} (Attempt {attempt + 1})")
                response = self.session.get(url, timeout=self.config.REQUEST_TIMEOUT)
                
                if response.status_code == 200:
                    return response
                else:
                    logger.warning(f"Status code {response.status_code} for {url}")
                    
            except requests.RequestException as e:
                logger.error(f"Error fetching {url}: {str(e)}")
                
            if attempt < retries - 1:
                time.sleep(self.config.DELAY_BETWEEN_REQUESTS)
        
        return None
    
    def scrape_product_listing(self, url: str) -> List[Dict]:
        """Scrape product listing page"""
        response = self.fetch_page(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'lxml')
        products = []
        
        # Example scraping logic - customize based on target website
        for product in soup.select('.product-item'):
            product_data = {
                'title': product.select_one('.product-title').text.strip() if product.select_one('.product-title') else '',
                'price': product.select_one('.product-price').text.strip() if product.select_one('.product-price') else '',
                'url': product.select_one('a')['href'] if product.select_one('a') else '',
                'image': product.select_one('img')['src'] if product.select_one('img') else '',
            }
            products.append(product_data)
        
        return products
    
    def scrape_product_details(self, url: str) -> Dict:
        """Scrape individual product page"""
        response = self.fetch_page(url)
        if not response:
            return {}
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Example detail extraction - customize based on target website
        details = {
            'title': soup.select_one('h1').text.strip() if soup.select_one('h1') else '',
            'price': soup.select_one('.price').text.strip() if soup.select_one('.price') else '',
            'description': soup.select_one('.description').text.strip() if soup.select_one('.description') else '',
            'availability': soup.select_one('.availability').text.strip() if soup.select_one('.availability') else '',
            'rating': soup.select_one('.rating').text.strip() if soup.select_one('.rating') else '',
        }
        
        return details