"""
Модуль для работы со справочниками в SQLite (версия 2).

Содержит функции для CRUD-операций со справочными таблицами.
Каждая таблица имеет структуру: id (INTEGER PRIMARY KEY), name (TEXT UNIQUE NOT NULL).

Функции:
    create_reference — создаёт таблицу для справочника
    create_reference_entry — добавляет запись в справочник
    read_reference_entry — читает запись из справочника по id или имени
    update_reference_entry — обновляет запись в справочнике (заглушка)
"""

import sqlite3

DATABASE_PATH = 'database/base.db'


def create_reference(reference_name):
    """Создаёт таблицу для справочника, если она не существует.

    Таблица содержит поля:
        - id: INTEGER PRIMARY KEY AUTOINCREMENT
        - name: TEXT UNIQUE NOT NULL

    Args:
        reference_name (str): Имя таблицы (например, 'statuses', 'payment_methods')

    Returns:
        None

    Example:
        >>> create_reference("statuses")
        # Создаёт таблицу statuses с полями id и name
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {reference_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in create_reference")


def create_reference_entry(reference_name, data_to_create):
    """Добавляет запись в справочник.

    Если запись с таким name уже существует, пропускает вставку (INSERT OR IGNORE).
    Имя автоматически очищается от пробелов и капитализируется.

    Args:
        reference_name (str): Имя таблицы (например, 'statuses')
        data_to_create (str): Значение для вставки (например, 'approved')

    Returns:
        None

    Example:
        >>> create_reference_entry("statuses", "approved")
        # Добавляет запись "Approved" в таблицу statuses
    """
    _data_to_create = data_to_create.strip().capitalize()
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT OR IGNORE INTO {reference_name} (name) VALUES (?)",
        (_data_to_create,)
    )
    conn.commit()
    conn.close()
def read_reference_entry(reference_name, entry_uid=None, entry_name=None):
    """Читает запись из справочника по id или имени.

    Выполняет SELECT запрос с условием OR: ищет по id ИЛИ по имени.
    Если запись не найдена, возвращает None.

    Args:
        reference_name (str): Имя таблицы (например, 'statuses')
        entry_uid (int, optional): ID записи для поиска
        entry_name (str, optional): Имя записи для поиска

    Returns:
        tuple or None: Кортеж (id, name) или None если не найдено

    Example:
        >>> read_reference_entry("statuses", entry_uid=1)
        (1, 'Approved')
        >>> read_reference_entry("statuses", entry_name="Approved")
        (1, 'Approved')
        >>> read_reference_entry("statuses", entry_uid=999)
        None
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT * FROM {reference_name} WHERE id = ? OR name = ?",
            (entry_uid, entry_name)
        )
        entry = cursor.fetchone()
        return entry
    except Exception as e:
        print(e)
        print("Error in read_reference_entry")
        return None
    finally:
        conn.close()
def update_reference_entry(reference_name, data_to_update):
    """Обновляет запись в справочнике (заглушка).

    Функция пока не реализована. Предназначена для обновления
    существующих записей в справочных таблицах.

    Args:
        reference_name (str): Имя таблицы (например, 'statuses')
        data_to_update (dict): Данные для обновления (поля и значения)

    Returns:
        None

    TODO:
        - Реализовать UPDATE запрос
        - Определить формат data_to_update
    """
    try:
        pass
    except Exception as e:
        print(e)
        print("Error in update_reference_entry")