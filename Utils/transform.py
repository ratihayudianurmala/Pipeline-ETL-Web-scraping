import pandas as pd

def transform_data(df):
    try:
        #data invalid
        df = df[df['Title'] != 'Unknown Product']
        df = df[~df['Rating'].isin(['Invalid Rating', 'Not Rated'])]

        #Konversi harga
        df['Price'] = df['Price'].str.replace('$', '').astype(float) * 16000

        #bersihkan colors
        df['Colors'] = df['Colors'].astype(str).str.extract(r'(\d+)').astype(int)

        #bersihkan size
        df['Size'] = df['Size'].str.replace('Size: ', '').astype(str)


        #bersihkan gender
        df['Gender'] = df['Gender'].str.replace('Gender: ', '').astype(str)

        #convert rating ke float
        df["Rating"] = df['Rating'].astype(float)

        df = df.drop_duplicates()
        df = df.dropna()  
    
        return df     
    except Exception as e:
        print(f"Error saat transformasi: {e}")
        raise
