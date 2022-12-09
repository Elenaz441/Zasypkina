# Zasypkina

### Задание 2.3.2

Фото unit тестов (все пройдены):
![image](https://user-images.githubusercontent.com/102030455/205136537-b30ab401-24c0-460f-a017-a1eb62dc6094.png)

Фото doctest-ов:
![image](https://user-images.githubusercontent.com/102030455/205136825-668756d2-1e7e-499b-9131-9fd2cfbd38ac.png)


### Задание 2.3.3

Запустила профилизатор в PyCharm:
![image](https://user-images.githubusercontent.com/102030455/206177189-0388287c-473a-4898-874d-e117616e23b9.png)

Действительно, один из самых трудозатратных методов является форматирование даты
```py
def change_date(date_vac: str) -> str:
    """
    Форматирует дату публикации к нужному формату.

    Args:
        date_vac (str): Дата публикации.

    Returns:
        str: Отформатированная дата публикации.
    """
    return datetime.datetime.strptime(date_vac, '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y')
```

Далее заменила этот метод с помощью библиотеки dateutil
```py
def change_date(date_vac: str) -> str:
    """
    Форматирует дату публикации к нужному формату.

    Args:
        date_vac (str): Дата публикации.

    Returns:
        str: Отформатированная дата публикации.
    """
    return parse(date_vac).strftime('%d.%m.%Y')
```

Но метод начал работать ещё дольше (примерно в 5 раз)
![image](https://user-images.githubusercontent.com/102030455/206178814-a5cb69fb-8642-47b2-9598-804fd57ae049.png)

Далее решила попробовать сделать форматирование даты с помощью строк. Но такая реализация метода мне не очень нравится, так как стал менее читаемым (не очевидно само форматирование даты).
```py
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
```

Однако этот вариант показал себя лучше всего
![image](https://user-images.githubusercontent.com/102030455/206180361-0f06a8db-64d3-4b0e-8aa4-9413ce772d9b.png)

Но я всё равно решила оставить старую реализацию (с помощью datetime.strpftime), так как этот код наиболее понятен и читабелен.

Ещё одним трудозатратным методом в моей программе является clean_string:
```py
    def clean_string(self, raw_html: str) -> str:
        """
        Очищает строку от HTML кода

        Args:
            raw_html (str): Строка, которую нужно очистить

        Returns:
            str: Очищенная строка.
        """
        result = re.sub("<.*?>", '', raw_html)
        return result if '\n' in raw_html else " ".join(result.split())
```

Я попыталась переделать этот метод таким образом:
```py
    def clean_string(self, raw_html) -> str:
        """
        Очищает строку от HTML кода

        Args:
            raw_html (str): Строка, которую нужно очистить

        Returns:
            str: Очищенная строка.
        """
        while raw_html.find('<') > -1:
            index1 = raw_html.find('<')
            index2 = raw_html.find('>')
            raw_html = raw_html[:index1] + raw_html[index2 + 1:]
        return raw_html if '\n' in raw_html else " ".join(raw_html.split())
```
Однако эта реализация отработала примерно также как и прошлая:
![image](https://user-images.githubusercontent.com/102030455/206182022-2a099910-10bb-4cc4-bd87-e7d073de961b.png)

Поэтому я решила оставить прежнюю реализацию этого метода.