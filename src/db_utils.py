import psycopg2


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
                        city VARCHAR NOT NULL UNIQUE,
                        region VARCHAR NOT NULL,
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
                        accredited_IT VARCHAR(3) NOT NULL,
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
                        vacancy_name INTEGER NOT NULL,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        employer_name VARCHAR REFERENCES employers(employer_name),
                        vacancy_link VARCHAR NOT NULL,
                        area VARCHAR REFERENCES areas(city),
                        salary INTEGER,
                        currency VARCHAR,
                        published DATE NOT NULL
                    )
                    """)
    conn.commit()
    conn.close()
