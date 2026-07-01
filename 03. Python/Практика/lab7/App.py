"""
App — точка входа приложения для управления фермерскими рынками.

Содержит функцию testing() для демонстрации работы библиотеки dataLib
и main() как основную точку запуска.

Использование:
    python App.py
"""

from uuid import uuid4


def testing():
    """Демонстрационная функция: создаёт справочник MEDIA, добавляет записи,
    связывает с рынком и обновляет данные."""
    import dataLib
    # import fileLib
    import userLib
    dataLib.create_reference("MEDIA")
    dataLib.create_reference_entry("MEDIA", "Youtube")
    dataLib.create_reference_entry("MEDIA", "Twitter")
    dataLib.create_reference_entry("MEDIA", "Instagram")
    x = dataLib.read_reference_entry("MEDIA", entry_name="Youtube")
    dataLib.create_connection_reference("MediaToMarket1")
    dataLib.create_connection_entry("MediaToMarket1", uuid4(), uuid4(), True)
    dataLib.update_reference_entry("MEDIA", {'Id': x[0], 'Name': '12341'})
def main():
    """Основная функция запуска приложения."""
    import dataLib
    # import fileLib
    import userLib
    testing()
if __name__ == "__main__":
    main()
