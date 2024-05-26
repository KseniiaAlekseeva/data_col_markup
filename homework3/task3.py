import pandas as pd
from clickhouse_driver import Client
import sys

file_path = 'log3.txt'
sys.stdout = open(file_path, "w")

client = Client('localhost')

records = client.execute('SELECT * FROM books_data.books')
df = pd.DataFrame(records, columns=['id', 'Name', 'Price', 'Amount', 'Description'])
print(df.head())

records = client.execute("SELECT * FROM books_data.books WHERE isNull(Price)")
df_fatal = pd.DataFrame(records, columns=df.columns)
print(df_fatal)

records = client.execute("SELECT * FROM books_data.books WHERE Amount = '1'")
df_amount_1 = pd.DataFrame(records, columns=df.columns)
print(df_amount_1)

min_price = 11.0
max_price = 13.0
records = client.execute(
    f"SELECT * FROM books_data.books WHERE Price BETWEEN {min_price} AND {max_price}")
df_price = pd.DataFrame(records, columns=df.columns)
print(df_price[['Name', 'Price']])

df_price['Price'] = df_price['Price'].apply(lambda pr: int(pr))
print(df_price[['Name', 'Price']])

sorted_records = client.execute("SELECT * FROM books_data.books ORDER BY Price DESC")
df_sorted_records = pd.DataFrame(sorted_records, columns=df.columns)
print(df_sorted_records[['Name', 'Price']])

multi_sorted_records = client.execute("SELECT * FROM books_data.books ORDER BY Amount ASC, Price DESC")
df_multi_sorted_records = pd.DataFrame(multi_sorted_records, columns=df.columns)
print(df_multi_sorted_records[['Amount', 'Price']])

count_records = client.execute("SELECT COUNT(*) FROM books_data.books WHERE isNotNull(Price) AND isNotNull(Amount) AND isNotNull(Description)")
print("Общее количество полных записей:", count_records[0][0])

amount_count_records = client.execute("SELECT Amount, COUNT(*) FROM books_data.books GROUP BY Amount ORDER BY Amount ASC")
df_amount_count_records = pd.DataFrame(amount_count_records, columns=['Amount', 'Count'])
print(df_amount_count_records)

avg_price = client.execute("SELECT AVG(Price) FROM books_data.books")
print("Средняя цена книг:", avg_price[0][0])

avg_price = client.execute("SELECT SUM(Price*Amount)/SUM(Amount) FROM books_data.books")
print("Средняя цена книг с учетом количества:", avg_price[0][0])
