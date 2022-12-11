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


if __name__ == '__main__':
    file = input('Введите название файла: ')
    vacancy = input('Введите название вакансии: ')
    df = pd.read_csv(file)
    df['years'] = df['published_at'].apply(lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z').year)
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
    print('Динамика уровня зарплат по годам:', salary_by_years)
    print('Динамика уровня зарплат по годам для выбранной профессии:', vac_salary_by_years)
    print('Динамика количества вакансий по годам:', count_by_years)
    print('Динамика количества вакансий по годам для выбранной профессии:', vac_count_by_years)
    data = DataSet(file)
    dict_cities = {}
    for vac in data.vacancies_objects:
        if vac.area_name not in dict_cities.keys():
            dict_cities[vac.area_name] = 0
        dict_cities[vac.area_name] += 1
    needed_vacancies_objects = list(
        filter(lambda vac: int(len(data.vacancies_objects) * 0.01) <= dict_cities[vac.area_name],
               data.vacancies_objects))
    print_statistic(get_salary_level(needed_vacancies_objects, 'area_name').items(), 1,
                    'Уровень зарплат по городам (в порядке убывания): ', True, 10)
    print_statistic(get_count_vacancies(needed_vacancies_objects, 'area_name', data).items(), 1,
                    'Доля вакансий по городам (в порядке убывания): ', True, 10)