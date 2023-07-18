# Программа для создания и работы с базой данных HeadHunter
## Требования для работы программы
Для работы программы необходимо в папке src создать файл database.ini со следующим кодом,
а также установить необходимые библиотеки

<b>[postgresql]   
host=localhost  
user=postgres  
password=`Ваш пароль`  
port=5432</b>

<h2> Описание работы программы </h2>
В рамках программы проектируется база данных с работодателями, их вакансиями, а также с таблицами, данные которых
используются в качестве внешних ключей и зависимостей

Программа парсит все вакансии следующих компаний:
- Яндекс
- Магнит, розничная сеть
- Газпром нефть
- Лукойл
- Черкизово
- Ostin
- Алроса
- DNS
- Альфабанк
- Сеть аптек Апрель

С учетом ограничения пагинации API HH, максимальное количество вакансий от 1 работодателя составляет 2000.

В целях обхода на ограничение запросов и необходимости ввода капчи установлены временные паузы (0,5 сек) после каждой
страницы запроса информации о вакансиях (в основном необходимо вне рабочего времени).

При работе с БД доступны следующие методы:
- `get_companies_and_vacancies_count()`: получает список всех компаний и количество вакансий у каждой компании.
- `get_all_vacancies()`: получает список всех вакансий с указанием названия компании,
названия вакансии и зарплаты и ссылки на вакансию.
- `get_avg_salary()`: получает среднюю зарплату по вакансиям.
- `get_vacancies_with_higher_salary()`: получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
- `get_vacancies_with_keyword()`: получает список всех вакансий, в названии которых содержатся переданные в метод слова.

Для удобства пользования разработан модуль для взаимодействия с пользователем через консоль

<h2>Как установить</h2>

1. Склонируйте репозиторий к себе на компьютер с помощью команды git clone.  
2. Для установки зависимостей через requirements.txt используйте команду pip install -r requirements.txt.  
3. Для установки зависимостей через poetry.lock используйте команду poetry install.  