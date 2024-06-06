import pandas as pd
from sqlalchemy import create_engine
import random
import requests

# Leggi i dati dal file CSV
df = pd.read_csv('Books.csv')

# Rimuovi le colonne che non ci interessano
df = df.drop(columns=['Image-URL-S', 'Image-URL-M'])

# Add description column
df['Description'] = 'This is a book about ' + df['Book-Title'] + ' written by ' + df['Book-Author']

# Add random price column (between 10 and 100)
df['Price'] = [round(random.uniform(10, 100), 2) for _ in range(len(df))]

df = df.drop(columns=['Year-Of-Publication'])

# Rinomina le colonne
df = df.rename(columns={
    "ISBN": "isbn",
    "Book-Title": "title",
    "Book-Author": "author",
    "Publisher": "publisher",
    "Image-URL-L": "image_url",
    "Description": "description",
    "Price": "price"
})

print(df.head())

# Crea un motore di database
#engine = create_engine('postgresql://onlineshop:cloud2024@db_product:5432/flask_db')

# Inserisci i dati nel database
#df.to_sql('books', engine, if_exists='append', index=False)

#to add books you need to call api
API =" http://localhost:4004/api/product/create-book"

for i in range(len(df)):
    book = df.iloc[i].to_dict()
    print(book)
    response = requests.post(API, json=book)
    if response.status_code != 200:
        print('Failed to add book:', book)
        print('Response:', response.json())