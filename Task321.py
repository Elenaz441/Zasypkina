import pandas as pd
from datetime import datetime

file = input('Введите название файла: ')
df = pd.read_csv(file)
df['years'] = df['published_at'].apply(lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z').year)
years = df['years'].unique()
for year in years:
    data = df[df['years'] == year]
    data.to_csv(f'csv_files\\year_{year}.csv')