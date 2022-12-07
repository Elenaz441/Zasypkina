# Zasypkina

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

