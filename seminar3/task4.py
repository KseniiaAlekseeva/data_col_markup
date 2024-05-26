# Импорт необходимых библиотек
import pandas as pd # Импорт библиотеки pandas для работы с данными в табличном виде
from clickhouse_driver import Client # Импорт класса Client из библиотеки clickhouse_driver для работы с базой данных ClickHouse
from datetime import datetime # Импорт класса datetime из модуля datetime для работы с датами и временем

# Подключение к серверу ClickHouse
client = Client('localhost') # Создание клиента для подключения к серверу ClickHouse, работающему локально

# 1. Выполнение базового запроса для получения всех записей из таблицы 'crashes'
records = client.execute('SELECT * FROM town_cary.crashes') # Выполнение SQL-запроса к базе данных для получения всех записей из таблицы 'crashes'
df_records = pd.DataFrame(records, columns=['id', 'location_description', 'rdfeature', 'rdsurface', 'rdcondition', 'lightcond', 'weather', 'crash_date', 'year', 'fatalities', 'injuries', 'month']) # Преобразование полученных записей в DataFrame с указанием названий столбцов
df_records.head() # Вывод первых пяти записей DataFrame для предварительного просмотра

# 2. Фильтрация записей на основе критериев
# 2.1. Равенство: Получение записей с fatalities, равным 'Yes'
fatal_records = client.execute("SELECT * FROM town_cary.crashes WHERE fatalities = 'Yes'") # Выполнение запроса на выборку записей, где поле fatalities равно 'Yes'
df_fatal_records = pd.DataFrame(fatal_records, columns=df_records.columns) # Преобразование результатов запроса в DataFrame
df_fatal_records.head() # Вывод первых пяти записей отфильтрованного DataFrame

# 2.2. Равенство: Получение записей с годом, равным '2021'
records_2021 = client.execute("SELECT * FROM town_cary.crashes WHERE year == '2021'") # Выполнение запроса на выборку записей за 2021 год (исправить на year = '2021')
df_2021_records = pd.DataFrame(records_2021, columns=df_records.columns) # Преобразование результатов запроса в DataFrame (исправить переменную на records_2021)
df_2021_records.head() # Вывод первых пяти записей отфильтрованного DataFrame

# 2.3. Диапазон: Выборка записей с датой аварии между двумя временными метками
start_timestamp = 1627560000 # Начальная временная метка для фильтрации
end_timestamp = 1627565000 # Конечная временная метка для фильтрации
range_records = client.execute(f"SELECT * FROM town_cary.crashes WHERE crash_date BETWEEN {start_timestamp} AND {end_timestamp}") # Выполнение запроса на выборку записей по диапазону дат
df_range_records = pd.DataFrame(range_records, columns=df_records.columns) # Преобразование результатов запроса в DataFrame
# Изменение формата даты
df_range_records['crash_date'] = df_range_records['crash_date'].apply(lambda ts: datetime.fromtimestamp(ts).strftime('%Y-%m-%d')) # Преобразование временных меток в формат даты 'YYYY-MM-DD'
df_range_records # Вывод обновленного DataFrame

# 3. Сортировка записей на основе одного или нескольких полей
# 3.1. Сортировка записей по дате аварии в порядке убывания
sorted_records = client.execute("SELECT * FROM town_cary.crashes ORDER BY crash_date DESC") # Выполнение запроса на сортировку записей по дате аварии в порядке убывания
df_sorted_records = pd.DataFrame(sorted_records, columns=df_records.columns) # Преобразование результатов запроса в DataFrame
df_sorted_records.head() # Вывод первых пяти записей отсортированного DataFrame

# 3.2. Сортировка записей по году в порядке возрастания и по дате аварии в порядке убывания
multi_sorted_records = client.execute("SELECT * FROM town_cary.crashes ORDER BY year ASC, crash_date DESC") # Выполнение запроса на сортировку записей сначала по году (возрастание), затем по дате аварии (убывание)
df_multi_sorted_records = pd.DataFrame(multi_sorted_records, columns=df_records.columns) # Преобразование результатов запроса в DataFrame
df_multi_sorted_records.head() # Вывод первых пяти записей отсортированного DataFrame

# 4. Агрегирование записей с помощью таких функций, как count, sum и avg.
# 4.1. Подсчет общего количества записей
count_records = client.execute("SELECT COUNT(*) FROM town_cary.crashes") # Выполнение запроса на подсчет общего количества записей в таблице 'crashes'
print("Общее количество записей:", count_records[0][0]) # Вывод общего количества записей

# 4.2. Подсчет количества записей за каждый год
year_count_records = client.execute("SELECT year, COUNT(*) FROM town_cary.crashes GROUP BY year") # Выполнение запроса на подсчет количества записей за каждый год с группировкой по году
df_year_count_records = pd.DataFrame(year_count_records, columns=['year', 'count']) # Преобразование результатов запроса в DataFrame
df_year_count_records # Вывод DataFrame с количеством записей за каждый год

# 4.3. Рассчитайте среднюю дату ДТП для записей с injuries = 'Yes'
avg_crash_date = client.execute("SELECT AVG(crash_date) FROM town_cary.crashes WHERE injuries = 'Yes'") # Выполнение запроса на расчет средней даты ДТП для записей с травмами
date_object = datetime.fromtimestamp(avg_crash_date[0][0]) # Преобразование средней временной метки в объект datetime
date_string = date_object.strftime('%Y-%m-%d') # Преобразование объекта datetime в строку с датой
print("Средняя дата ДТП для записей с травмами:", date_string) # Вывод средней даты ДТП