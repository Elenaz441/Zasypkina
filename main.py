import csv, re, os
from typing import List, Dict, Tuple
from cProfile import Profile
from pstats import Stats
from vacancy import InputConnect
from statistic import Report, get_statistic, get_salary_level, get_count_vacancies, print_statistic
from Task322 import get_stat_by_year

prof = Profile()
prof.disable()


class DataSet:
    """
    Класс для формирования списка вакансий.

    Attributes:
        file_name (str): Название файла.
        vacancies_objects (List[Vacancy]): Сформированный список вакансий.

    """

    def __init__(self, file_name: str) -> None:
        """
        Инициализирует объект DataSet.

        Args:
            file_name (str): Имя файла.
        """
        self.file_name = file_name
        self.vacancies_objects = [Vacancy(vac) for vac in self.csv_filer(*self.csv_reader(file_name))]

    def clean_string(self, raw_html: str) -> str:
        """
        Очищает строку от HTML кода

        Args:
            raw_html (str): Строка, которую нужно очистить

        Returns:
            str: Очищенная строка.

        >>> DataSet('vacancies.csv').clean_string('<p>Группа компаний «МИАКОМ»</p>')
        'Группа компаний «МИАКОМ»'
        """
        result = re.sub("<.*?>", '', raw_html)
        return result if '\n' in raw_html else " ".join(result.split())

    def csv_reader(self, file_name: str) -> Tuple[List[str], List[List[str]]]:
        """
        Считывает данные из файла

        Args:
            file_name (str): Название файла.

        Returns:
            Tuple[List[str], List[List[str]]]: Название колонок и соответствующие им данные по каждой вакансии.
        """
        reader = csv.reader(open(file_name, encoding='utf_8_sig'))
        data_base = [line for line in reader]
        return data_base[0], data_base[1:]

    def csv_filer(self, list_naming: List[str], reader: List[List[str]]) -> List[Dict[str, str]]:
        """
        Преобразует данные в список словарей, где словарь содержит информацию об одной вакансии.

        Args:
            list_naming (List[str]): Поля вакансии
            reader (List[List[str]]): Данные из файла

        Returns:
            List[Dict[str, str]]: Список словарей.
        """
        new_vacans_list = list(filter(lambda vac: (len(vac) == len(list_naming) and vac.count('') == 0), reader))
        return [dict(zip(list_naming, map(self.clean_string, vac))) for vac in new_vacans_list]


class Vacancy:
    """
    Класс для представления вакансии

    Attributes:
        name (string): Название вакансии
        description (str): Описание вакансии
        key_skills (List[str]): Ключевые навыки для вакансии
        experience_id (str): Требуемый опят для вакансии
        premium (str): Атрибут, отвечающий за премиальность вакансии
        employer_name (str): Название компании, где есть вакансия
        salary (Salary): Информация о зарплате
        area_name (str): Название города
        published_at (str): Дата публикации вакансии
    """

    def __init__(self, dict_vac: Dict[str, str]):
        """
        Инициализирует объект Vacancy, проверяя наличие некоторых полей для вакансии

        Args: dict_vac (Dict[str, str]): Словарь, хранящий информацию о вакансии. Ключи - это названия полей,
        значения - информация о вакансии по соответствующему полю.
        """
        self.name = dict_vac['name']
        self.description = 'Нет данных' if 'description' not in dict_vac.keys() else dict_vac['description']
        self.key_skills = 'Нет данных' if 'key_skills' not in dict_vac.keys() else dict_vac['key_skills'].split('\n')
        self.experience_id = 'Нет данных' if 'experience_id' not in dict_vac.keys() else dict_vac['experience_id']
        self.premium = 'Нет данных' if 'premium' not in dict_vac.keys() else dict_vac['premium']
        self.employer_name = 'Нет данных' if 'employer_name' not in dict_vac.keys() else dict_vac['employer_name']
        salary_gross = 'Нет данных' if 'salary_gross' not in dict_vac.keys() else dict_vac['salary_gross']
        self.salary = Salary(dict_vac['salary_from'], dict_vac['salary_to'], salary_gross, dict_vac['salary_currency'])
        self.area_name = dict_vac['area_name']
        self.published_at = dict_vac['published_at']


class Salary:
    """
    Класс для представления зарплаты.

    Attributes:
        salary_from (str): Нижняя граница зарплаты
        salary_to (str): Верхняя граница зарплаты
        salary_gross (str): Наличие налогов
        salary_currency (str): Валюта оклада

    """

    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """
        Инициализирует объект Salary
        Args:
            salary_from (str): Нижняя граница зарплаты
            salary_to (str): Верхняя граница зарплаты
            salary_gross (str): Наличие налогов
            salary_currency (str): Валюта оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    def to_RUB(self, salary: float) -> float:
        """
        Вычисляет зарплату в рублях, при помощи словаря - currency_to_rub.

        Args:
            salary (float): Зарплата в другой валюте.

        Returns:
            float: Зарплата в рублях.

        # >>> Salary('10', '1000', 'true', 'EUR').to_RUB(1000.0)
        # 59900.0
        # >>> Salary('10', '1000', 'true', 'RUR').to_RUB(1000)
        # 1000.0
        # >>> Salary('10', '1000', 'true', 'QWE').to_RUB(1000.0)
        >>> Salary('10', '1000', 'false', 'EUR').to_RUB(559)
        33484.1
        >>> Salary('10', '1000', 'true', 'RUR').to_RUB(500)
        500.0
        >>> Salary('10', '1000', 'true', 'QWE').to_RUB(1000.0)
        Traceback (most recent call last):
        ...
        KeyError: 'QWE'
        """
        return float(salary * currency_to_rub[self.salary_currency])


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


def get_year(date_vac) -> str:
    """
    Возвращает год от даты.

    Args:
        date_vac (str): Дата публикации.

    Returns:
        str: Год публикации.
    """
    return date_vac[:4]


def exit_from_file(message: str):
    """
    Метод для выхода из программы.

    Args:
        message (str): Сообщение при выходе из программы
    """
    print(message)
    exit()


if __name__ == '__main__':
    type_output = input('Введите данные для печати: ')
    file_name = input('Введите название файла: ')
    if os.stat(file_name).st_size == 0:
        exit_from_file('Пустой файл')
    prof.enable()
    data = DataSet(file_name)
    prof.disable()
    if len(data.vacancies_objects) == 0:
        exit_from_file('Нет данных')
    if type_output == 'Статистика':
        vacancy_name = input('Введите название профессии: ')
        prof.enable()
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
        rp = Report()
        stat_by_years = get_stat_by_year(file_name, vacancy_name)
        print('Динамика уровня зарплат по годам:', stat_by_years[0])
        print('Динамика уровня зарплат по годам для выбранной профессии:', stat_by_years[1])
        print('Динамика количества вакансий по годам:', stat_by_years[2])
        print('Динамика количества вакансий по годам для выбранной профессии:', stat_by_years[3])
        list_statistic = [stat_by_years[0],
                          stat_by_years[1],
                          stat_by_years[2],
                          stat_by_years[3],
                          print_statistic(get_salary_level(needed_vacancies_objects, 'area_name').items(), 1,
                                          'Уровень зарплат по городам (в порядке убывания): ', True, 10),
                          print_statistic(get_count_vacancies(needed_vacancies_objects, 'area_name', data).items(), 1,
                                          'Доля вакансий по городам (в порядке убывания): ', True, 10)]
        rp.generate_excel(vacancy_name, list_statistic)
        rp.generate_image(vacancy_name, list_statistic)
        rp.generate_pdf(vacancy_name)
        prof.disable()
    elif type_output == 'Вакансии':
        parameter = input('Введите параметр фильтрации: ')
        sorting_param = input('Введите параметр сортировки: ')
        is_reversed_sort = input('Обратный порядок сортировки (Да / Нет): ')
        interval = list(map(int, input('Введите диапазон вывода: ').split()))
        columns = input('Введите требуемые столбцы: ')
        prof.enable()
        outer = InputConnect(parameter, sorting_param, is_reversed_sort, interval, columns)
        outer.check_parameters()
        outer.print_vacancies(data.vacancies_objects)
        prof.disable()
    prof.dump_stats('async')
    with open('async_stats.txt', 'wt') as _output:
        stats = Stats('async', stream=_output)
        stats.sort_stats('cumulative', 'time')
        stats.print_stats()

