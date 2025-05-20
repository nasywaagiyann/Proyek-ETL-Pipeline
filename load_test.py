import unittest
import pandas as pd
from unittest.mock import patch, Mock
from utils.load import ekspor_ke_csv, unggah_ke_google_sheets
from gspread.exceptions import WorksheetNotFound


class TestLoad(unittest.TestCase):
    @patch('utils.load.gspread.authorize')
    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name')
    def test_unggah_ke_google_sheets_worksheet_not_found(self, mock_credentials, mock_authorize):
        df = pd.DataFrame({'col1': [1], 'col2': ['a']})

        mock_spreadsheet = Mock()
        mock_spreadsheet.worksheet.side_effect = WorksheetNotFound("Worksheet not found")
        mock_spreadsheet.add_worksheet.return_value = Mock()
        mock_spreadsheet.url = "https://docs.google.com/spreadsheets/d/fakeurl"

        mock_client = Mock()
        mock_client.open_by_key.return_value = mock_spreadsheet
        mock_authorize.return_value = mock_client
        mock_credentials.return_value = Mock()

        unggah_ke_google_sheets(df, 'dummy_id', 'Sheet1')

        mock_spreadsheet.add_worksheet.assert_called_once()

    def test_ekspor_ke_csv_exception(self):
        df = pd.DataFrame({'col1': [1]})
        # Patch df.to_csv agar raise Exception
        with patch.object(pd.DataFrame, 'to_csv', side_effect=Exception("Disk penuh")):
            ekspor_ke_csv(df, 'dummy.csv')

    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name', side_effect=Exception("Auth gagal"))
    def test_unggah_ke_google_sheets_auth_fail(self, mock_credentials):
        df = pd.DataFrame({'col1': [1]})
        with self.assertRaises(Exception) as context:
            unggah_ke_google_sheets(df, 'dummy_id')
        self.assertIn("Auth gagal", str(context.exception))
