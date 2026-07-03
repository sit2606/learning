"""
App — точка входа приложения для управления фермерскими рынками.

Содержит user_lib_testing() для демонстрации CRUD-операций с пользователями
и main() как основную точку запуска с циклом обработки команд.

Использование:
    python App.py
"""
from BusinessLogic.marketList import get_all_markets_ordered_by_column
from DAL import userLib
from DAL.referenceLib import get_reference_with_name_as_key
from UI.uiLib import print_welcome
from BusinessLogic.workflowLib import *

def testing():
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
