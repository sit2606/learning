"""
commandHandler — обработчики команд пользователя.

Модуль содержит функции-обработчики для каждой поддерживаемой команды.
Каждая функция возвращает данные для вывода (не зависит от UI).
Вызывается из workflowLib.proceed_command().

Использование:
    from BusinessLogic.commandHandler import command_help, command_list, command_exit
"""
from BusinessLogic.marketList import get_all_markets


def command_help():
    return True
def command_exit():
    return False

def command_list():
    return True, get_all_markets()