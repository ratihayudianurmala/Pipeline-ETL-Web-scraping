import time
from datetime import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def ambil_konten(url):
    try:
        response = requests.get(url, headers=Headers, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None

def extract_fashion_data(article):

    # Ambil title dan price
    title = article.find('h3', class_='product-title')
    title = title.text.strip() if title else None
    
    price = article.find('span', class_='price')
    price = price.text.strip() if price else None
    
    # Ambil info dari tag <p>
    rating = None
    colors = None
    size = None
    gender = None
    
    for p in article.find_all('p'):
        text = p.text
        if 'Rating:' in text:
            rating = text.replace('Rating:', '').replace('⭐', '').replace('/ 5', '').strip()
        elif 'Colors' in text:
            colors = text.replace('Colors', '').strip()
        elif 'Size:' in text:
            size = text.replace('Size:', '').strip()
        elif 'Gender:' in text:
            gender = text.replace('Gender:', '').strip()
    
    fashion = {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender
    }
    
    return fashion

def scrape_fashion(base_url, max_page=50, delay=2):
    data = []
    url = base_url
    page = 0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    while page < max_page:
        page += 1
        print(f"Scraping halaman {page}")

        content = ambil_konten(url)
        soup = BeautifulSoup(content, "html.parser")
        articles = soup.find_all('div', class_='product-details')
        for article in articles:
            fashion = extract_fashion_data(article)
            if fashion["Title"]:
                fashion["Timestamp"] = timestamp
                data.append(fashion)

        next_button = soup.find('li', class_='next')
        if next_button:
            link = next_button.find('a')
            if link and link.get('href'):
                next_url = link.get('href')
                if not next_url.startswith('http'):
                    url = base_url + next_url
                else:
                    url = next_url
                time.sleep(delay)
            else:
                break
        else:
            break
 
    return data

def main():
    BASE_URL = "https://fashion-studio.dicoding.dev/"   
    all_data = scrape_fashion(BASE_URL, max_page=50, delay=2)
    df = pd.DataFrame(all_data)
    print(f"\nTotal: {len(df)} produk")
    print(df)

if __name__ == '__main__':
    main()