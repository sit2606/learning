"""
Модуль для работы с данными рынков в SQLite (версия 2).

Содержит функции для CRUD-операций с таблицей MARKETS.

Функции:
    add_market(market) — добавляет один рынок в базу
    add_many(markets) — batch-вставка списка рынков
    update_market(market) — обновляет данные рынка
    get_market(market_id) — получает один рынок по ID
    get_all_markets() — получает все рынки (список dict)
"""

import sqlite3

from config import DATABASE_PATH
from models.entities.market import Market


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

def update_market(market: Market):
    """Обновляет данные рынка в таблице MARKETS.

    Если рынок в режиме 'value' (названия), автоматически конвертирует
    обратно в ID через change_mode() перед записью.

    Args:
        market (Market): Объект рынка с обновлёнными данными.
            Обязательное поле: market.id

    Returns:
        None
    """
    if market.ref_mode == 'value' :
        market.change_mode()

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
            f"longitude = ?, "
            f"latitude = ?, "
            f"season1date = ?, "
            f"season1time = ?, "
            f"season2date = ?, "
            f"season2time = ?, "
            f"season3date = ?, "
            f"season3time = ?, "
            f"season4date = ?, "
            f"season4time = ?, "
            f"score = ? "
            f"WHERE id = ?",
            (market.market_info.marketname, market.location.street, market.location.city,
             market.location.county, market.location.state, market.location.zip,
             market.coordinates.longitude, market.coordinates.latitude,
             market.timesheet.season1date, market.timesheet.season1time,
             market.timesheet.season2date, market.timesheet.season2time,
             market.timesheet.season3date, market.timesheet.season3time,
             market.timesheet.season4date, market.timesheet.season4time,
             market.market_info.score, market.id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in update_market")

def get_market(market_id):
    """Получает один рынок по ID из таблицы MARKETS.

    Args:
        market_id: ID рынка (FMID)

    Returns:
        Market: объект рынка
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM MARKETS WHERE id = ?",
            (market_id,)
        )
        entry = cursor.fetchone()
        result = Market.from_dict({i : entry[i] for i in entry.keys()})
        conn.close()
        return result
    except Exception as e:
        print(e)
        print("Error in get_market")

def get_all_markets():
    """Получает все рынки из таблицы MARKETS.

    Returns:
        list[dict]: Список словарей с данными рынков
    """
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
        print("Error in get_all_markets")
def delete_market(market_id):
    """Удаляет рынок из таблицы MARKETS по ID.

    Args:
        market_id: ID рынка для удаления
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM MARKETS WHERE id = ?",
            (market_id,)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in delete_market")