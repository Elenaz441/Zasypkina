import pandas as pd
from typing import List, Dict, Tuple, Any
import sqlite3
from sqlalchemy import create_engine
import math


def normalise_row(row):
    """
    Возвращает зарплату по строке из dataframe

    Args:
        row (Any): Строка из dataframe

    Returns:
        float: Итоговая зарплата.
    """
    salary_from = row.salary_from
    salary_to = row.salary_to
    salary_currency = row.salary_currency
    salary = row.salary
    if type(salary_currency) is str:
        if not math.isnan(salary_from) and not math.isnan(salary_to):
            salary = (salary_from + salary_to) / 2
        elif not math.isnan(salary_from):
            salary = salary_from
        elif not math.isnan(salary_to):
            salary = salary_to
        if salary_currency != 'RUR' and salary_currency in ['BYR', 'USD', 'EUR', 'KZT', 'UAH']:
            date = f'01/{row.published_at[5:7]}/{row.published_at[:4]}'
            ratio_currency = cur.execute(f"""select {salary_currency} from currencies 
                                            where date='{date}'""").fetchone()[0]
            salary = float('NaN') if ratio_currency is None else salary * ratio_currency
        elif salary_currency != 'RUR':
            salary = float('NaN')
    return salary


conn = sqlite3.connect('project_vacancy.db')
cur = conn.cursor()
engine = create_engine('sqlite:///C:\\Users\\ezasy\\PycharmProjects\\Zasypkina\\project_vacancy.db')
pd.set_option('expand_frame_repr', False)
file = 'vacancies_dif_currencies.csv'
df = pd.read_csv(file)
df.insert(1, 'salary', float('NaN'))
df['salary'] = df.apply(lambda row: normalise_row(row), axis=1)
df.pop('salary_from')
df.pop('salary_to')
df.pop('salary_currency')
df['published_at'] = df['published_at'].apply(lambda s: s[:10])
# df.to_sql('vacancies', con=engine, index=False)