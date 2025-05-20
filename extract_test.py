import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, Mock
from utils.extract import scrape_main  # path import sekarang pasti benar

class TestExtract(unittest.TestCase):
    @patch('utils.extract.requests.get')
    def test_scrape_main_success(self, mock_get):
        contoh_html = '''
        <html><body>
        <div class="collection-card">
            <h3 class="product-title">Produk A</h3>
            <div class="price-container">$20.00</div>
            <p>Rating: 4.5</p>
            <p>Colors: 3</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        <div class="collection-card">
            <h3 class="product-title">Produk B</h3>
            <div class="price-container">$35.00</div>
            <p>Rating: 4.0</p>
            <p>Colors: 5</p>
            <p>Size: L</p>
            <p>Gender: Female</p>
        </div>
        </body></html>'''
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = contoh_html.encode('utf-8')
        mock_get.return_value = mock_response
        
        url = "https://fashion-studio.dicoding.dev/"
        result = scrape_main(url)
        
        expected = [
            {'title': 'Produk A', 'price': '$20.00', 'rating': 'Rating: 4.5', 'colors': 'Colors: 3', 'size': 'Size: M', 'gender': 'Gender: Unisex'},
            {'title': 'Produk B', 'price': '$35.00', 'rating': 'Rating: 4.0', 'colors': 'Colors: 5', 'size': 'Size: L', 'gender': 'Gender: Female'}
        ]
        self.assertEqual(result, expected)

    @patch('utils.extract.requests.get')
    def test_scrape_main_raises_on_bad_status(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        with self.assertRaises(Exception) as context:
            scrape_main("https://fashion-studio.dicoding.dev/")
        self.assertIn("Response tidak OK", str(context.exception))

if __name__ == '__main__':
    unittest.main()
