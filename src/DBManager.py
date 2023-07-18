import psycopg2
from abc import ABC, abstractmethod


class Manager(ABC):
    """
    Абстрактный класс менеджера работы с данными
    """

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword):
        pass


class DBManager(Manager):
    """
    Класс для работы с БД postgres
    """

    def __init__(self, db_name, **params):
        """
        Инициализация объекта
        :param db_name: название базы данных для работы
        :param params: параметры входа в базу данных (database.ini)
        """
        self.params = params
        self.db_name = db_name
        self.error_msg = 'Возникла ошибка. Работа программы продолжится'

    def get_companies_and_vacancies_count(self) -> list:
        """
        Возвращает список компаний с вакансиями
        :return: список компаний с вакансиями
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT employer_name, open_vacancies, table1.avaliable_vacancies FROM employers
                            JOIN
                            (SELECT COUNT(*) as avaliable_vacancies, employer_name FROM vacancies
                            GROUP BY employer_name) as table1
                            USING(employer_name)
                            """)
                data = cur.fetchall()

        except Exception:
            print(self.error_msg)
        finally:
            conn.close()

        return data

    def get_all_vacancies(self) -> list:
        """
        Возвращает список всех вакансий
        :return: список всех вакансий
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT employer_name, vacancy_name, salary, currency, vacancy_link FROM vacancies
                            """)
                data = cur.fetchall()

        except Exception:
            print(self.error_msg)
        finally:
            conn.close()

        return data

    def get_avg_salary(self) -> tuple:
        """
        Возвращает данные о средней з/п по вакансиям
        :return: данные о средней з/п
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            # Средняя з/п по вакансиям с разделением по валютам
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT currency, AVG(salary) as avg_salary FROM vacancies
                            WHERE salary <> 0
                            GROUP BY currency;
                            """)
                avg_all = cur.fetchall()

            # Средняя з/п по всем вакансиям в рублевом эквиваленте
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT AVG(vacancies.salary / currencies.rate) as avg_rub_salary FROM vacancies
                            JOIN currencies ON vacancies.currency = currencies.code
                            """)
                avg_rur = cur.fetchone()

        except Exception:
            print(self.error_msg)
        finally:
            conn.close()

        return avg_all, avg_rur[0]

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Возвращает все вакансии с з/п больше средней
        :return: все вакансии с з/п больше средней
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        avg_salary = self.get_avg_salary()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                            SELECT employer_name, vacancy_name, salary, currency, vacancy_link FROM vacancies
                            JOIN currencies ON vacancies.currency = currencies.code
                            WHERE (vacancies.salary / currencies.rate) > {avg_salary}
                            """)
                data = cur.fetchall()

        except Exception:
            print(self.error_msg)
        finally:
            conn.close()

        return data

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """
        Возвращает все вакансии, в названии которых есть ключевое слово
        :param keyword: ключевое слово
        :return: найденные вакансии
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                            SELECT employer_name, vacancy_name, salary, currency, 
                            vacancy_link FROM vacancies FROM vacancies
                            WHERE vacancy_name LIKE '%{keyword}%'
                            """)
                data = cur.fetchall()

        except Exception:
            print(self.error_msg)
        finally:
            conn.close()

        return data
