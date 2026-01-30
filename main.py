from Utils.extract import scrape_fashion
from Utils.transform import transform_data
from Utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql
import pandas as pd
import os
from dotenv import load_dotenv


def main():
    BASE_URL = "https://fashion-studio.dicoding.dev/"
    load_dotenv()

    # Extract
    print("="*50)
    print("TAHAP 1: EXTRACT")
    print("="*50)
    raw_data = scrape_fashion(BASE_URL, max_page=50, delay=2)
    df_raw = pd.DataFrame(raw_data)
    print(f"Data mentah: {len(df_raw)} rows\n")
    
    # Transform
    print("="*50)
    print("TAHAP 2: TRANSFORM")
    print("="*50)
    df_clean = transform_data(df_raw)
    print(f"Data bersih: {len(df_clean)} rows\n")
    
    # Load
    print("="*50)
    print("TAHAP 3: LOAD")
    print("="*50)
    
    # 1. Save to CSV
    save_to_csv(df_clean, 'products.csv')
    
    # 2. Save to Google Sheets
    try:
        sheet_url = save_to_google_sheets(
        df_clean, 
        credentials_file='google-sheets-api.json',
        sheet_name='Fashion Data ETL'
        )
        print(f"Google Sheets URL: {sheet_url}")
    except Exception as e:
        print(f"Gagal save ke Google Sheets: {e}")  

    # 3. Save to PostgreSQL
    try:
        save_to_postgresql(
            df_clean,
            host=os.getenv('DB_HOST', 'localhost'), 
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            table_name='fashion_products'
        )
    except Exception as e:
        print(f"Gagal save ke PostgreSQL: {e}")
    
    print("\n" + "="*50)
    print("ETL PIPELINE SELESAI!")
    print("="*50)
    
    # Preview hasil
    print("\nPreview data bersih:")
    print(df_clean.head())
    print("\nInfo tipe data:")
    print(df_clean.dtypes)

if __name__ == '__main__':
    main()