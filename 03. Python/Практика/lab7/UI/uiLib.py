"""
uiLib — библиотека функций вывода в консоль.

Модуль содержит функции для отображения:
- print_welcome(): приветствие
- print_help(): справка по командам (help, list_all, list, show, order, exit)
- print_table_header(): шапка таблицы
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
    print('show - выводит подробную информацию о рынке по ID')
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


def print_detailed_market_info(market_info):
    print('======--------------------------------======')
    print('Основная информация')
    print('ID - ' + market_info['basic_info']['market_id'])
    print('Название рынка: ' + market_info['basic_info']['marketname'])
    address_string = market_info['basic_info']['street'] + ', ' + market_info['basic_info']['city'] + ', '+ market_info['basic_info']['county'] + ', ' +  market_info['basic_info']['state'] + ', ' +  market_info['basic_info']['zip'] + '. '
    print('Адрес: ' + address_string)
    print('Рабочие часы: ')
    print('======--------------------------------======')
    print(market_info['basic_info']['season1date'])
    print(market_info['basic_info']['season1time'])
    print('======--------------------------------======')
    print(market_info['basic_info']['season2date'])
    print(market_info['basic_info']['season2time'])
    print('======--------------------------------======')
    print(market_info['basic_info']['season3date'])
    print(market_info['basic_info']['season3time'])
    print('======--------------------------------======')
    print(market_info['basic_info']['season4date'])
    print(market_info['basic_info']['season4time'])
    print('======--------------------------------======')
    print('Способы связи ')
    for media_name, method_status in market_info['media_info'].items():
        print(media_name + ' - ' + method_status)
    print('======--------------------------------======')
    print('Методы оплаты \n(y - если метод поддерживается,\n n - если метод не поддерживается)')
    for method_name, method_status in market_info['bank_info'].items():
        print(method_name + ' - ' + method_status )
    print('======--------------------------------======')
    print('Продаваемые товары \n(y - если товар продаётся,\n n - если товар не продаётся)')
    for grocery_name, method_status in market_info['grocery_info'].items():
        print(grocery_name + ' - ' + method_status)
    return None