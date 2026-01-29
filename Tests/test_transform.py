import pytest
import pandas as pd
from Utils.transform import transform_data

def test_transform_removes_unknown_product():
    """Test apakah Unknown Product dihapus"""
    data = {
        'Title': ['T-shirt 1', 'Unknown Product', 'Hoodie 3'],
        'Price': ['$100.00', '$200.00', '$300.00'],
        'Rating': ['4.5', '3.0', '4.8'],
        'Colors': ['3', '5', '2'],
        'Size': ['M', 'L', 'XL'],
        'Gender': ['Men', 'Women', 'Unisex'],
        'Timestamp': ['2026-01-27 12:00:00.000000'] * 3
    }
    df = pd.DataFrame(data)
    
    result = transform_data(df)
    
    assert 'Unknown Product' not in result['Title'].values
    assert len(result) == 2

def test_transform_removes_invalid_rating():
    """Test apakah Invalid Rating dihapus"""
    data = {
        'Title': ['T-shirt 1', 'T-shirt 2', 'T-shirt 3'],
        'Price': ['$100.00', '$200.00', '$300.00'],
        'Rating': ['4.5', 'Invalid Rating', '3.8'],
        'Colors': ['3', '5', '2'],
        'Size': ['M', 'L', 'XL'],
        'Gender': ['Men', 'Women', 'Unisex'],
        'Timestamp': ['2026-01-27 12:00:00.000000'] * 3
    }
    df = pd.DataFrame(data)
    
    result = transform_data(df)
    
    assert len(result) == 2
    assert 'Invalid Rating' not in result['Rating'].values

def test_transform_removes_not_rated():
    """Test apakah Not Rated dihapus"""
    data = {
        'Title': ['T-shirt 1', 'T-shirt 2'],
        'Price': ['$100.00', '$200.00'],
        'Rating': ['4.5', 'Not Rated'],
        'Colors': ['3', '5'],
        'Size': ['M', 'L'],
        'Gender': ['Men', 'Women'],
        'Timestamp': ['2026-01-27 12:00:00.000000'] * 2
    }
    df = pd.DataFrame(data)
    
    result = transform_data(df)
    
    assert len(result) == 1
    assert result.iloc[0]['Title'] == 'T-shirt 1'

def test_transform_converts_price_to_rupiah():
    """Test konversi price dari dollar ke rupiah (x16000)"""
    data = {
        'Title': ['T-shirt 1'],
        'Price': ['$100.00'],
        'Rating': ['4.5'],
        'Colors': ['3'],
        'Size': ['M'],
        'Gender': ['Men'],
        'Timestamp': ['2026-01-27 12:00:00.000000']
    }
    df = pd.DataFrame(data)
    
    result = transform_data(df)
    
    # $100 * 16000 = 1,600,000
    assert result.iloc[0]['Price'] == 1600000.0
    assert isinstance(result.iloc[0]['Price'], float)

def test_transform_cleans_colors():
    """Test pembersihan kolom Colors (ambil angka saja)"""
    data = {
        'Title': ['T-shirt 1'],
        'Price': ['$100.00'],
        'Rating': ['4.5'],
        'Colors': ['3'],
        'Size': ['M'],
        'Gender': ['Men'],
        'Timestamp': ['2026-01-27 12:00:00.000000']
    }
    df = pd.DataFrame(data)
    
    result = transform_data(df)
    
    assert result.iloc[0]['Colors'] == 3
    assert result['Colors'].dtype == 'int64' 

def test_transform_removes_duplicates():
    """Test penghapusan data duplikat"""
    data = {
        'Title': ['T-shirt 1', 'T-shirt 1', 'T-shirt 2'],
        'Price': ['$100.00', '$100.00', '$200.00'],
        'Rating': ['4.5', '4.5', '3.8'],
        'Colors': ['3', '3', '5'],
        'Size': ['M', 'M', 'L'],
        'Gender': ['Men', 'Men', 'Women'],
        'Timestamp': ['2026-01-27 12:00:00.000000'] * 3
    }
    df = pd.DataFrame(data)
    
    result = transform_data(df)
    
    assert len(result) == 2

def test_transform_removes_nulls():
    """Test penghapusan data dengan nilai null"""
    data = {
        'Title': ['T-shirt 1', None, 'T-shirt 3'],
        'Price': ['$100.00', '$200.00', '$300.00'],
        'Rating': ['4.5', '3.0', '4.8'],
        'Colors': ['3', '5', '2'],
        'Size': ['M', 'L', 'XL'],
        'Gender': ['Men', 'Women', 'Unisex'],
        'Timestamp': ['2026-01-27 12:00:00.000000'] * 3
    }
    df = pd.DataFrame(data)
    
    result = transform_data(df)
    
    assert len(result) == 2
    assert result['Title'].isna().sum() == 0

def test_transform_correct_data_types():
    """Test tipe data sudah benar setelah transform"""
    data = {
        'Title': ['T-shirt 1'],
        'Price': ['$100.00'],
        'Rating': ['4.5'],
        'Colors': ['3'],
        'Size': ['M'],
        'Gender': ['Men'],
        'Timestamp': ['2026-01-27 12:00:00.000000']
    }
    df = pd.DataFrame(data)
    
    result = transform_data(df)
    
    assert result['Price'].dtype == float
    assert result['Rating'].dtype == float
    assert result['Colors'].dtype == int
    assert result['Size'].dtype == object  # string
    assert result['Gender'].dtype == object  # string