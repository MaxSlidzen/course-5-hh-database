import requests
import time


def get_employers_ids(employers: list) -> list:
    """
    Создание списка c id работодателей
    :param employers: Список с названиями компаний,
    :return: Список с id компаний из списка с названиями
    """
    # Итерация по списку с названиями
    employers_ids = []
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

        # Добавление компании в список
        employers_ids.append(needed_employer['id'])

    return employers_ids


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


def get_hh_data(employers_names):
    data = {}
    data['areas'] = get_areas_data()
    data['currencies'] = get_currencies_data()
    data['industries'] = get_industries_data()
    employers_ids = get_employers_ids(employers_names)
    data['employers'] = get_employers_data(employers_ids)
    data['vacancies'] = []
    for employer in data['employers']:
        data['vacancies'].extend(get_vacancies_data(employer))

    return data


def get_employers_data(employers_ids: list) -> list[dict]:
    employers_data = []
    for employer_id in employers_ids:
        response = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        employer_data = response.json()
        employers_data.append(employer_data)

    return employers_data


def get_vacancies_data(employer):
    page = 0
    vacancies_data = []

    while True:
        response = requests.get(employer['vacancies_url'],
                                params={'page': page,
                                        'per_page': 100})
        vacancies = response.json()['items']
        for vacancy in vacancies:
            vacancies_data.append(vacancy)

        # Поскольку 0-я страница тоже считается за страницу,
        # то сначала прибавляем страницу, а затем проверяем ограничения
        page += 1
        # Пауза для обхода капчи
        time.sleep(0.5)

        # Ограничение по количеству страниц вакансий и учет ограничения для глубины пагинации HH API
        if page == response.json()['pages'] or len(vacancies_data) == 2000:
            break

    return vacancies_data


def get_areas_data():
    response = requests.get('https://api.hh.ru/areas')
    areas_data = []
    areas = response.json()
    for country in areas:
        country_name = country['name']
        regions = country['areas']
        for region in regions:
            region_name = region['name']
            cities = region['areas']
            for city in cities:
                areas_data.append(
                    {
                        'id': city['id'],
                        'name': city['name'],
                        'region': region_name,
                        'country': country_name
                    }
                )
    return areas_data


def get_currencies_data():
    response = requests.get('https://api.hh.ru/dictionaries')
    currencies_data = []
    currencies = response.json()['currency']
    for currency in currencies:
        currencies_data.append(
            {
                'currency_code': currency['code'],
                'currency_name': currency['name'],
                'currency_rate': currency['rate']
            }
        )

    return currencies_data


def get_industries_data():
    industries_data = []
    response = requests.get('https://api.hh.ru/industries')
    industries = response.json()
    for industry in industries:
        for subindustry in industry['industries']:
            industries_data.append(
                {
                    'id': subindustry['id'],
                    'name': subindustry['name']
                }
            )
    return industries_data
