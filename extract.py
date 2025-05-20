import requests
from bs4 import BeautifulSoup

def scrape_main(link):
    try:
        hasil = requests.get(link, timeout=10)
        if hasil.status_code != 200:
            raise Exception(f"Response tidak OK: {hasil.status_code}")
    except requests.RequestException as err:
        raise Exception(f"Error saat mengakses {link}: {err}")
    
    try:
        parser = BeautifulSoup(hasil.content, 'html.parser')
        produk_elements = parser.select('div.collection-card')
        
        if len(produk_elements) == 0:
            raise Exception("Elemen produk tidak ditemukan pada halaman")
        
        daftar_produk = []
        
        for produk in produk_elements:
            def cari_teks(selector, default):
                elemen = produk.select_one(selector)
                return elemen.get_text(strip=True) if elemen else default
            
            def cari_paragraf(keyword, default):
                paragraf = produk.find('p', string=lambda s: s and keyword in s)
                return paragraf.get_text(strip=True) if paragraf else default
            
            item = {
                'title': cari_teks('h3.product-title', 'Judul tidak tersedia'),
                'price': cari_teks('div.price-container', 'Harga tidak tersedia'),
                'rating': cari_paragraf('Rating', 'Rating tidak tersedia'),
                'colors': cari_paragraf('Colors', 'Warna tidak tersedia'),
                'size': cari_paragraf('Size', 'Ukuran tidak tersedia'),
                'gender': cari_paragraf('Gender', 'Gender tidak tersedia')
            }
            
            daftar_produk.append(item)
        
        if not daftar_produk:
            raise Exception("Tidak ditemukan produk apapun")
        
        return daftar_produk
    
    except Exception as parse_err:
        raise Exception(f"Kesalahan saat memproses HTML: {parse_err}")
