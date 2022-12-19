from multiprocessing import Pool

import pandas as pd
from datetime import datetime
from functools import partial
from Task232 import get_count_vacancies, get_salary_level, DataSet, print_statistic


def get_statistic_by_year(file, vacancy, statistics):
    df = pd.read_csv(file)
    df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
    year = int(file[15:19])
    statistics[0] = (year, int(df['salary'].mean()))
    statistics[1] = (year, int(df[df['name'] == vacancy]['salary'].mean()))
    statistics[2] = (year, len(df))
    statistics[3] = (year, len(df[df['name'] == vacancy]))
    return statistics


def get_stat_by_year(file, vacancy):
    df = pd.read_csv(file)
    df['years'] = df['published_at'].apply(lambda s: s[:4])
    years = df['years'].unique()
    salary_by_years = {year: [] for year in years}
    vac_salary_by_years = {year: [] for year in years}
    count_by_years = {year: 0 for year in years}
    vac_count_by_years = {year: 0 for year in years}
    statistics = [salary_by_years, vac_salary_by_years, count_by_years, vac_count_by_years]
    files = []
    for year in years:
        # data = df[df['years'] == year]
        # data.to_csv(f'csv_files\\year_{year}.csv')
        files.append(f'csv_files\\year_{year}.csv')
    p = Pool()
    output = list(p.map(partial(get_statistic_by_year, vacancy=vacancy, statistics=statistics), files))
    salary_by_years = {stat[0][0]: stat[0][1] for stat in output}
    vac_salary_by_years = {stat[1][0]: stat[1][1] for stat in output}
    count_by_years = {stat[2][0]: stat[2][1] for stat in output}
    vac_count_by_years = {stat[3][0]: stat[3][1] for stat in output}
    return [salary_by_years, vac_salary_by_years, count_by_years, vac_count_by_years]
    # print('Динамика уровня зарплат по годам:', salary_by_years)
    # print('Динамика уровня зарплат по годам для выбранной профессии:', vac_salary_by_years)
    # print('Динамика количества вакансий по годам:', count_by_years)
    # print('Динамика количества вакансий по годам для выбранной профессии:', vac_count_by_years)