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
from UI.column_helper import COLUMNS, COLUMNS_INFO
from UI.comparison_helper import COMPARISON_SIGNS


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
def print_list(markets_for_show, start_pos= 1, step = 10000, column_name = None):
    print('======--------------------------------======')
    if column_name is not None:
        print(f'Список всех рынков (сортированный по столбцу "{COLUMNS[column_name['name']]}"):')
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

def print_comparison_rules():
    print('======--------------------------------======')
    print('Введите критерий, по которому нужно отфильтровать выборку')
    print('Критерий вводится в виде формулы:')
    print('> - больше чем')
    print('< - меньше чем')
    print('>= - больше чем или равно')
    print('<= -  меньше чем или равно')
    print('= равно')
    print('Пример: \n')
    print('> 30  выведет все записи, которые строго больше 30')
    print('Лучше всего отделить число от знака пробелом')
def request_filter():
    print_header_numbers()
    filter_input = True
    while filter_input:
        user_input = input('Введите номер колонки, по которой вы хотите отфильтровать список\n'
                           'или введите `back` чтобы вернуться \n' )
        match user_input:
            case 'back':
                return None,None
            case _:
                try:
                    column = int(user_input)
                    if COLUMNS_INFO[column]['type'] == 'text':
                        return_filter = ''
                        match COLUMNS_INFO[column]['name']:
                            case 'city':
                                return_filter = input('Введите название города на английском языке ').strip().capitalize()
                            case 'state':
                                return_filter = input('Введите название штата на английском языке ').strip().capitalize()
                            case 'marketname':
                                return_filter = input('Введите название рынка на английском языке ').strip().capitalize()
                            case 'county':
                                return_filter = input('Введите название графства на английском языке ').strip().capitalize()
                        return column, return_filter
                    if COLUMNS_INFO[column]['type'] == 'numeric':
                            sign = ''
                            filter_value = ''
                            print_comparison_rules()
                            match COLUMNS_INFO[column]['name']:
                                case 'number':
                                    filter_value = input('Введите критерий сравнения\n')
                                case 'market_id':
                                    filter_value = input('Введите критерий сравнения\n')
                                case 'zip':
                                    filter_value = input('Введите критерий сравнения\n')
                                case 'score':
                                    filter_value = input('Введите критерий сравнения\n')
                            match filter_value:
                                case _:
                                    for symbol in filter_value.strip().split(' '):
                                        if symbol in COMPARISON_SIGNS:
                                            sign = symbol
                                        elif symbol.isnumeric():
                                            filter_value = str(symbol)
                                            return_filter = (sign,filter_value)
                                            return column, return_filter
                                        else:
                                            print('Ошибка ввода формулы. Попробуйте снова или введите `back` для выхода')
                except Exception as e:
                    print(e)
                    print('Что то пошло не так')
                    return None,None
    return None, None
