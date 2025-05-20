import os
import pandas as pd
import gspread
import logging
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import pytest

def test_unggah_ke_google_sheets_auth_error(monkeypatch):
    df = pd.DataFrame({"a": [1]})

    def raise_error(*args, **kwargs):
        raise Exception("Auth Error")

    # Mock ServiceAccountCredentials.from_json_keyfile_name untuk gagal
    monkeypatch.setattr(
        "utils.load.ServiceAccountCredentials.from_json_keyfile_name",
        raise_error
    )

    with pytest.raises(Exception):
        unggah_ke_google_sheets(df, "dummy_id")

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ekspor_ke_csv(df: pd.DataFrame, nama_file="produk.csv"):
    """Simpan data ke file CSV tanpa index."""
    try:
        df.to_csv(nama_file, index=False)
        logging.info(f"Data berhasil disimpan ke file CSV: {nama_file}")
    except Exception as err:
        logging.error(f"Terjadi kesalahan saat menyimpan CSV: {err}")

def unggah_ke_google_sheets(df: pd.DataFrame, id_spreadsheet, nama_range="Sheet1!A1"):
    """Unggah DataFrame ke worksheet Google Sheets tertentu."""
    try:
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        kredensial = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)
        klien = gspread.authorize(kredensial)

        spreadsheet = klien.open_by_key(id_spreadsheet)

        # Ambil nama worksheet dari nama_range, misal 'Sheet1!A1' -> 'Sheet1'
        nama_worksheet = nama_range.split('!')[0]

        try:
            worksheet = spreadsheet.worksheet(nama_worksheet)
        except gspread.exceptions.WorksheetNotFound:
            logging.info(f"Worksheet '{nama_worksheet}' tidak ditemukan, membuat worksheet baru.")
            worksheet = spreadsheet.add_worksheet(title=nama_worksheet, rows="100", cols="20")

        worksheet.clear()

        data_to_update = [df.columns.values.tolist()] + df.values.tolist()
        worksheet.update(data_to_update)

        logging.info("Data berhasil diunggah ke Google Sheets.")
        logging.info(f"URL Google Sheets: {spreadsheet.url}")

    except Exception as error:
        logging.error(f"Gagal mengunggah data ke Google Sheets: {error}")
        raise
