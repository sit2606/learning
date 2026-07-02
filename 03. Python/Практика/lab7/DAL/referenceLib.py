"""
referenceLib — библиотека для управления справочниками и связями.

Модуль предоставляет CRUD-функции для работы со справочными CSV-файлами
(references) и связями между рынками и элементами справочников (connections).
Все файлы хранятся в папке files/.

Использование:
    from referenceLib import create_reference, create_reference_entry, read_reference_entry
"""

import csv
import os
import uuid


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
        with open(f"files/{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
    except Exception as e:
        print(e)
        print("Error in create reference")


def create_reference_entry(reference_name, data_to_create):
    """
    Добавляет новую запись в справочник.

    Если CSV-файл справочника не существует, создаёт его автоматически
    через create_reference(). Затем генерирует UUID и записывает
    новую строку [Id, Name] в файл.

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
        # Создаёт categories.csv (если нет) и добавляет строку [UUID, 'Овощи']
    """
    _reference_name = reference_name
    _data_to_create = data_to_create
    file_path = f"files/{_reference_name}.csv"
    if not os.path.isfile(file_path):
        create_reference(reference_name)
    try:
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            uid = uuid.uuid4()
            writer.writerow([uid, data_to_create])
    except Exception as e:
        print(e)
        print("Error in create_reference_entry")


def read_reference_entry(reference_name, entry_uid=None, entry_name=None):
    """
    Ищет запись в справочнике по UUID или имени.

    Если CSV-файл не существует, создаёт пустой справочник.
    Затем перебирает строки и возвращает первую запись, где
    поле 'Id' совпадает с entry_uid или поле 'Name' совпадает с entry_name.

    Args:
        reference_name (str): Имя справочника (без расширения .csv).
        entry_uid: UUID записи для поиска по полю 'Id' (по умолчанию None).
        entry_name: Имя записи для поиска по полю 'Name' (по умолчанию None).

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
    file_path = f"files/{_reference_name}.csv"
    if not os.path.isfile(file_path):
        create_reference(reference_name)
    try:
        with open(f"files/{_reference_name}.csv", "r", newline="", encoding="utf-8") as file:
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
    Обновляет существующую запись в CSV-справочнике по полю 'Id'.

    Читает CSV-файл, находит строку с Id, совпадающим с data_to_update["Id"],
    обновляет её значениями из data_to_update и перезаписывает файл.

    Args:
        reference_name (str): Имя справочника (без расширения .csv).
        data_to_update (dict): Словарь вида {'Id': '...', 'Name': '...'}.
            Обязательно должен содержать ключ 'Id' для поиска записи.

    Returns:
        None

    Raises:
        Exception: при ошибке чтения/записи файла выводит сообщение
        "Error in update_reference_entry" и текст исключения в консоль.

    Example:
        >>> update_reference_entry('categories', {'Id': 'abc-123', 'Name': 'Фрукты'})
        # Обновляет Name у записи с Id 'abc-123'
    """
    _reference_name = reference_name
    _data_to_update = data_to_update
    try:
        with open(f"files/{_reference_name}.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            new_file = []
            for row in reader:
                if _data_to_update["Id"] == row["Id"]:
                    row.update(_data_to_update)
                new_file.append(row)
        with open(f"files/{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
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
        with open(f"files/{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
    except Exception as e:
        print(e)
        print("Error in create reference")


def create_connection_entry(reference_name, market_id, reference_id, status):
    """
    Добавляет запись о связи между рынком и элементом справочника.

    Если CSV-файл не существует, создаёт его через create_connection_reference().
    Записывает строку [market_id, reference_id, status] в файл.

    Args:
        reference_name (str): Имя файла связи (без расширения .csv).
        market_id: Идентификатор рынка.
        reference_id: Идентификатор элемента справочника.
        status: Значение связи (например, URL соцсети, тип товара).

    Returns:
        None

    Raises:
        Exception: при ошибке записи файла выводит сообщение
        "Error in create reference entity" и текст исключения в консоль.

    Example:
        >>> create_connection_entry('MarketXSocialMedia', 'mkt-1', 'ref-5', 'https://...')
        # Создаёт файл MarketXSocialMedia.csv (если нет) и добавляет связь
    """

    _reference_name = reference_name
    _market_id = market_id
    _reference_id = reference_id
    _status = status
    file_path = f"files/{_reference_name}.csv"
    if not os.path.isfile(file_path):
        create_connection_reference(reference_name)
    try:
        with open(f"files/{_reference_name}.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([ market_id, reference_id, status])
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
        with open(f"files/{_reference_name}.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["market_id"] == _market_id and row["reference_id"] == _reference_id:
                    return row["status"]
    except:
        print("Error in read_connection_entry")
