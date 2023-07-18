from src.DBManager import DBManager
from src.config import config
from src.print_utils import print_avg_salary, print_vacancies, print_companies_and_vacancies_count


def user_interaction():
    params = config()
    db_manager = DBManager('hh_database', params)
    count = 0
    while count < 3:
        user_input = input("Введите:\n"
                           "1 - Для отображения компаний с доступными вакансиями;\n"
                           "2 - Для отображения всех вакансий;\n"
                           "3 - Для отображения средней з/п по вакансиям;\n"
                           "4 - Для отображения всех вакансий, у которых зарплата выше средней по всем вакансиям;\n"
                           "5 - Для отображения вакансий по ключевому слову;\n"
                           "0 - Для завершения программы:\n")

        if user_input == "1":
            count = 0
            data = db_manager.get_companies_and_vacancies_count()
            print_companies_and_vacancies_count(data)
        elif user_input == "2":
            count = 0
            data = db_manager.get_all_vacancies()
            print_vacancies(data)
        elif user_input == "3":
            count = 0
            data = db_manager.get_avg_salary()
            print_avg_salary(data)
        elif user_input == "4":
            count = 0
            data = db_manager.get_vacancies_with_higher_salary()
            print_vacancies(data)
        elif user_input == "5":
            count = 0
            user_input = input("Ввод чувствителен к регистру.\n"
                               "Введите ключевое слово :")
            data = db_manager.get_vacancies_with_keyword(user_input)
            print_vacancies(data)
        elif user_input == '0':
            break
        else:
            count += 1
            print("Необходимо ввести один из предложенных вариантов!\n"
                  "После 3-кратного некорректного ввода подряд программа завершит работу.\n"
                  f"Некорректных вводов подряд: {count}")
