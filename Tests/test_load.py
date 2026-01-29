# tests/test_load.py
import pytest
import pandas as pd
import os
from Utils import load
from unittest.mock import patch, MagicMock

# Sample dataframe untuk semua test
df_sample = pd.DataFrame({
    'title': ['Product A', 'Product B'],
    'price': [100.0, 200.0],
    'rating': [4.5, 3.8],
    'colors': [3, 2],
    'size': ['M', 'L'],
    'gender': ['Men', 'Women'],
    'timestamp': ['2026-01-27 00:00:00', '2026-01-27 01:00:00']
})

# -------------------------------
# Test save_to_csv
# -------------------------------
def test_save_to_csv_success(tmp_path):
    file_path = tmp_path / "test_products.csv"
    result = load.save_to_csv(df_sample, filename=file_path)
    assert result is True
    assert file_path.exists()

def test_save_to_csv_columns(tmp_path):
    file_path = tmp_path / "test_columns.csv"
    load.save_to_csv(df_sample, filename=file_path)
    df_read = pd.read_csv(file_path)
    for col in df_sample.columns:
        assert col in df_read.columns

def test_save_to_csv_empty_dataframe(tmp_path):
    file_path = tmp_path / "test_empty.csv"
    df_empty = pd.DataFrame()
    result = load.save_to_csv(df_empty, filename=file_path)
    assert result is True
    assert file_path.exists()

# -------------------------------
# Test save_to_postgresql dengan mock
# -------------------------------
@patch("psycopg2.connect")
def test_save_to_postgresql_success(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    result = load.save_to_postgresql(
        df_sample,
        host="localhost",
        database="testdb",
        user="user",
        password="pass",
        table_name="products_test"
    )

    # Pastikan koneksi & commit dilakukan
    mock_connect.assert_called_once()
    mock_conn.cursor.assert_called()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called()
    assert result is True

# -------------------------------
# Test save_to_google_sheets dengan mock lengkap
# -------------------------------
@patch("Utils.load.gspread.authorize")
@patch("Utils.load.ServiceAccountCredentials.from_json_keyfile_name")
def test_save_to_google_sheets_success(mock_creds, mock_authorize):
    # Mock credentials
    mock_creds.return_value = MagicMock()

    # Mock client, sheet, dan worksheet
    mock_client = MagicMock()
    mock_sheet = MagicMock()
    mock_worksheet = MagicMock()

    mock_authorize.return_value = mock_client
    mock_client.open.return_value = mock_sheet
    mock_sheet.get_worksheet.return_value = mock_worksheet
    mock_sheet.url = "https://docs.google.com/spreadsheets/d/123"

    # Panggil fungsi
    url = load.save_to_google_sheets(
        df_sample, 
        credentials_file='dummy.json', 
        sheet_name='Test Sheet'
    )

    # Pastikan worksheet clear & update dipanggil
    mock_worksheet.clear.assert_called_once()
    mock_worksheet.update.assert_called_once()
    # Pastikan URL dikembalikan
    assert url == "https://docs.google.com/spreadsheets/d/123"
