from src.hh_data_utils import get_hh_data
from src.db_utils import create_database, save_data_to_database
from src.config import config
import time


def main():
    employers_names = ['Яндекс', 'Магнит, розничная сеть', 'Газпром нефть', 'Лукойл', 'Черкизово',
                       'Ostin', 'Алроса', 'DNS', 'Альфабанк', 'Сеть аптек Апрель']

    params = config()

    hh_data = get_hh_data(employers_names)

    create_database('hh_database', params)
    save_data_to_database(hh_data, 'hh_database', params)


if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
    finally:
        print("--- %s seconds ---" % (time.time() - start_time))
