import csv, re, os
from datetime import datetime
from typing import List, Dict, Tuple, Any
from prettytable import PrettyTable, ALL
from cProfile import Profile
from pstats import Stats

prof = Profile()
prof.disable()


currency_to_rub = {"AZN": 35.68,
                   "BYR": 23.91,
                   "EUR": 59.90,
                   "GEL": 21.74,
                   "KGS": 0.76,
                   "KZT": 0.13,
                   "RUR": 1,
                   "UAH": 1.64,
                   "USD": 60.66,
                   "UZS": 0.0055, }

translation = {"name": "Название",
               "description": "Описание",
               "key_skills": "Навыки",
               "experience_id": "Опыт работы",
               "premium": "Премиум-вакансия",
               "employer_name": "Компания",
               "salary_from": "Нижняя граница вилки оклада",
               "salary_to": "Верхняя граница вилки оклада",
               "salary_gross": "Оклад указан до вычета налогов",
               "salary_currency": "Идентификатор валюты оклада",
               "area_name": "Название региона",
               "published_at": "Дата публикации вакансии",
               "Оклад": "Оклад",
               "Нет данных": "Нет данных",
               "True": "Да",
               "TRUE": "Да",
               "False": "Нет",
               "FALSE": "Нет",
               "noExperience": "Нет опыта",
               "between1And3": "От 1 года до 3 лет",
               "between3And6": "От 3 до 6 лет",
               "moreThan6": "Более 6 лет",
               "AZN": "Манаты",
               "BYR": "Белорусские рубли",
               "EUR": "Евро",
               "GEL": "Грузинский лари",
               "KGS": "Киргизский сом",
               "KZT": "Тенге",
               "RUR": "Рубли",
               "UAH": "Гривны",
               "USD": "Доллары",
               "UZS": "Узбекский сум"}

reverse_translation = {"Название": "name",
                       "Описание": "description",
                       "Навыки": "key_skills",
                       "Опыт работы": "experience_id",
                       "Премиум-вакансия": "premium",
                       "Компания": "employer_name",
                       "Оклад": "Оклад",
                       "Название региона": "area_name",
                       "Дата публикации вакансии": "published_at",
                       "Идентификатор валюты оклада": "salary_currency"}

rang_experience_id = {"noExperience": 0,
                      "between1And3": 1,
                      "between3And6": 2,
                      "moreThan6": 3}


class InputConnect:
    """
    Формирование таблицы PrettyTable с удобным отображением информации о вакансии.

    Attributes:
        filter_param (str or List[str]): Параметр фильтрации
        sort_param (str): Параметр сортировки
        reversed_sort (str or bool): Параметр обратной сортировки
        interval (List[int]): Промежуток выводимых колонок
        columns (str or List[str]): Название выводимых колонок
    """

    def __init__(self, filter_param, sort_param, reversed_sort, interval, columns):
        """
        Инициализирует объект InputConnect

        Args:
            filter_param (str): Параметр фильтрации
            sort_param (str): Параметр сортировки
            reversed_sort (str or bool): Параметр обратной сортировки
            interval (List[int]): Промежуток выводимых колонок
            columns (str or List[str]): Название выводимых колонок
        """
        self.filter_param = filter_param
        self.sort_param = sort_param
        self.reversed_sort = reversed_sort
        self.interval = interval
        self.columns = columns

    def check_parameters(self) -> None:
        """
        Проверка параметров на корректность ввода.
        """
        if ': ' not in self.filter_param and self.filter_param != '':
            exit_from_file('Формат ввода некорректен')
        self.filter_param = self.filter_param.split(': ')
        if len(self.filter_param) == 2 and self.filter_param[0] not in list(translation.values()):
            exit_from_file('Параметр поиска некорректен')
        if self.sort_param != '' and self.sort_param not in list(translation.values()):
            exit_from_file('Параметр сортировки некорректен')
        if self.reversed_sort not in ['Да', 'Нет', '']:
            exit_from_file('Порядок сортировки задан некорректно')
        self.reversed_sort = (self.reversed_sort == 'Да')
        if len(self.columns) != 0:
            self.columns = self.columns.split(', ')
            self.columns.insert(0, '№')

    def formatter(self, vacancy: Any) -> List[Any]:
        """
        Осуществляет форматирование необходимых полей.

        Args:
            vacancy (Vacancy): Вакансия.

        Returns:
            List[Any]: Список отформатированных полей.
        """

        def change_salary(salary: Any) -> str:
            """
            Форматирует зарплату к нужному формату.

            Args:
                salary (Salary): Информация о зарплате.

            Returns:
                str: Отформатированная информация о зарплате.
            """
            salary_from = int(float(salary.salary_from))
            salary_to = int(float(salary.salary_to))
            if salary_from >= 1000:
                salary_from = f'{salary_from // 1000} {str(salary_from)[-3:]}'
            if salary_to >= 1000:
                salary_to = f'{salary_to // 1000} {str(salary_to)[-3:]}'
            info_gross = 'Без вычета налогов' if translation[salary.salary_gross] == 'Да' else 'С вычетом налогов'
            result_salary = f'{salary_from} - {salary_to} ({translation[salary.salary_currency]}) ({info_gross})'
            return result_salary

        return [vacancy.name, vacancy.description, '\n'.join(vacancy.key_skills), translation[vacancy.experience_id],
                translation[vacancy.premium], vacancy.employer_name, change_salary(vacancy.salary), vacancy.area_name,
                change_date(vacancy.published_at)]

    def data_filter(self, list_vacancies: List[Any], parameter: List[str]) -> List[Any]:
        """
        Фильтрует список вакансий по введённым параметрам.

        Args:
            list_vacancies (List[Vacancy]): Список вакансий.
            parameter (List[str]): Параметры фильтрации.

        Returns:
            List[Vacancy]: Список отфильтрованных вакансий.
        """
        if parameter[0] == 'Навыки':
            parameter[1] = parameter[1].split(', ')
        if parameter[0] == 'Оклад':
            list_vacancies = list(
                filter(lambda vac: int(vac.salary.salary_from) <= int(parameter[1]) <= int(vac.salary.salary_to),
                       list_vacancies))
        elif parameter[0] == 'Навыки':
            list_vacancies = list(
                filter(lambda vac: all(item in vac.key_skills for item in parameter[1]), list_vacancies))
        elif parameter[0] == 'Опыт работы' or parameter[0] == 'Премиум-вакансия':
            list_vacancies = list(
                filter(lambda vac: parameter[1] == translation[vac.__getattribute__(reverse_translation[parameter[0]])],
                       list_vacancies))
        elif parameter[0] == 'Идентификатор валюты оклада':
            list_vacancies = list(
                filter(lambda vac: parameter[1] == translation[vac.salary.salary_currency], list_vacancies))
        elif parameter[0] == 'Дата публикации вакансии':
            list_vacancies = list(filter(lambda vac: parameter[1] == change_date(vac.published_at), list_vacancies))
        else:
            list_vacancies = list(
                filter(lambda vac: parameter[1] == vac.__getattribute__(reverse_translation[parameter[0]]),
                       list_vacancies))
        return list_vacancies

    def data_sort(self, list_vacancies: List[Any], param: str, is_reverse: bool) -> List[Any]:
        """
        Сортирует список вакансий по введённым параметрам.

        Args:
            list_vacancies (List[Vacancy]): Список вакансий.
            param (str): Параметр сортировки.
            is_reverse (bool): Параметр обратной сортировки.

        Returns:
            List[Vacancy]: Список отсортированных вакансий.
        """
        if param == 'Навыки':
            list_vacancies.sort(key=lambda vac: len(vac.key_skills), reverse=is_reverse)
        elif param == 'Оклад':
            list_vacancies.sort(
                key=lambda vac: vac.salary.to_RUB(float(vac.salary.salary_from) + float(vac.salary.salary_to)) / 2,
                reverse=is_reverse)
        elif param == 'Дата публикации вакансии':
            # parse(vac.published_at).strftime('%Y-%m-%dT%H:%M:%S%z')
            list_vacancies.sort(key=lambda vac: (datetime.datetime.strptime(vac.published_at, '%Y-%m-%dT%H:%M:%S%z')),
                                reverse=is_reverse)
        elif param == 'Опыт работы':
            list_vacancies.sort(key=lambda vac: rang_experience_id[vac.experience_id], reverse=is_reverse)
        else:
            list_vacancies.sort(key=lambda vac: vac.__getattribute__(reverse_translation[param]), reverse=is_reverse)
        return list_vacancies

    def print_vacancies(self, list_vacancies: List[Any]) -> None:
        """
        Выводит информацию о вакансии в таблицу PrettyTable

        Args:
            list_vacancies (List[Vacancy]): Список вакансий.
        """
        self.interval.append(len(list_vacancies) + 1)
        list_vacancies = list_vacancies if len(self.filter_param) != 2 else self.data_filter(list_vacancies,
                                                                                             self.filter_param)
        list_vacancies = list_vacancies if len(list_vacancies) != 0 else 'Ничего не найдено'
        if type(list_vacancies) is str:
            print(list_vacancies)
            return
        list_vacancies = list_vacancies if len(self.sort_param) == 0 else self.data_sort(list_vacancies,
                                                                                         self.sort_param,
                                                                                         self.reversed_sort)
        table_header = list(reverse_translation.keys())[:-1]
        table_header.insert(0, '№')
        vacans_table = PrettyTable(table_header)
        vacans_table.hrules = ALL
        for i in range(len(list_vacancies)):
            vac = self.formatter(list_vacancies[i])
            vac = list(map(lambda i: f'{i[:100]}...' if len(i) > 100 else i, vac))
            vac.insert(0, i + 1)
            vacans_table.add_row(vac)
        vacans_table.align = 'l'
        vacans_table.max_width = 20
        if len(self.interval) > 1 and len(self.columns) >= 2:
            vacans_table = vacans_table.get_string(start=self.interval[0] - 1, end=self.interval[1] - 1,
                                                   fields=self.columns)
        elif len(self.interval) > 1:
            vacans_table = vacans_table.get_string(start=self.interval[0] - 1, end=self.interval[1] - 1)
        elif len(self.columns) >= 2:
            vacans_table = vacans_table.get_string(fields=self.columns)
        print(vacans_table)


def change_date(date_vac: str) -> str:
    """
    Форматирует дату публикации к нужному формату.

    Args:
        date_vac (str): Дата публикации.

    Returns:
        str: Отформатированная дата публикации.
    """
    date = date_vac[:date_vac.find('T')].split('-')
    return '.'.join(reversed(date))


def exit_from_file(message: str):
    """
    Метод для выхода из программы.

    Args:
        message (str): Сообщение при выходе из программы
    """
    print(message)
    exit()