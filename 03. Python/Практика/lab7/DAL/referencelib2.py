"""
Модуль для работы со справочниками в SQLite (версия 2).

Содержит функции для CRUD-операций со справочными таблицами.

Типы таблиц:
    1. Простые справочники: id (INTEGER PRIMARY KEY), name (TEXT UNIQUE NOT NULL)
       Используются для: Статусов, Типов оплаты, Категорий

    2. Связующие справочники: market_id, reference_id, status
       Составной ключ: PRIMARY KEY (market_id, reference_id)
       Используются для: связи рынков со справочниками

Функции для простых справочников:
    create_reference — создаёт таблицу простого справочника
    create_reference_entry — добавляет запись в простой справочник
    read_reference_entry — читает запись из простого справочника по id/имени
    update_reference_entry — обновляет запись в простом справочнике
    get_reference_with_name_as_key — возвращает словарь {name: id} или {name: [ref_id, status]}
    get_reference_with_uid_as_key — возвращает словарь {id: name} или {market_id: [ref_id, status]}

Функции для связующих справочников:
    create_connection_reference — создаёт таблицу связующего справочника
    create_connection_entry — добавляет запись в связующий справочник
    create_connection_entry_by_list — batch-вставка в связующий справочник
    read_connection_entry — читает статус связи между рынком и справочником
    get_all_connections_by_market_id — возвращает все связи для рынка
    delete_all_connections_by_market_id — удаляет все связи для рынка
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

def get_reference_with_name_as_key(reference_name, reference_type=''):
    """Возвращает справочник в виде словаря с именем в качестве ключа.

    Для простых справочников: {name: id}
    Для связующих справочников: {market_id: [reference_id, status]}

    Args:
        reference_name (str): Имя таблицы (например, 'statuses')
        reference_type (str): Тип справочника ('Common' или 'Connection')

    Returns:
        dict: Словарь справочника

    Example:
        >>> get_reference_with_name_as_key("statuses", "Common")
        {'Approved': 1, 'Pending': 2, 'Rejected': 3}
        >>> get_reference_with_name_as_key("market_statuses", "Connection")
        {'1': ['2', 'active'], '3': ['1', 'pending']}
    """
    reference = dict()
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {reference_name}")
        entry = cursor.fetchall()
        conn.close()
        match reference_type:
            case 'Common':
                for i in entry:
                    reference.update({i['name']: i['id']})
                return reference
            case 'Connection':
                for i in entry:
                    reference.update({
                        i['market_id']: [i['reference_id'], i['status']]
                    })
                return reference
            case _:
                print('Error in get_reference_with_name_as_key')
                print('No reference type provided')
                return None
    except Exception as e:
        print(e)
        print("Error in get_reference_with_name_as_key")
        return None
def get_reference_with_uid_as_key(reference_name, reference_type='Common'):
    """Возвращает справочник в виде словаря с ID в качестве ключа.

    Для простых справочников: {id: name}
    Для связующих справочников: {market_id: [reference_id, status]}

    Args:
        reference_name (str): Имя таблицы (например, 'statuses')
        reference_type (str): Тип справочника ('Common' или 'Connection')

    Returns:
        dict: Словарь справочника

    Example:
        >>> get_reference_with_uid_as_key("statuses", "Common")
        {1: 'Approved', 2: 'Pending', 3: 'Rejected'}
        >>> get_reference_with_uid_as_key("market_statuses", "Connection")
        {1: ['2', 'active'], 3: ['1', 'pending']}
    """
    reference = dict()
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {reference_name}")
        entry = cursor.fetchall()
        conn.close()
        match reference_type:
            case 'Common':
                for i in entry:
                    reference.update({i['id']: i['name']})
                return reference
            case 'Connection':
                for i in entry:
                    reference.update({
                        i['market_id']: [i['reference_id'], i['status']]
                    })
                return reference
            case _:
                print('Error in get_reference_with_uid_as_key')
                print('No reference type provided')
                return None
    except Exception as e:
        print(e)
        print("Error in get_reference_with_uid_as_key")
        return None
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
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT OR IGNORE INTO {reference_name} (name) VALUES (?)",
        (data_to_create,)
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
        conn.close()
        return entry
    except Exception as e:
        print(e)
        print("Error in read_reference_entry")
        return None

def update_reference_entry(reference_name, data_to_update):
    """Обновляет запись в простом справочнике.

    Args:
        reference_name (str): Имя таблицы (например, 'statuses')
        data_to_update (tuple): Кортеж (new_name, entry_id)

    Returns:
        None

    Example:
        >>> update_reference_entry("statuses", ("NewName", 1))
        # Обновляет запись с id=1, меняет name на "NewName"
    """
    entry_name, entry_id = data_to_update
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE {reference_name} SET name = ? WHERE id = ?",
            (entry_name, entry_id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in update_reference_entry")

def create_connection_reference(reference_name):
    """Создаёт таблицу связующего справочника, если она не существует.

    Таблица связывает рынки с простыми справочниками.
    Структура:
        - market_id: INTEGER (ID рынка)
        - reference_id: INTEGER (ID записи из простого справочника)
        - status: TEXT (дополнительный статус)
        - PRIMARY KEY (market_id, reference_id) — составной ключ

    Args:
        reference_name (str): Имя таблицы (например, 'market_statuses')

    Returns:
        None

    Example:
        >>> create_connection_reference("market_statuses")
        # Создаёт таблицу market_statuses с составным ключом
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {reference_name} (
            market_id INTEGER NOT NULL,
            reference_id INTEGER NOT NULL,
            status TEXT,
            PRIMARY KEY (market_id, reference_id)
        )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in create_connection_reference")


def create_connection_entry(reference_name, market_id, reference_id, status):
    """Добавляет запись в связующий справочник.

    Если запись с такой комбинацией (market_id, reference_id) уже существует,
    пропускает вставку (INSERT OR IGNORE).

    Args:
        reference_name (str): Имя таблицы (например, 'market_statuses')
        market_id (int): ID рынка
        reference_id (int): ID записи из справочника
        status (str): Дополнительный статус

    Returns:
        None

    Example:
        >>> create_connection_entry("market_statuses", 1, 2, "active")
        # Добавляет связь рынка 1 со справочником 2, статус "active"
    """
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT OR IGNORE INTO {reference_name} (market_id, reference_id, status) VALUES (?, ?, ?)",
            (market_id, reference_id, status)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in create_connection_entry")


def create_connection_entry_by_list(reference_name, list_entries):
    """Batch-вставка записей в связующий справочник.

    Args:
        reference_name (str): Имя таблицы (например, 'market_statuses')
        list_entries (list): Список кортежей/списков [(market_id, reference_id, status), ...]

    Returns:
        None

    Example:
        >>> data = [(1, 2, "active"), (1, 3, "pending"), (2, 1, "active")]
        >>> create_connection_entry_by_list("market_statuses", data)
        # Вставляет 3 записи одной транзакцией
    """
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()
        cursor.executemany(
            f"INSERT OR IGNORE INTO {reference_name} (market_id, reference_id, status) VALUES (?, ?, ?)",
            list_entries
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in create_connection_entry_by_list")

def read_connection_entry(reference_name, market_id, reference_id):
    """Ищет статус связи между рынком и элементом справочника.

    Выполняет SELECT запрос к связующей таблице и возвращает значение 'status'
    для записи, где market_id и reference_id совпадают с переданными параметрами.

    Args:
        reference_name (str): Имя таблицы (например, 'market_statuses')
        market_id (int): ID рынка
        reference_id (int): ID записи из справочника

    Returns:
        str: значение поля 'status' найденной записи, или None если не найдена

    Example:
        >>> read_connection_entry('market_statuses', 1, 2)
        'active'
    """
    _reference_name = reference_name
    _market_id = market_id
    _reference_id = reference_id
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {reference_name} WHERE market_id = ? and reference_id = ?",
                      (_market_id, _reference_id, ))
        result = cursor.fetchone()
        return result["status"]
    except:
        print("Error in read_connection_entry")


def get_all_connections_by_market_id(reference_name, market_id):
    """Возвращает все связи для указанного рынка.

    Args:
        reference_name (str): Имя таблицы (например, 'market_statuses')
        market_id (int): ID рынка

    Returns:
        dict: Словарь {market_id: {reference_id: status, ...}}

    Example:
        >>> get_all_connections_by_market_id("market_statuses", 1)
        {'1': {'2': 'active', '3': 'pending'}}
    """
    connections_dict = {}
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM {reference_name} WHERE market_id = ?",
            (str(market_id),)
        )
        entry = cursor.fetchall()
        conn.close()
        for row in entry:
            connections_dict[row["reference_id"]] = row["status"]
        return {str(market_id): connections_dict}
    except Exception as e:
        print(e)
        print("Error in get_all_connections_by_market_id")
        return None


def delete_all_connections_by_market_id(reference_name, market_id):
    """Удаляет все связи для указанного рынка.

    Args:
        reference_name (str): Имя таблицы (например, 'market_statuses')
        market_id (int): ID рынка

    Returns:
        bool: True если что-то удалено, False если нет

    Example:
        >>> delete_all_connections_by_market_id("market_statuses", 1)
        True
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM {reference_name} WHERE market_id = ?",
            (str(market_id),)
        )
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
    except Exception as e:
        print(e)
        print("Error in delete_all_connections_by_market_id")
        return False