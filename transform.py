import pandas as pd
import numpy as np
import re
from datetime import datetime
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('future.no_silent_downcasting', True)

def clean_rating(rating_str):
    if pd.isna(rating_str):
        return np.nan
    match = re.search(r'(\d+(?:[.,]\d+)?)', str(rating_str))
    if match:
        rating_clean = match.group(1).replace(',', '.')
        try:
            return float(rating_clean)
        except ValueError:
            return np.nan
    return np.nan

def extract_color_count(text):
    if pd.isna(text):
        return np.nan
    match = re.search(r'(\d+)', str(text))
    if match:
        return int(match.group(1))
    return np.nan

def transform_data(products):
    print("DEBUG: Data input (products), contoh 3 item:")
    print(products[:3])  # print sebagian data mentah
    
    df = pd.DataFrame(products)
    print("\nDEBUG: Kolom DataFrame:", df.columns.tolist())
    print("DEBUG: 5 baris pertama DataFrame:")
    print(df.head())

    # Pastikan kolom penting ada
    required_cols = ['title', 'price', 'rating', 'colors', 'size', 'gender']
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Kolom '{col}' tidak ditemukan di data produk")

    # Filter title yang tidak valid
    df = df[df['title'].str.lower() != 'unknown product']

    # Bersihkan price: hapus simbol non-digit, ubah ke float, rupiah (kurs 16000)
    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df[df['price'].notna()]
    df = df[df['price'] > 0]
    df['price'] = df['price'] * 16000

    # Bersihkan rating
    # Bersihkan rating dan bulatkan ke 1 angka di belakang koma
    df['rating'] = df['rating'].apply(clean_rating).round(1)
    df = df[df['rating'].notna()]


    # Bersihkan colors
    df['colors'] = df['colors'].apply(extract_color_count)
    df = df[df['colors'].notna()]
    df['colors'] = df['colors'].astype(int)

    # Bersihkan size dan gender
    df['size'] = df['size'].replace(r'Size:\s*', '', regex=True)
    df['gender'] = df['gender'].replace(r'Gender:\s*', '', regex=True)

    # Hapus duplikasi dan NA
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Tambah timestamp
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("\nDEBUG: Data setelah transformasi:")
    print(df.head())

    return df
