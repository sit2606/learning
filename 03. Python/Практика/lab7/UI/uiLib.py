"""
uiLib — библиотека функций вывода в консоль.

Модуль содержит функции для отображения:
- print_welcome(): приветствие
- print_help(): справка по командам
- print_table_header(): шапка таблицы (русские названия колонок)
- print_header_numbers(): нумерация колонок для сортировки/фильтрации
- print_list_all(markets): полный список рынков
- print_list(markets, start, step): список с пагинацией
- print_exit(): сообщение о завершении
- print_detailed_market_info(market_info): подробная информация о рынке
- print_market_reviews(reviews, average_score): вывод отзывов о рынке

Использование:
    from UI.uiLib import print_welcome, print_help, print_list, print_detailed_market_info
"""


from UI.column_helper import COLUMNS


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
    print('register - запускает процедуру регистрации пользователя')
    print('review - добавить отзыв к рынку')
    print('filter - вывести отфильтрованный по какому-либо критерию список рынков')
    print('login - войти в приложение со своим логином\\паролем')
    print('logout - выйти из приложения')
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
                        ' | ' + markets_for_show[number]['marketname']+ ' | ' + markets_for_show[number]['zip'] + ' | '
                                 + markets_for_show[number]['score'] + ' | '
                                 )
            print(formatted_output)
        print('======--------------------------------======')
    except KeyError:
        print('Список закончился')
    return markets_for_show,end_pos,step
def print_header_numbers():
    """Выводит шапку таблицы с номерами колонок для сортировки и фильтрации."""
    print('======--------------------------------======')
    print_table_header()
    print('Номер - 1')
    print('ID - 2')
    print('город - 3')
    print('графство - 4')
    print('штат - 5')
    print('название рынка - 6')
    print('п. индекс - 7')
    print('ср. оценка - 8')
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


def print_market_reviews(reviews, average_score):
    """
    Выводит список отзывов о рынке и среднюю оценку.

    Args:
        reviews (list): Список словарей с отзывами (user_name, score, review_text).
        average_score (float): Средняя оценка рынка.
    """
    print('======--------------------------------======')
    if len(reviews) == 1:
        print(f'На основании {len(reviews)} отзыва средняя оценка рынка:  {average_score}')
    else:
        print(f'На основании {len(reviews)} отзывов средняя оценка рынка:  {average_score}')
    for review in reviews:
        print('======--------------------------------======')
        print(f'Автор рецензии {review["user_name"]}')
        print(f'Оценка: {review["score"]}')
        print(f'Текст рецензии')
        print(review['review_text'])
    return None