import pandas as pd
import sqlite3
from sqlalchemy import create_engine

conn = sqlite3.connect('project_vacancy.db')
engine = create_engine('sqlite:///C:\\Users\\ezasy\\PycharmProjects\\Zasypkina\\project_vacancy.db')
df = pd.read_csv('data_currencies.csv')
df.to_sql('currencies', con=engine, index=False)
