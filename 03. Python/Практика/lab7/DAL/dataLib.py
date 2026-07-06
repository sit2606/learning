"""
dataLib — библиотека для управления данными о фермерских рынках.

Модуль предоставляет заглушки для CRUD-операций с рынками
(create_market, update_market, delete_market). Функции в разработке.

Использование:
    from dataLib import create_market, update_market, delete_market
"""
import csv


def create_market():
    """
    Создаёт новую запись о фермерском рынке.

    Функция в разработке (заглушка).
    """
    pass


def update_market(data_to_update):
    _data_to_update = data_to_update
    field_names = ['market_id',
                   'marketname',
                   'street',
                   'city',
                   'county',
                   'state',
                   'zip',
                   'season1date',
                   'season1time',
                   'season2date',
                   'season2time',
                   'season3date',
                   'season3time',
                   'season4date',
                   'season4time',
                   'score']
    try:
        with open(f"files/MARKET_INFO.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            new_file = []
            for row in reader:
                if _data_to_update["market_id"] == row["market_id"]:
                    row.update(_data_to_update)
                new_file.append(row)
        with open(f"files/MARKET_INFO.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(new_file)
    except Exception as e:
        print(e)
        print("Error in update_market")


def delete_market():
    """
    Удаляет запись фермерского рынка.

    Функция в разработке (заглушка).
    """
    pass