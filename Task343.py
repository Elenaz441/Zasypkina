from multiprocessing import Pool
from typing import List, Dict, Tuple, Any
import pandas as pd
from functools import partial
from statistic import Report
import math


def get_statistic_by_city(file: str) -> List[Dict[str, Any]]:
    """
    Возвращает статистики по городам

    Args:
        file (str): Название файла

    Returns:
        List[Dict[str, Any]]: Список статистик по городам.
    """
    df = pd.read_csv(file)
    df = df[df['area_name'].map(df['area_name'].value_counts() >= len(df) * 0.01)]
    df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
    cities = df["area_name"].unique()
    stat1 = {city: [] for city in cities}
    stat2 = {city: 0 for city in cities}
    for city in cities:
        stat1[city] = df[df['area_name'] == city]['salary'].mean() if \
            math.isnan(df[df['area_name'] == city]['salary'].mean()) else \
            int(df[df['area_name'] == city]['salary'].mean())
        stat2[city] = round(len(df[df['area_name'] == city]) / len(df), 4)
    stat1 = dict(sorted(stat1.items(), key=lambda x: x[1], reverse=True)[:10])
    stat2 = dict(sorted(stat2.items(), key=lambda x: x[1], reverse=True)[:10])
    return [stat1, stat2]


def get_statistic_by_year(file: str, vacancy: str, area_name: str, statistics: List[Dict[int, Any]]) -> List[Dict[int, Any]]:
    """
    Преобразовывает статистики для конкретного года

    Args:
        file (str): Название файла
        vacancy (str): Название вакансии
        area_name (str): Название региона
        statistics (List[Dict[int, Any]]): Список статистик по годам

    Returns:
        List[Dict[int, Any]]: Список статистик по годам.
    """
    df = pd.read_csv(file)
    df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
    year = int(file[15:19])
    statistics[0] = (year, int(df['salary'].mean()))
    statistics[1] = (year, df[(df['name'] == vacancy) & (df['area_name'] == area_name)]['salary'].mean() if
        math.isnan(df[(df['name'] == vacancy) & (df['area_name'] == area_name)]['salary'].mean()) else
        int(df[(df['name'] == vacancy) & (df['area_name'] == area_name)]['salary'].mean()))
    statistics[2] = (year, len(df))
    statistics[3] = (year, len(df[(df['name'] == vacancy) & (df['area_name'] == area_name)]))
    return statistics


def get_statistics(file: str, vacancy: str, area_name: str) -> List[Dict[Any, Any]]:
    """
    Возвращает статистики

    Args:
        file (str): Название файла
        vacancy (str): Название вакансии
        area_name (str): Название региона

    Returns:
        List[Dict[Any, Any]]: Список статистик.
    """
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
        data = df[df['years'] == year]
        data.to_csv(f'csv_files\\year_{year}.csv')
        files.append(f'csv_files\\year_{year}.csv')
    p = Pool()
    output = list(p.map(partial(get_statistic_by_year, vacancy=vacancy, area_name=area_name, statistics=statistics), files))
    salary_by_years = {stat[0][0]: stat[0][1] for stat in output}
    vac_salary_by_years = {stat[1][0]: stat[1][1] for stat in output}
    count_by_years = {stat[2][0]: stat[2][1] for stat in output}
    vac_count_by_years = {stat[3][0]: stat[3][1] for stat in output}
    stat_by_city = get_statistic_by_city(file)
    return [salary_by_years, vac_salary_by_years, count_by_years, vac_count_by_years, stat_by_city[0], stat_by_city[1]]


if __name__ == '__main__':
    file_name = input('Введите название файла: ')
    vacancy_name = input('Введите название профессии: ')
    area_name = input('Введите название региона: ')
    statistic = get_statistics(file_name, vacancy_name, area_name)
    print('Уровень зарплат по городам (в порядке убывания) - только первые 10 значений:', statistic[4])
    print('Доля вакансий по городам (в порядке убывания) - только первые 10 значений:', statistic[5])
    print('Динамика уровня зарплат по годам для выбранной профессии и региона:', statistic[1])
    print('Динамика количества вакансий по годам для выбранной профессии и региона:', statistic[3])
    report = Report()
    report.generate_excel(vacancy_name, statistic)
    report.generate_image(vacancy_name, statistic)
    report.generate_pdf(vacancy_name)