"""
Модуль для работы с данными рынков в SQLite (версия 2).

Содержит функции для CRUD-операций с таблицей MARKETS.

Функции:
    add_market — добавляет один рынок в базу
    add_many — batch-вставка списка рынков
    update_market — обновляет данные рынка
"""

import sqlite3

from config import DATABASE_PATH
from models.entities.market import Market
from models.entities.reference import Reference


def add_market(market: Market):
    """Добавляет один рынок в таблицу MARKETS.

    Args:
        market (Market): Объект рынка для вставки

    Returns:
        None
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO MARKETS 
               (id, marketname, street, city, county, state, zip, 
                longitude, latitude, season1date, season1time, season2date, season2time, 
                season3date, season3time, season4date, season4time, score) 
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (market.id, market.market_info.marketname, market.location.street,
             market.location.city, market.location.county, market.location.state,
             market.location.zip, market.coordinates.longitude, market.coordinates.latitude,
             market.timesheet.season1date, market.timesheet.season1time,
             market.timesheet.season2date, market.timesheet.season2time,
             market.timesheet.season3date, market.timesheet.season3time,
             market.timesheet.season4date, market.timesheet.season4time,
             market.market_info.score)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in create_market")

def add_many(markets: list[Market]):
    """Batch-вставка списка рынков в таблицу MARKETS.

    Args:
        markets (list[Market]): Список объектов Market для вставки

    Returns:
        None
    """
    try:
        z = [(market.id, market.market_info.marketname, market.location.street,
             market.location.city, market.location.county, market.location.state,
             market.location.zip, market.coordinates.longitude, market.coordinates.latitude,
             market.timesheet.season1date, market.timesheet.season1time,
             market.timesheet.season2date, market.timesheet.season2time,
             market.timesheet.season3date, market.timesheet.season3time,
             market.timesheet.season4date, market.timesheet.season4time,
             market.market_info.score) for market in markets]
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.executemany(
            """INSERT OR IGNORE INTO MARKETS
               (id, marketname, street, city, county, state, zip,
                longitude, latitude, season1date, season1time, season2date, season2time,
                season3date, season3time, season4date, season4time, score)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            z
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in add_many")

def update_market(data_to_update):
    """Обновляет данные рынка в таблице MARKETS.

    Args:
        data_to_update (dict): Словарь с обновляемыми данными.
            Обязательное поле: id

    Returns:
        None
    """
    city = Reference('CITY')
    county = Reference('COUNTY')
    state = Reference('STATE')
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE MARKETS SET "
            f"marketname = ?, "
            f"street = ?, "
            f"city = ?,"
            f"county = ?, "
            f"state = ?, "
            f"zip = ?, "
            f"season1date = ?, "
            f"season1time = ?, "
            f"season2date = ?, "
            f"season2time = ?, "
            f"season3date = ?, "
            f"season3time = ?, "
            f"season4date = ?, "
            f"season4time = ?, "
            f"score = ?"
            f"WHERE id = ?",
            (data_to_update['marketname'], data_to_update['street'], data_to_update['city'],
             data_to_update['county'], data_to_update['state'], data_to_update['zip'],
             data_to_update['season1date'], data_to_update['season1time'],
             data_to_update['season2date'], data_to_update['season2time'],
             data_to_update['season3date'], data_to_update['season3time'],
             data_to_update['season4date'], data_to_update['season4time'],
             data_to_update['score'],)
        )
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        print("Error in update_market")

def get_market(market_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            f"""SELECT * FROM MARKETS WHERE id = {market_id}"""
        )
        entry = cursor.fetchone()
        result = Market.from_dict({i : entry[i] for i in entry.keys()})
        conn.close()
        return result
    except Exception as e:
        print(e)
        print("Error in create_market")

def get_all_markets():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            f"""SELECT * FROM MARKETS"""
        )
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result
    except Exception as e:
        print(e)
        print("Error in create_market")