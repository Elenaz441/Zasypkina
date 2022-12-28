from multiprocessing import Pool
from typing import List, Dict, Tuple, Any
import pandas as pd
from functools import partial
from statistic import Report, get_salary_level, get_count_vacancies, get_statistic
from main import DataSet, get_year


def get_statistic_by_year(file: str, vacancy: str, statistics: List[Dict[int, Any]]) -> List[Dict[int, Any]]:
    """
    Преобразовывает статистики для конкретного года

    Args:
        file (str): Название файла
        vacancy (str): Название вакансии
        statistics (List[Dict[int, Any]]): Список статистик по годам

    Returns:
        List[Dict[int, Any]]: Список статистик по годам.
    """
    df = pd.read_csv(file)
    df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
    year = int(file[15:19])
    statistics[0] = (year, int(df['salary'].mean()))
    statistics[1] = (year, int(df[df['name'] == vacancy]['salary'].mean()))
    statistics[2] = (year, len(df))
    statistics[3] = (year, len(df[df['name'] == vacancy]))
    return statistics


def get_stat_by_years(file, vacancy):
    """
    Возвращает статистики по годам

    Args:
        file (str): Название файла
        vacancy (str): Название вакансии

    Returns:
        List[Dict[int, Any]]: Список статистик по годам.
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


if __name__ == '__main__':
    file_name = input('Введите название файла: ')
    vacancy_name = input('Введите название профессии: ')
    statistic = get_stat_by_years(file_name, vacancy_name)
    data = DataSet(file_name)
    for vac in data.vacancies_objects:
        vac.published_at = get_year(vac.published_at)
    dict_cities = {}
    for vac in data.vacancies_objects:
        if vac.area_name not in dict_cities.keys():
            dict_cities[vac.area_name] = 0
        dict_cities[vac.area_name] += 1
    needed_vacancies_objects = list(
        filter(lambda vac: int(len(data.vacancies_objects) * 0.01) <= dict_cities[vac.area_name],
               data.vacancies_objects))
    print('Динамика уровня зарплат по годам:', statistic[0])
    print('Динамика уровня зарплат по годам для выбранной профессии:', statistic[1])
    print('Динамика количества вакансий по годам:', statistic[2])
    print('Динамика количества вакансий по годам для выбранной профессии:', statistic[3])
    statistic.append(get_statistic(get_salary_level(needed_vacancies_objects, 'area_name').items(), 1, True, 10))
    statistic.append(get_statistic(get_count_vacancies(needed_vacancies_objects, 'area_name', data).items(), 1, True, 10))
    report = Report()
    report.generate_excel(vacancy_name, statistic)
    report.generate_image(vacancy_name, statistic)
    report.generate_pdf(vacancy_name)