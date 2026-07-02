"""
uiLib — библиотека функций вывода в консоль (UI).

Модуль содержит функции для вывода приветствия, справки
по командам, списков рынков (полный, с пагинацией, отсортированный)
и сообщения о завершении работы.

Использование:
    from uiLib import print_welcome, print_help, print_list_all, print_list, print_list_ordered, print_exit
"""


def print_welcome():
    print('======--------------------------------======')
    print('Добро пожаловать в приложение для просмотра')
    print('информации о фермерских рынках США')
    print('======--------------------------------======')

def print_help():
    print('Доступные команды:')
    print('list_all - выводит таблицу со списком всех рынков')
    print('list - выводит таблицу рынков с пагинацией')
    print('help - выводит перечень всех доступных команд')
    print('order - выводит таблицу рынков отсортированных по колонке')
    print('exit - завершает работу приложения')

def print_exit():
    print('======--------------------------------======')
    print('Программа завершает работу!')
    print('======--------------------------------======')
def print_list_all(markets):
    print('======--------------------------------======')
    print('Список всех рынков:')
    for market_id, market_info in markets.items():
        formatted_output = (str(market_id) + ' | ' +  market_info['city'] + ' | ' + market_info['county'] + ' | ' + market_info['state'] +
                            ' | ' + market_info['marketname'] +' | '+ market_info['zip'])
        print(formatted_output)
        print('--------------------------------------------')
    print('======--------------------------------======')
def print_list(markets, start_pos, step):
    print('======--------------------------------======')
    print('Список всех рынков:')
    header = 'Номер | ID | город | графство | штат | название рынка | п. индекс | '
    print(header)
    print('--------------------------------------------')
    for number  in range(start_pos, start_pos + step):
        formatted_output = ( str(markets[number]['number']) +  ' | ' +
                    markets[number]['market_id'] + ' | ' + markets[number]['city'] + ' | ' + markets[number]['county']
                    + ' | ' + markets[number]['state'] +
                    ' | ' + markets[number]['marketname']+ ' | ' + markets[number]['zip'] + ' | ')
        print(formatted_output)
    print('======--------------------------------======')
def print_list_ordered(markets):
    print('======--------------------------------======')
    print('Список всех рынков (сортированный):')
    header = 'Номер | ID | город | графство | штат | название рынка | п. индекс | '
    print(header)
    print('--------------------------------------------')
    for market_id, market_info in markets.items():
        formatted_output = ( ' | ' + str(market_info['number']) + ' | ' +
                    str(market_id) + ' | ' + market_info['city'] + ' | ' + market_info['county'] + ' | ' + market_info[
                'state'] +
                    ' | ' + market_info['marketname'] + ' | ' + market_info['zip'])
        print(formatted_output)
    print('======--------------------------------======')