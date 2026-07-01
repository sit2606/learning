"""
App — точка входа приложения для управления фермерскими рынками.

Содержит функцию testing() для демонстрации работы библиотек
dataLib и fileLib, и main() как основную точку запуска.

Использование:
    python App.py
"""





def testing():
    """
    Демонстрационная функция: полный цикл обработки данных.

    1. Инициализирует справочники (MEDIA, GROCERY_TYPES, BANKING_INFO)
    2. Читает Export.csv и создаёт связи рынков с справочниками
    3. Создаёт итоговый файл MARKET_INFO.csv
    """
    import fileLib
    import dataLib
    fileLib.prepare_ref()
    dataLib.create_market_base(fileLib.read_csv())
    print('s')
def main():
    """Основная функция запуска приложения."""
    import dataLib
    # import fileLib
    import userLib
    testing()
if __name__ == "__main__":
    main()
