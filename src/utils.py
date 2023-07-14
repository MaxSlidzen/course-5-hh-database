import requests
import psycopg2


def get_employers_ids(employers: list) -> list:
    """
    Создание списка c id работодателей
    :param employers: Список с названиями компаний,
    :return: Список с id компаний из списка с названиями
    """
    # Итерация по списку с названиями
    start_employers_ids = []
    for employer_name in employers:
        response = requests.get('https://api.hh.ru/employers',
                                params={'text': {employer_name}})
        employers = response.json()

        # В случае ответа с несколькими компаниями (подразделения/схожие названия),
        # выбор одной с наибольшим количеством вакансий
        needed_employer = None
        open_vacancies = 0
        for employer in employers['items']:
            if employer['open_vacancies'] > open_vacancies:
                needed_employer = employer
                open_vacancies = employer['open_vacancies']

        # Добавление id компании в список
        start_employers_ids.append(needed_employer['id'])

    return start_employers_ids


def to_strip_date(date_str: str):
    """
    Возвращает дату публикации без указания времени

    :param date_str:
    :return: дата в формате гггг-мм-дд
    """
    stripped_date = date_str.split("T")[0]
    return stripped_date


def get_hh_salary(raw_vacancy: dict) -> int:
    """
    Возвращает величину зарплаты для вакансий HH

    :param raw_vacancy: "сырой" словарь с данными о вакансии HH
    :return: величина зарплаты
    """
    if raw_vacancy["salary"] is None:
        return 0
    elif raw_vacancy["salary"]["from"] is None:
        return raw_vacancy["salary"]["to"]
    return raw_vacancy["salary"]["from"]


def get_hh_vacancies_params(raw_vacancy: dict) -> list:
    """
    Возвращает параметры для вакансий HH

    :param raw_vacancy: "сырой" словарь с данными о вакансии HH
    :return: параметры для вакансий HH
    """
    salary = get_hh_salary(raw_vacancy)
    if salary > 0:
        currency = raw_vacancy["salary"]["currency"]
    else:
        currency = ""

    return [
        raw_vacancy["id"],
        raw_vacancy["name"],
        raw_vacancy["employer"]['id'],
        raw_vacancy["employer"]['name'],
        raw_vacancy["alternate_url"],
        raw_vacancy["area"]["name"],
        salary,
        currency,
        to_strip_date(raw_vacancy["published_at"])
    ]


def create_database(database_name: str, params: dict) -> None:
    """
    Создание базы данных и таблиц для сохранения данных о каналах и видео
    :param database_name: Название создаваемой БД
    :param params: параметры подключения к БД (postgres)
    """

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')
    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE employers 
                    (
                        employer_id INTEGER PRIMARY KEY,
                        accredited_IT VARCHAR(3) NOT NULL,
                        employer_name VARCHAR(50) NOT NULL,
                        employer_site VARCHAR,
                        employer_hh_link VARCHAR NOT NULL,
                        industries VARCHAR,
                        open_vacancies INTEGER NOT NULL
                    )
                    """)

    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE vacancies
                    (
                        vacancy_id INTEGER PRIMARY KEY,
                        vacancy_name INTEGER NOT NULL,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        employer_name VARCHAR REFERENCES employers(employer_name),
                        vacancy_link VARCHAR NOT NULL,
                        area VARCHAR NOT NULL,
                        salary INTEGER,
                        currency VARCHAR,
                        published DATE NOT NULL,
                    )
                    """)
    conn.commit()
    conn.close()
