"""
commandHandler — обработчики команд пользователя.

Модуль содержит функции-обработчики для каждой поддерживаемой команды.
Каждая функция возвращает данные для вывода (не зависит от UI).
Вызывается из workflowLib.proceed_command().

Использование:
    from BusinessLogic.commandHandler import command_help, command_list_all, command_list, command_order, command_exit
"""
from BusinessLogic.marketList import get_all_markets, get_all_markets_ordered_by_num, get_all_markets_ordered_by_column


def command_help():
    return True
def command_exit():
    return False

def command_list_all():
    return True, get_all_markets()
def command_list():
    start_num = int(input('Введите стартовый номер: ')) or 1
    step = int(input('Введите  шаг: ')) or 10
    return True, get_all_markets_ordered_by_num(),start_num,step
def command_order():
    print('Вывод сортированного списка (по полю County)')
    return True, get_all_markets_ordered_by_column()