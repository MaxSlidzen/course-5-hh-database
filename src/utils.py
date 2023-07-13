import requests


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
