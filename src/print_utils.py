def print_companies_and_vacancies_count(data: list[tuple[str, int]]) -> None:
    """
    Выводит информацию о компаниях с количеством вакансий
    :param data: информация о компаниях
    :return:
    """
    for employer in data:
        print(f'В компании {employer[0]} всего открыто {employer[1]} вакансий,'
              f'Из них {employer[2]} находится в базе данных')


def print_vacancies(data: list[tuple[str, int]]) -> None:
    """
    Выводит информацию о вакансиях
    :param data: информация о вакансиях
    :return:
    """
    for vacancy in data:
        print(f'В компанию {vacancy[0]} требуется "{vacancy[1]}" с з/п {vacancy[2]}'
              f'{" " + vacancy[3] if vacancy[2] != 0 else ""}. '
              f'Ссылка на вакансию {vacancy[4]}')
    print(f'\nПоказано результатов: {len(data)}')


def print_avg_salary(data: tuple[list[tuple[str, float]], float]) -> None:
    """
    Выводит информацию о средней з/п с учетом валюты вакансии,
    а также среднюю з/п обо всех вакансиях в рублевом эквиваленте
    :param data: информация о средних з/п в различных валютах
    :return:
    """
    for currency in data[0]:
        print(f'Средняя з/п по вакансиям в валюте '
              f'{currency[0]} составляет {int(currency[1])}')
    print(f'Средняя з/п по всем вакансиям в рублевом эквиваленте составляет {int(data[1])}')
