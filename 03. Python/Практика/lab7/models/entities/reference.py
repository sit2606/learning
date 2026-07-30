"""
Справочники (Reference) — базовая сущность для работы с данными.

Содержит класс Reference для управления справочниками в SQLite:
- Common: простые справочники (id, name) — MEDIA, GROCERY_TYPES, BANKING_INFO, CITY и др.
- Connection: связующие таблицы many-to-many — MarketXSocialMedia, MarketXGrocery и др.

Использование:
    >>> media = Reference("MEDIA")
    >>> media.add("Instagram")
    >>> media.get_all_with_names()
    {'Facebook': 1, 'Twitter': 2, 'Instagram': 3}

    >>> market_media = Reference("MarketXSocialMedia", "Connection")
    >>> market_media.add((1, 3, "active"))
"""

from DAL.referencelib2 import create_connection_reference, create_reference, get_reference_with_name_as_key, \
    get_reference_with_uid_as_key, create_connection_entry, create_reference_entry, create_connection_entry_by_list, \
    create_reference_entry_by_list, read_connection_entry, read_reference_entry, update_reference_entry, \
    get_all_connections_by_market_id, delete_all_connections_by_market_id


class Reference:
    """Класс для работы со справочниками.

    Поддерживает два типа справочников:
    - Common: простые справочники (id, name)
    - Connection: связующие справочники (market_id, reference_id, status)

    При создании экземпляра автоматически создаёт таблицу в БД (CREATE TABLE IF NOT EXISTS).

    Attributes:
        name (str): Имя таблицы в БД
        reference_type (str): Тип справочника ('Common' или 'Connection')

    Example:
        >>> media = Reference("MEDIA")
        >>> media.add("Instagram")
        >>> media.get_all_with_names()
        {'Facebook': 1, 'Twitter': 2, 'Instagram': 3}
    """

    def __init__(self, name, reference_type="Common"):
        """Инициализирует справочник и создаёт таблицу если не существует.

        Args:
            name (str): Имя таблицы (например, 'MEDIA', 'MarketXSocialMedia')
            reference_type (str): 'Common' для простых, 'Connection' для связующих
        """
        self.name = name
        self.reference_type = reference_type
        if reference_type == "Connection":
            create_connection_reference(name)
        else:
            create_reference(name)

    def get_all_with_names(self):
        """Возвращает справочник как словарь {name: id} или {market_id: [ref_id, status]}.

        Returns:
            dict: Словарь справочника
        """
        return get_reference_with_name_as_key(self.name, self.reference_type)

    def get_all_with_keys(self):
        """Возвращает справочник как словарь {id: name} или {market_id: [ref_id, status]}.

        Returns:
            dict: Словарь справочника
        """
        return get_reference_with_uid_as_key(self.name, self.reference_type)

    def add(self, data_to_create):
        """Добавляет одну запись в справочник.

        Args:
            data_to_create: Для Common — строка (name).
                           Для Connection — кортеж (market_id, reference_id, status)
        """
        if self.reference_type == "Connection":
            return create_connection_entry(self.name, *data_to_create)
        else:
            return create_reference_entry(self.name, data_to_create)

    def add_many(self, data_to_create):
        """Batch-вставка записей в справочник.

        Args:
            data_to_create (list): Список кортежей [(name,), ...] или [(market_id, ref_id, status), ...]
        """
        if self.reference_type == "Connection":
            return create_connection_entry_by_list(self.name, data_to_create)
        else:
            return create_reference_entry_by_list(self.name, data_to_create)

    def get_entry(self, entry_uid=None, entry_name=None, market_id=None, reference_id=None):
        """Читает запись из справочника.

        Args:
            entry_uid (int, optional): ID записи (для Common)
            entry_name (str, optional): Имя записи (для Common)
            market_id (int, optional): ID рынка (для Connection)
            reference_id (int, optional): ID справочника (для Connection)

        Returns:
            tuple or dict or None: Найденная запись или None
        """
        if self.reference_type == "Connection":
            return read_connection_entry(self.name, market_id, reference_id)
        else:
            return read_reference_entry(self.name, entry_uid, entry_name)

    def get_connections(self, market_id):
        """Возвращает все связи для рынка (только для Connection).

        Args:
            market_id (int): ID рынка

        Returns:
            dict: Словарь {market_id: {reference_id: status, ...}} или None

        Example:
            >>> market_media = Reference("MarketXSocialMedia", "Connection")
            >>> market_media.get_connections(1)
            {'1': {'2': 'active', '3': 'pending'}}
        """
        if self.reference_type == "Connection":
            return get_all_connections_by_market_id(self.name, market_id)
        print("Метод доступен только для Connection справочников")
        return None

    def delete_connections(self, market_id):
        """Удаляет все связи для рынка (только для Connection).

        Args:
            market_id (int): ID рынка

        Returns:
            bool: True если что-то удалено, False если нет

        Example:
            >>> market_media = Reference("MarketXSocialMedia", "Connection")
            >>> market_media.delete_connections(1)
            True
        """
        if self.reference_type == "Connection":
            return delete_all_connections_by_market_id(self.name, market_id)
        print("Метод доступен только для Connection справочников")
        return None
