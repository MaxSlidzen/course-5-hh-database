-- Создание базы данных
CREATE TABLE areas
(
    city_id INTEGER PRIMARY KEY,
    city VARCHAR,
    region VARCHAR,
    country VARCHAR NOT NULL
);
CREATE TABLE industries
(
    industry_id REAL PRIMARY KEY,
    name VARCHAR NOT NULL
);
CREATE TABLE currencies
(
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) UNIQUE,
    name VARCHAR(20) NOT NULL,
    rate REAL
);
CREATE TABLE employers
(
    employer_id INTEGER PRIMARY KEY,
    accredited_IT BOOLEAN,
    employer_name VARCHAR(50) NOT NULL UNIQUE,
    employer_site VARCHAR,
    employer_hh_link VARCHAR NOT NULL,
    industry REAL REFERENCES industries(industry_id),
    open_vacancies INTEGER NOT NULL
);
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
);

-- Запрос всех компаний и количество вакансий у каждой компании.
SELECT employer_name, open_vacancies, table1.avaliable_vacancies FROM employers
JOIN
(SELECT COUNT(*) as avaliable_vacancies, employer_name FROM vacancies
GROUP BY employer_name) as table1
USING(employer_name)

--  Запрос всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT employer_name, vacancy_name, salary, currency, vacancy_link FROM vacancies

-- Запрос средней зарплаты по вакансиям с учетом валют
SELECT currency, AVG(salary) as avg_salary FROM vacancies
WHERE salary <> 0
GROUP BY currency;

-- Запрос средней зарплаты по всем вакансиям в рублевом эквиваленте
SELECT AVG(vacancies.salary / currencies.rate) as avg_rub_salary FROM vacancies
JOIN currencies ON vacancies.currency = currencies.code

-- Запрос всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT employer_name, vacancy_name, salary, currency, vacancy_link FROM vacancies
JOIN currencies ON vacancies.currency = currencies.code
WHERE (vacancies.salary / currencies.rate) > (
SELECT AVG(vacancies.salary / currencies.rate) as avg_rub_salary FROM vacancies
JOIN currencies ON vacancies.currency = currencies.code
)

-- Запрос всех вакансий, в названии которых содержатся переданные в метод слова
SELECT employer_name, vacancy_name, salary, currency,
vacancy_link FROM vacancies
WHERE vacancy_name LIKE '%{keyword}%'

