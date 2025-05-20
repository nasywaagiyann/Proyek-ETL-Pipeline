import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from utils.transform import transform_data as bersihkan_data

class TestTransform(unittest.TestCase):
    def test_bersihkan_data_basic(self):
        data_input = [
            {
                'title': 'Produk A',
                'price': '$20.00',
                'rating': 'Rating: 4.5',
                'colors': 'Colors: 3',
                'size': 'Size: M',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'unknown product',
                'price': '$15.00',
                'rating': 'Rating: 3.0',
                'colors': 'Colors: 2',
                'size': 'Size: S',
                'gender': 'Gender: Male'
            },
            {
                'title': 'Produk C',
                'price': 'Harga tidak tersedia',
                'rating': 'Rating: 4.0',
                'colors': 'Colors: 4',
                'size': 'Size: L',
                'gender': 'Gender: Female'
            }
        ]
        
        df_cleaned = bersihkan_data(data_input)

        self.assertNotIn('unknown product', df_cleaned['title'].str.lower().values)
        self.assertNotIn('Produk C', df_cleaned['title'].values)

        self.assertTrue(all(df_cleaned['price'] > 0))
        self.assertTrue(df_cleaned['rating'].dtype == float)
        self.assertTrue(df_cleaned['colors'].dtype == int)

        self.assertFalse(df_cleaned['size'].str.contains('Size:').any())
        self.assertFalse(df_cleaned['gender'].str.contains('Gender:').any())

        self.assertIn('timestamp', df_cleaned.columns)
        self.assertTrue(df_cleaned['timestamp'].notnull().all())

if __name__ == '__main__':
    unittest.main()
