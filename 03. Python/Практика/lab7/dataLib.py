"""
dataLib — библиотека для управления данными о фермерских рынках и справочниками.

Модуль предоставляет CRUD-функции для работы с рынками (markets),
справочниками (references) и связями между ними (connections)
через CSV-файлы.

Использование:
    from dataLib import create_reference, create_reference_entry
"""

import csv
import uuid


def create_market():
    """
    Создаёт новую запись о фермерском рынке.

    Функция в разработке (заглушка).
    """
    pass


def update_market():
    """
    Обновляет данные существующего фермерского рынка.

    Функция в разработке (заглушка).
    """
    pass


def delete_market():
    """
    Удаляет запись фермерского рынка.

    Функция в разработке (заглушка).
    """
    pass
def create_reference(reference_name):
    """
    Создаёт новый справочник (CSV-файл) с заголовками 'Id' и 'Name'.

    Args:
        reference_name (str): Имя справочника (без расширения .csv).
            Файл будет создан как '<reference_name>.csv' в текущей директории.

    Returns:
        None

    Raises:
        Exception: при ошибке создания файла выводит сообщение
        "Error in create reference" и текст исключения в консоль.

    Example:
        >>> create_reference('categories')
        # Создаёт файл categories.csv с заголовками Id, Name
    """
    _reference_name = reference_name
    field_names = ['Id','Name']
    try:
        with open(f"{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
    except Exception as e:
        print(e)
        print("Error in create reference")
def create_reference_entry(reference_name, data_to_create):
    """
    Добавляет новую запись в существующий справочник.

    Генерирует уникальный UUID для поля 'Id' и записывает его вместе
    с переданным значением в CSV-файл справочника.

    Args:
        reference_name (str): Имя справочника (без расширения .csv).
        data_to_create (str): Значение для поля 'Name' новой записи.

    Returns:
        None

    Raises:
        Exception: при ошибке записи файла выводит сообщение
        "Error in create_reference_entry" и текст исключения в консоль.

    Example:
        >>> create_reference_entry('categories', 'Овощи')
        # Добавляет строку [UUID, 'Овощи'] в файл categories.csv
    """
    _reference_name = reference_name
    _data_to_create = data_to_create
    try:
        with open(f"{_reference_name}.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            uid = uuid.uuid4()
            writer.writerow([uid, _data_to_create])
    except Exception as e:
        print(e)
        print("Error in create_reference_entry")
def read_reference_entry(reference_name, entry_uid=None, entry_name=None):
    """
    Ищет запись в справочнике по UUID или имени.

    Построчно перебирает CSV-файл и возвращает первую найденную запись,
    где поле 'Id' совпадает с entry_uid или поле 'Name' совпадает с entry_name.

    Args:
        reference_name (str): Имя справочника (без расширения .csv).
        entry_uid: UUID записи для поиска по полю 'Id' (по умолчанию NULL).
        entry_name: Имя записи для поиска по полю 'Name' (по умолчанию NULL).

    Returns:
        tuple: кортеж (Id, Name) найденной записи, или None если не найдена.

    Raises:
        Exception: при ошибке чтения файла выводит сообщение
        "Error in read_reference_entry" и текст исключения в консоль.

    Example:
        >>> read_reference_entry('categories', entry_uid='abc-123')
        ('abc-123', 'Овощи')
        >>> read_reference_entry('categories', entry_name='Овощи')
        ('abc-123', 'Овощи')
    """
    _reference_name = reference_name
    _entry_uid = entry_uid
    _entry_name = entry_name
    try:
        with open(f"{_reference_name}.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Id"] == _entry_uid:
                    return row["Id"], row["Name"]
                if row["Name"] == _entry_name:
                    return row["Id"], row["Name"]
    except Exception as e:
        print(e)
        print("Error in read_reference_entry")
def update_reference_entry(reference_name, data_to_update):
    """
    Обновляет существующую запись в CSV-справочнике.

    Открывает CSV-файл справочника, перебирает строки и обновляет значения
    в тех ячейках, где ключ столбца совпадает с ключом из переданного словаря.

    Args:
        reference_name (str): Имя справочника (без расширения .csv).
            Файл ищется как '<reference_name>.csv' в текущей директории.
        data_to_update (dict): Словарь вида {столбец: новое_значение}.
            Ключи должны совпадать с именами столбцов CSV-файла.

    Returns:
        None

    Raises:
        При ошибке чтения/записи файла выводит сообщение
        "Error in update_reference_entry" в консоль.

    Note:
        Файл открывается в режиме добавления ('a'), что может привести
        к некорректной работе DictReader. Для корректного обновления
        рекомендуется использовать режим 'r+' или перезапись файла.

    Example:
        >>> update_reference_entry('categories', {'Name': 'Фрукты'})
        # Заменяет значение столбца 'Name' на 'Фрукты' во всех строках
    """
    _reference_name = reference_name
    _data_to_update = data_to_update
    try:
        with open(f"{_reference_name}.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            new_file = []
            for row in reader:
                if data_to_update["Id"] == row["Id"]:
                    row.update(_data_to_update)
                new_file.append(row)
        with open(f"{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Id", "Name"])
            writer.writeheader()
            writer.writerows(new_file)
    except Exception as e:
        print(e)
        print("Error in update_reference_entry")
def create_connection_reference(reference_name):
    """
    Создаёт CSV-файл для хранения связей между рынками и справочниками.

    Файл содержит заголовки: 'market_id', 'reference_id', 'status'.

    Args:
        reference_name (str): Имя файла связи (без расширения .csv).

    Returns:
        None

    Raises:
        Exception: при ошибке создания файла выводит сообщение
        "Error in create reference" и текст исключения в консоль.

    Example:
        >>> create_connection_reference('market_goods')
        # Создаёт файл market_goods.csv с заголовками market_id, reference_id, status
    """
    _reference_name = reference_name
    field_names = ['market_id','reference_id','status']
    try:
        with open(f"{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
    except Exception as e:
        print(e)
        print("Error in create reference")
def create_connection_entry(reference_name, market_id, reference_id, status):
    """
    Добавляет запись о связи между рынком и элементом справочника.

    Генерирует UUID для связи и записывает market_id, reference_id, status
    в CSV-файл.

    Args:
        reference_name (str): Имя файла связи (без расширения .csv).
        market_id: Идентификатор рынка.
        reference_id: Идентификатор элемента справочника.
        status: Статус связи (например, 'active', 'inactive').

    Returns:
        None

    Raises:
        Exception: при ошибке записи файла выводит сообщение
        "Error in create reference entity" и текст исключения в консоль.

    Example:
        >>> create_connection_entry('market_goods', 'mkt-1', 'good-5', 'active')
        # Добавляет связь рынка mkt-1 с товаром good-5 в файл market_goods.csv
    """
    _reference_name = reference_name
    _market_id = market_id
    _reference_id = reference_id
    _status = status
    try:
        with open(f"{_reference_name}.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            uid = uuid.uuid4()
            writer.writerow([uid, market_id, reference_id, status])
    except Exception as e:
        print(e)
        print("Error in create reference entity")
def read_connection_entry(reference_name, market_id, reference_id):
    """
    Ищет статус связи между рынком и элементом справочника.

    Перебирает строки CSV-файла и возвращает значение 'status' для записи,
    где market_id и reference_id совпадают с переданными параметрами.

    Args:
        reference_name (str): Имя файла связи (без расширения .csv).
        market_id: Идентификатор рынка для фильтрации.
        reference_id: Идентификатор элемента справочника для фильтрации.

    Returns:
        str: значение поля 'status' найденной записи, или None если не найдена.

    Raises:
        Exception: при ошибке чтения файла выводит сообщение
        "Error in read_connection_entry" в консоль.

    Example:
        >>> read_connection_entry('market_goods', 'mkt-1', 'good-5')
        'active'
    """
    _reference_name = reference_name
    _market_id = market_id
    _reference_id = reference_id
    try:
        with open(f"{_reference_name}.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["market_id"] == _market_id and row["reference_id"] == _reference_id:
                    return row["status"]
    except:
        print("Error in read_connection_entry")