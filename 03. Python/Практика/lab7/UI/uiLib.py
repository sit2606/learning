"""
uiLib — библиотека функций вывода в консоль.

Модуль содержит функции для отображения:
- print_welcome(): приветствие
- print_help(): справка по командам
- print_list_all(markets): полный список рынков
- print_list(markets, start, step): список с пагинацией
- print_ordered_instruction(): инструкция по сортировке
- print_exit(): сообщение о завершении

Использование:
    from UI.uiLib import print_welcome, print_help, print_list
"""


from UI.columnToRu import COLUMNS


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
def print_table_header():
    header = ''
    for column in COLUMNS.values():
        header += ' | ' + column
    print(header)
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
def print_list(markets_for_show, start_pos= 1, step = 10, column_name = None):
    print('======--------------------------------======')
    if column_name is not None:
        print(f'Список всех рынков (сортированный по столбцу "{COLUMNS[column_name]}"):')
    else:
        print('Список всех рынков:')
    print_table_header()
    print('--------------------------------------------')
    end_pos = start_pos + step
    try:
        for number  in range(start_pos, start_pos + step):
            formatted_output = ( ' | ' + str(markets_for_show[number]['number']) +  ' | ' +
                        markets_for_show[number]['market_id'] + ' | ' + markets_for_show[number]['city'] + ' | ' + markets_for_show[number]['county']
                        + ' | ' + markets_for_show[number]['state'] +
                        ' | ' + markets_for_show[number]['marketname']+ ' | ' + markets_for_show[number]['zip'] + ' | ')
            print(formatted_output)
        print('======--------------------------------======')
    except KeyError:
        print('Список закончился')
    return markets_for_show,end_pos,step
def print_ordered_instruction():
    print('======--------------------------------======')
    print_table_header()
    print('Номер - 1')
    print('ID - 2')
    print('город - 3')
    print('графство - 4')
    print('штат - 5')
    print('название рынка - 6')
    print('п. индекс - 7')
    print('======--------------------------------======')