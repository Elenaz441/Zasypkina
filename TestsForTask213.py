import unittest
from Task213 import *


class MyTestCase(unittest.TestCase):
    def test_clean_string_html(self):
        self.assertEqual(DataSet('vacancies.csv').clean_string('<p>Группа компаний «МИАКОМ»</p>'), 'Группа компаний «МИАКОМ»')

    def test_clean_string_escaped_chars(self):
        self.assertEqual(DataSet('vacancies.csv').clean_string('wqerty\nqwer'), 'wqerty\nqwer')

    def test_clean_string_extra_spaces(self):
        self.assertEqual(DataSet('vacancies.csv').clean_string(f' try  do     it  '), 'try do it')

    def test_data_filter_currency(self):
        vac1 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Нет данных',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vac2 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Нет данных',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vac1, vac2]
        result = [vac2]
        self.assertEqual(InputConnect('', '', '', [0, 91], '').data_filter(vacancies, ['Идентификатор валюты оклада', 'Рубли']), result)

    def test_data_filter_salary(self):
        vac1 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Нет данных',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vac2 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Нет данных',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vac1, vac2]
        result = [vac1]
        self.assertEqual(InputConnect('', '', '', [0, 91], '').data_filter(vacancies, ['Оклад', '1000']), result)

    def test_data_filter_skills(self):
        vac1 = Vacancy({'name': 'Фронт-разработчик', 'description': 'Нет данных', 'key_skills': 'CSS\nHTML',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vac2 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'SQL\nPython\nGit',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vac1, vac2]
        result = [vac2]
        self.assertEqual(InputConnect('', '', '', [0, 91], '').data_filter(vacancies, ['Навыки', 'SQL, Git']), result)

    def test_data_sort_experience_id(self):
        vac1 = Vacancy({'name': 'Фронт-разработчик', 'description': 'Нет данных', 'key_skills': 'CSS\nHTML',
                        'experience_id': 'between1And3', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vac2 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'SQL\nPython\nGit',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vac3 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'SQL\nPython\nGit',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vac1, vac2, vac3]
        result = [vac2, vac3, vac1]
        self.assertEqual(InputConnect('', '', '', [0, 91], '').data_sort(vacancies, 'Опыт работы', False), result)

    def test_data_sort_salary_reversed(self):
        vac1 = Vacancy({'name': 'Фронт-разработчик', 'description': 'Нет данных', 'key_skills': 'CSS\nHTML',
                        'experience_id': 'between1And3', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vac2 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'SQL\nPython\nGit',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '10', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vac3 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'SQL\nPython\nGit',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vac1, vac2, vac3]
        result = [vac3, vac1, vac2]
        self.assertEqual(InputConnect('', '', '', [0, 91], '').data_sort(vacancies, 'Оклад', True), result)

    def test_data_sort_skills(self):
        vac1 = Vacancy({'name': 'Фронт-разработчик', 'description': 'Нет данных', 'key_skills': 'CSS\nHTML',
                        'experience_id': 'between1And3', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vac2 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'SQL\nPython\nGit\nMySQL',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '10', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vac3 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'SQL\nPython\nGit',
                        'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                        'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vac1, vac2, vac3]
        result = [vac1, vac3, vac2]
        self.assertEqual(InputConnect('', '', '', [0, 91], '').data_sort(vacancies, 'Навыки', False), result)

    def test_formatter_check1000(self):
        vac = Vacancy({'name': 'Фронт-разработчик', 'description': 'Нет данных', 'key_skills': 'CSS\nHTML',
                        'experience_id': 'between1And3', 'premium': 'True', 'employer_name': 'Нет данных',
                        'salary_from': '900', 'salary_to': '11000', 'salary_gross': 'True', 'salary_currency': 'EUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        result = ['Фронт-разработчик', 'Нет данных', 'CSS\nHTML', 'От 1 года до 3 лет', 'Да', 'Нет данных',
                  '900 - 11 000 (Евро) (Без вычета налогов)', 'Москва', '06.07.2022']
        self.assertEqual(InputConnect('', '', '', [0, 91], '').formatter(vac), result)

    def test_formatter_check_false(self):
        vac = Vacancy({'name': 'Фронт-разработчик', 'description': 'Нет данных', 'key_skills': 'CSS\nHTML',
                        'experience_id': 'between1And3', 'premium': 'False', 'employer_name': 'Нет данных',
                        'salary_from': '1000', 'salary_to': '11000', 'salary_gross': 'False', 'salary_currency': 'EUR',
                        'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        result = ['Фронт-разработчик', 'Нет данных', 'CSS\nHTML', 'От 1 года до 3 лет', 'Нет', 'Нет данных',
                  '1 000 - 11 000 (Евро) (С вычетом налогов)', 'Москва', '06.07.2022']
        self.assertEqual(InputConnect('', '', '', [0, 91], '').formatter(vac), result)



if __name__ == '__main__':
    unittest.main()
