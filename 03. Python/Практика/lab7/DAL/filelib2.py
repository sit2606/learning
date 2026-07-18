"""
Модуль инициализации справочных данных в SQLite (версия 2).

Содержит функцию prepare_ref() для создания и заполнения справочных таблиц
при первом запуске приложения.

Справочники:
    - MEDIA: типы СМИ
    - GROCERY_TYPES: типы продовольственных товаров
    - BANKING_INFO: банковские реквизиты
"""

from DAL import requiredFiles, referencelib2

REF_LIST = [
    {'MEDIA': requiredFiles.MEDIA},
    {'GROCERY_TYPES': requiredFiles.GROCERY_TYPES},
    {'BANKING_INFO': requiredFiles.BANKING_INFO}
]


def prepare_ref():
    """Инициализирует справочники, создавая таблицы и заполняя их данными.

    Для каждого справочника:
    1. Создаёт таблицу (create_reference)
    2. Добавляет все значения из множества (create_reference_entry)

    Args:
        None

    Returns:
        None

    Example:
        >>> prepare_ref()
        # Создаёт таблицы MEDIA, GROCERY_TYPES, BANKING_INFO
        # и заполняет их записями из requiredFiles
    """
    for item in REF_LIST:
        ref_name = list(item.keys())[0]
        referencelib2.create_reference(ref_name)
        list_of_entries = item.get(ref_name)
        for value in list_of_entries:
            referencelib2.create_reference_entry(ref_name, value)