import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2
from psycopg2 import sql

def save_to_csv(df, filename='products.csv'):
    """Simpan dataframe ke CSV"""
    try:
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data berhasil disimpan ke {filename}")
        return True
    except Exception as e:
        print(f"Error saat menyimpan CSV: {e}")
        raise

def save_to_google_sheets(df, credentials_file='google-sheets-api.json',
                          sheet_name='Fashion Data ETL'):
    """
    Simpel: Upload dataframe ke Google Sheets yang sudah ada.
    Spreadsheet harus sudah dibuat dan sudah di-share ke service account.
    """
    try:
        # Setup credentials
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)
        print("Connected to Google Sheets")

        # Buka spreadsheet yang sudah ada
        sheet = client.open(sheet_name)
        worksheet = sheet.get_worksheet(0)  # ambil worksheet pertama

        # Bersihkan data lama
        worksheet.clear()
        print("Old data cleared")

        # Upload dataframe
        data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
        worksheet.update(data_to_upload, 'A1')
        print(f"Data berhasil diupload ke {sheet_name}!")
        print(f"URL: {sheet.url}")

        return sheet.url

    except Exception as e:
        print(f"Gagal upload ke Google Sheets: {e}")
        raise


def save_to_postgresql(df, host, database, user, password, table_name='products'):
    """Simpan dataframe ke PostgreSQL"""
    try:
        # Koneksi ke database
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Drop table jika sudah ada
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Buat table baru
        create_table_query = f"""
        CREATE TABLE {table_name} (
            title VARCHAR(255),
            price FLOAT,
            rating FLOAT,
            colors INTEGER,
            size VARCHAR(10),
            gender VARCHAR(20),
            timestamp TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        
        # Insert data
        for index, row in df.iterrows():
            insert_query = f"""
            INSERT INTO {table_name} (title, price, rating, colors, size, gender, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, tuple(row))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✓ Data berhasil disimpan ke PostgreSQL (table: {table_name})")
        return True
    except Exception as e:
        print(f"Error saat menyimpan ke PostgreSQL: {e}")
        raise