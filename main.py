from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import ekspor_ke_csv, unggah_ke_google_sheets

def jalankan_pipeline():
    url_awal = 'https://fashion-studio.dicoding.dev/'
    kumpulan_produk = []

    print(f"Memulai pengambilan data dari: {url_awal}")
    try:
        hasil_scrape = scrape_main(url_awal)
        if hasil_scrape:
            kumpulan_produk += hasil_scrape
        else:
            print("Tidak ada data pada halaman utama.")
            return
    except Exception as err:
        print(f"Terjadi kesalahan saat mengakses halaman utama: {err}")
        return

    for halaman in range(2, 51):
        halaman_url = f"{url_awal}page{halaman}"
        print(f"Mengakses halaman {halaman}: {halaman_url}")
        try:
            hasil_scrape = scrape_main(halaman_url)
            if not hasil_scrape:
                print(f"Tidak ada data di halaman {halaman}. Pengambilan dihentikan.")
                break
            kumpulan_produk += hasil_scrape
        except Exception as err:
            print(f"Kesalahan saat mengambil data dari halaman {halaman}: {err}")
            break

    if not kumpulan_produk:
        print("Tidak ada produk yang berhasil diambil.")
        return

    print(f"\nTotal produk berhasil dikumpulkan: {len(kumpulan_produk)}")
    try:
        data_bersih = transform_data(kumpulan_produk)
        print(f"Total produk setelah transformasi dan pembersihan: {len(data_bersih)}")

        # Simpan ke file CSV
        ekspor_ke_csv(data_bersih, 'data_produk.csv')
        print("Data berhasil disimpan ke data_produk.csv")

        # Upload ke Google Sheets
        id_sheet = '1OyDTrheHmpvtBAGneqOb294glQX20QWtO6rbgp8SIdE'  
        nama_range = 'Sheet1!A1'
        unggah_ke_google_sheets(data_bersih, id_sheet, nama_range)
        print("Data berhasil diunggah ke Google Sheets.")
    except Exception as e:
        print(f"Kesalahan saat mentransformasi atau menyimpan data: {e}")

if __name__ == '__main__':
    jalankan_pipeline()
