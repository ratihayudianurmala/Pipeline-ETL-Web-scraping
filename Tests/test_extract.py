import pytest
import sys
import os

# Tambahkan parent directory ke path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils.extract import ambil_konten, extract_fashion_data, scrape_fashion
from bs4 import BeautifulSoup
import pandas as pd

def test_ambil_konten_success():
    """Test apakah fungsi ambil_konten berhasil fetch data dari URL valid"""
    url = "https://fashion-studio.dicoding.dev/"
    content = ambil_konten(url)
    
    assert content is not None
    assert len(content) > 0
    assert isinstance(content, bytes)

def test_ambil_konten_invalid_url():
    """Test error handling untuk URL invalid"""
    url = "https://invalid-url-that-doesnt-exist-12345.com"
    content = ambil_konten(url)
    
    assert content is None

def test_extract_fashion_data_complete():
    """Test extract data dengan semua field lengkap"""
    html = """
    <div class="product-details">
        <h3 class="product-title">T-shirt 1</h3>
        <span class="price">$50.00</span>
        <p>Rating: ⭐ 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('div', class_='product-details')
    
    result = extract_fashion_data(article)
    
    assert result['Title'] == 'T-shirt 1'
    assert result['Price'] == '$50.00'
    assert result['Rating'] == '4.5'
    assert result['Colors'] == '3'
    assert result['Size'] == 'M'
    assert result['Gender'] == 'Men'

def test_extract_fashion_data_missing_fields():
    """Test extract data dengan beberapa field yang hilang"""
    html = """
    <div class="product-details">
        <h3 class="product-title">T-shirt 2</h3>
        <span class="price">$75.00</span>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('div', class_='product-details')
    
    result = extract_fashion_data(article)
    
    assert result['Title'] == 'T-shirt 2'
    assert result['Price'] == '$75.00'
    assert result['Rating'] is None
    assert result['Colors'] is None
    assert result['Size'] is None
    assert result['Gender'] is None

def test_extract_fashion_data_no_title():
    """Test extract data tanpa title"""
    html = """
    <div class="product-details">
        <span class="price">$100.00</span>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('div', class_='product-details')
    
    result = extract_fashion_data(article)
    
    assert result['Title'] is None
    assert result['Price'] == '$100.00'

def test_scrape_fashion_basic():
    """Test scrape_fashion bisa scrape minimal 1 halaman"""
    BASE_URL = "https://fashion-studio.dicoding.dev/"
    
    # Scrape 1 halaman saja untuk test cepat
    data = scrape_fashion(BASE_URL, max_page=1, delay=0)
    
    assert len(data) > 0
    assert isinstance(data, list)
    assert 'Title' in data[0]
    assert 'Price' in data[0]
    assert 'Timestamp' in data[0]

def test_scrape_fashion_returns_dataframe_compatible():
    """Test data hasil scraping bisa dikonversi ke DataFrame"""
    BASE_URL = "https://fashion-studio.dicoding.dev/"
    
    data = scrape_fashion(BASE_URL, max_page=1, delay=0)
    df = pd.DataFrame(data)
    
    assert len(df) > 0
    assert 'Title' in df.columns
    assert 'Price' in df.columns
    assert 'Rating' in df.columns
    assert 'Colors' in df.columns
    assert 'Size' in df.columns
    assert 'Gender' in df.columns
    assert 'Timestamp' in df.columns

def test_scrape_fashion_timestamp_exists():
    """Test setiap data punya timestamp"""
    BASE_URL = "https://fashion-studio.dicoding.dev/"
    
    data = scrape_fashion(BASE_URL, max_page=1, delay=0)
    
    for item in data:
        assert 'Timestamp' in item
        assert item['Timestamp'] is not None
        assert len(item['Timestamp']) > 0