from src.hh_data_utils import get_hh_data
from src.db_utils import create_database, save_data_to_database
from src.config import config
from src.user_interaction import user_interaction


def main():
    employers_names = ['Яндекс', 'Магнит, розничная сеть', 'Газпром нефть', 'Лукойл', 'Черкизово',
                       'Ostin', 'Алроса', 'DNS', 'Альфабанк', 'Сеть аптек Апрель']

    params = config()

    print("Происходит сбор данных, создание базы данных и её заполнение.\n"
          "Это займет некоторое время, пожалуйста подождите")

    hh_data = get_hh_data(employers_names)

    create_database('hh_database', params)

    save_data_to_database(hh_data, 'hh_database', params)

    # Удаление переменной с большим объемом данных для освобождения памяти при работе программы
    del hh_data

    user_interaction()


if __name__ == '__main__':

    main()
