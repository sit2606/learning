"""
App — точка входа приложения для управления фермерскими рынками.

Выполняет:
1. Создание директории files/
2. Тестирование CRUD пользователей
3. Инициализацию справочников и парсинг Export.csv
4. Цикл обработки пользовательских команд

Использование:
    python App.py
"""
from BusinessLogic.marketList import get_all_markets_ordered_by_column, get_market_by_id
from DAL import userLib
from DAL.fileLib import create_reference_base
from DAL.referenceLib import get_reference_with_name_as_key, get_all_connections_by_market_id, \
    get_reference_with_uid_as_key
from UI.uiLib import print_welcome
from BusinessLogic.workflowLib import *

def testing():
    create_reference_base()
    s = get_all_connections_by_market_id('MarketXBankingInfo',1000021)
    z = get_reference_with_uid_as_key('MarketXBankingInfo', 'Connection')
    get_market_by_id(1000021)
    print('a')

def user_lib_testing():
    fileLib.create_user_base()
    test_user_uid = userLib.create_user()
    test_user = userLib.read_user(test_user_uid)
    test_user['firstname'] = 'TestIngs'
    userLib.update_user(test_user)
    test_user_to_delete = userLib.create_user()
    userLib.create_user()
    userLib.delete_user(test_user_to_delete)
def main():
    """Основная функция запуска приложения."""
    testing()
    directory_creation()
    user_lib_testing()
    file_creation()
    run_app = True
    print_welcome()
    while run_app:
        command = get_command()
        run_app = proceed_command(command)

if __name__ == "__main__":
    main()
