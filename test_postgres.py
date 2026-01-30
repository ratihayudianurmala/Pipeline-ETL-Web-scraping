import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# 2. Panggil pakai os.getenv
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    port=os.getenv("DB_PORT")
)

print("Berhasil konek ke Postgres dengan aman!")