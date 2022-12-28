import pandas as pd
import sqlite3

conn = sqlite3.connect('project_vacancy.db')
vacancy = input('Введите название вакансии: ')
df1 = pd.read_sql("""select strftime('%Y',published_at) as date, round(avg(salary)) as avg_salary 
                        from vacancies 
                        group by strftime('%Y',published_at)""", conn)
df2 = pd.read_sql("""select strftime('%Y',published_at) as date, count(salary) as count 
                        from vacancies 
                        group by strftime('%Y',published_at)""", conn)
df3 = pd.read_sql(f"""select strftime('%Y',published_at) as date, round(avg(salary)) as avg_salary 
                        from vacancies
                        where name like '%{vacancy}%' 
                        group by strftime('%Y',published_at)""", conn)
df4 = pd.read_sql(f"""select strftime('%Y',published_at) as date, count(salary) as count 
                        from vacancies
                        where name like '%{vacancy}%' 
                        group by strftime('%Y',published_at)""", conn)
df5 = pd.read_sql("""select area_name, avg from
                        (select area_name, round(avg(salary)) as avg, count(salary) as count
                        from vacancies
                        group by area_name
                        order by avg desc)
                    where count > (select count(*) from vacancies) * 0.01
                    limit 10""", conn)
df6 = pd.read_sql("""select area_name,
                        round(cast(count as real) / (select count(*) from vacancies), 4) as percent from
                        (select area_name, count(salary) as count
                        from vacancies
                        group by area_name
                        order by count desc)
                        limit 10""", conn)
pd.set_option('expand_frame_repr', False)
print('Динамика уровня зарплат по годам \n', df1)
print('Динамика количества вакансий по годам \n', df2)
print('Динамика уровня зарплат по годам для выбранной профессии \n', df3)
print('Динамика количества вакансий по годам для выбранной профессии \n', df4)
print('Уровень зарплат по городам (в порядке убывания) - только первые 10 значений \n', df5)
print('Доля вакансий по городам (в порядке убывания) - только первые 10 значений \n', df6)