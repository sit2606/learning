"""
Модели для справочных данных.

Содержит классы для представления справочников:
- SimpleReference — базовый справочник (Статусы, Типы оплаты, Категории)
- ConnectionReference — связующий справочник (связь рынков со справочниками)
"""


class SimpleReference:
    """Базовый класс для простых справочников.

    Представляет справочник с одним полем name.
    Используется для: Статусов, Типов оплаты, Категорий рынков.

    Attributes:
        name (str): Название элемента справочника

    Example:
        >>> ref = SimpleReference("approved")
        >>> print(ref.name)
        approved
    """

    def __init__(self, name):
        """Инициализирует справочник.

        Args:
            name (str): Название элемента справочника
        """
        self.name = name


class ConnectionReference(SimpleReference):
    """Класс для связующих справочников.

    Наследуется от SimpleReference.
    Используется для связи рынков с другими справочниками
    (рынок-статус, рынок-тип оплаты, рынок-категория).

    Example:
        >>> ref = ConnectionReference("approved")
        >>> print(ref.name)
        approved
    """
    pass