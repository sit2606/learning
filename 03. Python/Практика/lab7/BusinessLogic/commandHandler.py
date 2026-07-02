"""
commandHandler — обработчики команд пользователя.

Модуль содержит функции-обработчики для каждой поддерживаемой команды.
Вызывается из workflowLib.proceed_command().

Использование:
    from commandHandler import command_help, command_exit
"""
from BusinessLogic.marketList import get_all_markets
from UI import uiLib


def command_help():
    uiLib.print_help()
    return True
def command_exit():
    uiLib.print_exit()
    return False


def command_list():
    a = get_all_markets()
    uiLib.print_list(a)
    return True