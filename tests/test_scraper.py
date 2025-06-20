import pytest
from unittest.mock import Mock, patch
from src.scraper import WebScraper

class TestWebScraper:
    @pytest.fixture
    def scraper(self):
        return WebScraper()
    
    def test_fetch_page_success(self, scraper):
        with patch('requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'<html><body>Test</body></html>'
            mock_get.return_value = mock_response
            
            result = scraper.fetch_page('http://test.com')
            assert result is not None
            assert result.status_code == 200
    
    def test_fetch_page_retry_on_failure(self, scraper):
        with patch('requests.Session.get') as mock_get:
            mock_get.side_effect = [Exception('Network error'), Mock(status_code=200)]
            
            result = scraper.fetch_page('http://test.com', retries=2)
            assert result is not None
            assert mock_get.call_count == 2
    
    def test_scrape_product_listing(self, scraper):
        html_content = '''
        <html>
            <body>
                <div class="product-item">
                    <h2 class="product-title">Test Product</h2>
                    <span class="product-price">$99.99</span>
                    <a href="/product/1">View</a>
                    <img src="/image1.jpg">
                </div>
            </body>
        </html>
        '''
        
        with patch.object(scraper, 'fetch_page') as mock_fetch:
            mock_response = Mock()
            mock_response.content = html_content.encode()
            mock_fetch.return_value = mock_response
            
            products = scraper.scrape_product_listing('http://test.com')
            assert len(products) == 1
            assert products[0]['title'] == 'Test Product'
            assert products[0]['price'] == '$99.99'