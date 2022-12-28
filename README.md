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

### Задание 3.2.1

В результате сформировались эти файлы.

![image](https://user-images.githubusercontent.com/102030455/206720182-494b709f-d1d5-4472-90ee-f620c95661ae.png)

### Задание 3.2.2
 Время работы файла без многополочночти:
 ![image](https://user-images.githubusercontent.com/102030455/206901250-0e3dfdf6-27e8-4911-ab31-50bc2dea451f.png)

Время работы файла с многопоточностью:
![image](https://user-images.githubusercontent.com/102030455/206901276-bb97e2c0-b93b-4daf-87d0-ead70ad2aa8d.png)

Видно, что файл с многопоточностью работает быстрее примерно на 10 секунд.


### Задание 3.2.3
Время работы файла с Concurrent futures:
![image](https://user-images.githubusercontent.com/102030455/208096172-222602bc-2d42-427f-ba99-4b1b77868e6b.png)

Время работы файла с Concurrent futures:
Если сравнивать с multiprocessing, то Concurrent futures работает медленнее

### Задание 3.3.1
Частотность с которой встречаются различные валюты, за 2003 – 2022 гг.
![1](https://user-images.githubusercontent.com/102030455/208485010-c7fde94e-af49-4630-8b37-c632a9018042.jpg)

### Задание 3.3.2
Сформировала csv-файл с первыми 100 строками (отображение через MS Excel):
![image](https://user-images.githubusercontent.com/102030455/208904890-65d432ae-7263-4c07-acb5-3aa72db7a8a6.png)
![image](https://user-images.githubusercontent.com/102030455/208905083-331f5503-d876-4a73-95ff-6f278239b267.png)
![image](https://user-images.githubusercontent.com/102030455/208905126-9c7af352-ac1f-40d3-80f8-a8484abc9c5e.png)
![image](https://user-images.githubusercontent.com/102030455/208905166-4cc3ed31-2ecf-4a7d-9d06-5bda7dc9f8af.png)

### Задание 3.5.1
Создана база данных, в которой сформирована таблица валют из csv-файла:
![image](https://user-images.githubusercontent.com/102030455/209675225-352b80dd-7c77-46cb-9fb2-8fd41c160a0f.png)

### Задание 3.5.2
Создала таблицу в базе данных с вакансиями
![image](https://user-images.githubusercontent.com/102030455/209799445-811ef406-2859-45d5-860c-0edea838dc7d.png)


