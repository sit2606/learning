"""
uiLib — библиотека функций вывода в консоль (UI).

Модуль содержит функции для вывода приветствия, справки
по командам, списка рынков и сообщения о завершении работы.

Использование:
    from uiLib import print_welcome, print_help, print_list, print_exit
"""


def print_welcome():
    print('======--------------------------------======')
    print('Добро пожаловаться в приложение по просмотру')
    print('информации о фермерских рынках США')
    print('======--------------------------------======')

def print_help():
    print('Доступные команды:')
    print('list - выводит таблицу со списком всех рынков')
    print('help - выводит перечень всех доступных команд')
    print('exit - завершает работу приложения')

def print_exit():
    print('======--------------------------------======')
    print('Программа завершает работу!')
    print('======--------------------------------======')
def print_list(markets):
    print('======--------------------------------======')
    print('Список всех рынков:')
    for market_id, market_info in markets.items():
        formatted_output = (str(market_id) + ' | ' +  market_info['city'] + ' | ' + market_info['county'] + ' | ' + market_info['state'] +
                            ' | ' + market_info['marketname'] +' | '+ market_info['zip'])
        print(formatted_output)
        print('--------------------------------------------')
    print('======--------------------------------======')