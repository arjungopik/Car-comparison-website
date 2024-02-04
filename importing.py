import pandas as pd
import os
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
import time

dbname = 'carcmp'
user = 'postgres'
password = 'user'
host = 'localhost'
port = '5432'
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cursor = conn.cursor()
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
id=0

excel_files = ['Book.xlsx']
for i in range(len(excel_files)):
    table_name = os.path.splitext(os.path.basename(excel_files[i]))[0]
    df = pd.read_excel(excel_files[i])
    column_names = df.columns.tolist()
    columns_str = ', '.join([f'"{col}" VARCHAR' for col in column_names])
    create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})'
    cursor.execute(create_table_query)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    time.sleep(5)
    print(f"{table_name} Data imported successfully from Excel to PostgreSQL.")
    conn.commit()
cursor.close()
conn.close()
