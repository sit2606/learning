"""
commandHandler — обработчики команд пользователя.

Модуль содержит функции-обработчики для каждой команды:
- command_help(): справка
- command_exit(): выход
- command_list_all(): список всех рынков
- command_list(): список с пагинацией
- command_order(): сортировка по колонке

Каждая функция возвращает данные для вывода (не зависит от UI).
Вызывается из workflowLib.proceed_command().

Использование:
    from BusinessLogic.commandHandler import command_help, command_list_all
"""
from BusinessLogic.marketList import get_all_markets, get_all_markets_ordered_by_num, get_all_markets_ordered_by_column,\
    prepare_ordered_list


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
    column = int(input('Введите номер колонки, по которой вы хотите отсортировать список: '))
    order = input('Введите порядок сортировки d - от большего к меньшему, a - от меньшего к большему: ')
    markets , column = get_all_markets_ordered_by_column(column, order)
    markets = prepare_ordered_list(markets)
    return True, markets, column, order