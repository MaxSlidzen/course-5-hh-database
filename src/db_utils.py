import psycopg2
from typing import Any
from src.hh_data_utils import get_hh_salary, to_strip_date


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
                    CREATE TABLE areas
                    (
                        city_id INTEGER PRIMARY KEY,
                        city VARCHAR,
                        region VARCHAR,
                        country VARCHAR NOT NULL
                    )
                    """)

    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE industries
                    (
                        industry_id REAL PRIMARY KEY,
                        name VARCHAR NOT NULL
                    )
                    """)

    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE currencies
                    (
                        id SERIAL PRIMARY KEY,
                        code VARCHAR(3) UNIQUE,
                        name VARCHAR(20) NOT NULL,
                        rate REAL
                    )
                    """)

    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE employers 
                    (
                        employer_id INTEGER PRIMARY KEY,
                        accredited_IT BOOLEAN,
                        employer_name VARCHAR(50) NOT NULL UNIQUE,
                        employer_site VARCHAR,
                        employer_hh_link VARCHAR NOT NULL,
                        industry REAL REFERENCES industries(industry_id),
                        open_vacancies INTEGER NOT NULL
                    )
                    """)

    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE vacancies
                    (
                        vacancy_id INTEGER PRIMARY KEY,
                        vacancy_name VARCHAR NOT NULL,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        employer_name VARCHAR REFERENCES employers(employer_name),
                        vacancy_link VARCHAR NOT NULL,
                        area_id INTEGER REFERENCES areas(city_id),
                        salary INTEGER,
                        currency VARCHAR,
                        published DATE NOT NULL
                    )
                    """)
    conn.commit()
    conn.close()


def save_data_to_database(data: dict[str, list[dict[str, Any]]], database_name: str, params: dict) -> None:
    """
    Сохранение данных c HH в базу данных
    :param data: словарь с данными
    :param database_name: название БД для HH
    :param params: параметры для входа в БД
    :return:
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for area in data['areas']:
            cur.execute(
                """
                INSERT INTO areas (city_id, city, region, country)
                VALUES (%s, %s, %s, %s)
                """,
                (int(area['id']), area['name'], area['region'], area['country'])
            )

        for currency in data['currencies']:
            cur.execute(
                """
                INSERT INTO currencies (code, name, rate)
                VALUES (%s, %s, %s)
                """,
                (currency['currency_code'], currency['currency_name'], currency['currency_rate'])
            )

        for industry in data['industries']:
            cur.execute(
                """
                INSERT INTO industries (industry_id, name)
                VALUES (%s, %s)
                """,
                (float(industry['id']), industry['name'])
            )

        for employer in data['employers']:
            cur.execute(
                """
                INSERT INTO employers (employer_id, accredited_IT, employer_name,
                employer_site, employer_hh_link, industry, open_vacancies)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (int(employer['id']), employer['accredited_it_employer'],
                 employer['name'], employer['site_url'], employer['vacancies_url'],
                 float(employer['industries'][0]['id']), employer['open_vacancies'])
            )

        for vacancy in data['vacancies']:

            salary = get_hh_salary(vacancy)

            if salary > 0:
                currency = vacancy["salary"]['currency']
            else:
                currency = None

            published = to_strip_date(vacancy["published_at"])

            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, employer_id, employer_name,
                vacancy_link, area_id, salary, currency , published)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (int(vacancy['id']), vacancy['name'],
                 int(vacancy['employer']['id']), vacancy['employer']['name'],
                 vacancy['alternate_url'], int(vacancy['area']['id']), salary,
                 currency, published)
            )

    conn.commit()
    conn.close()
