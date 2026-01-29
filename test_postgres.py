import psycopg2
import os
from dotenv import load_dotenv

try:
    conn = psycopg2.connect(
        host='localhost',
        database='etl_db',
        user='postgres',
        password='plosotimur2' 
    )
    print("Koneksi ke PostgreSQL berhasil!")
    conn.close()
except Exception as e:
    print(f"Gagal koneksi: {e}")