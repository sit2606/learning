"""
commandHandler — обработчики команд пользователя.

Модуль содержит функции-обработчики для каждой команды:
- command_help(): справка
- command_exit(): выход
- command_list_all(): список всех рынков
- command_list(): список с пагинацией
- command_order(): сортировка по колонке
- command_show(market_id): показ данных одного рынка

Каждая функция возвращает данные для вывода (не зависит от UI).
Вызывается из workflowLib.proceed_command().

Использование:
    from BusinessLogic.commandHandler import command_help, command_list_all
"""
from BusinessLogic.marketList import get_all_markets, get_all_markets_ordered_by_num, get_all_markets_ordered_by_column, \
    prepare_ordered_list, get_market_by_id


def command_help():
    """Возвращает True для продолжения работы."""
    return True


def command_exit():
    """Возвращает False для завершения работы."""
    return False


def command_list_all():
    """Возвращает (True, dict_всех_рынков)."""
    return True, get_all_markets()


def command_list():
    """
    Запрашивает у пользователя стартовую позицию и шаг.
    Возвращает (True, dict_рынков_с_нумерацией, старт, шаг).
    """
    start_num = int(input('Введите стартовый номер: ')) or 1
    step = int(input('Введите  шаг: ')) or 10
    return True, get_all_markets_ordered_by_num(), start_num, step


def command_order():
    """
    Запрашивает у пользователя номер колонки и порядок сортировки.
    Возвращает (True, dict_рынков, имя_колонки, порядок).
    """
    column = int(input('Введите номер колонки, по которой вы хотите отсортировать список: '))
    order = input('Введите порядок сортировки d - от большего к меньшему, a - от меньшего к большему: ')
    markets, column = get_all_markets_ordered_by_column(column, order)
    markets = prepare_ordered_list(markets)
    return True, markets, column, order


def command_show(market_id):
    """
    Получает данные одного рынка по Id.

    Args:
        market_id: Идентификатор рынка.

    Returns:
        None при успехе (данные выводятся в консоль),
        True при ошибке (для продолжения работы).
    """
    market_info = get_market_by_id(market_id)
    if market_info is None:
        print('Ошибка в ID, попробуйте ещё раз')
        return True
    else:
        print('s')
    return None