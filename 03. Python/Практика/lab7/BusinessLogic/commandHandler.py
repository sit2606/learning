"""
commandHandler — обработчики команд пользователя.

Модуль содержит функции-обработчики для каждой поддерживаемой команды.
Вызывается из workflowLib.proceed_command().

Использование:
    from commandHandler import command_help, command_exit
"""
from BusinessLogic.marketList import get_all_markets


def command_help():
    return True
def command_exit():
    return False

def command_list():
    return True, get_all_markets()