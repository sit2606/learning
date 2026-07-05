"""
commandHandler — обработчики команд пользователя.

Модуль содержит функции-обработчики для каждой команды:
- command_help(): справка
- command_exit(): выход
- command_list_all(): список всех рынков
- command_list(): список с пагинацией
- command_order(): сортировка по колонке
- command_show(market_id): показ данных одного рынка
- register_user(): регистрация нового пользователя
- login_user(): авторизация пользователя

Каждая функция возвращает данные для вывода (не зависит от UI).
Вызывается из workflowLib.proceed_command().

Использование:
    from BusinessLogic.commandHandler import command_help, command_list_all
"""
import uuid

import bcrypt
import getpass

from BusinessLogic.marketList import get_all_markets, get_all_markets_ordered_by_num, get_all_markets_ordered_by_column, \
    prepare_ordered_list, get_market_by_id
from DAL import userLib
from DAL.userLib import get_user_by_username


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
        (True, market_info) — кортеж (статус, данные рынка),
        True — при ошибке (рынок не найден).
    """
    market_info = get_market_by_id(market_id)
    if market_info is None:
        print('Ошибка в ID, попробуйте ещё раз')
        return True
    else:
        return True, market_info


def register_user():
    """
    Регистрация нового пользователя.

    Запрашивает логин, пароль (хешируется через bcrypt), имя и фамилию.
    Проверяет уникальность логина. Ввод 'stop' отменяет регистрацию.

    Returns:
        True — после успешной регистрации или отмены.
    """
    registration_process = True
    while registration_process:
        user_name = input('Введите ваш логин: ')
        match user_name:
            case 'stop':
                return True
            case _:
                user = get_user_by_username(user_name)
                if user is not None:
                    print('Пожалуйста, введите другой username или введите stop для завершения регистрации')
                else:
                    user = {}
                    user.update({'user_name': user_name})
                    user_password = getpass.getpass("Введите ваш пароль: ")
                    password_bytes = user_password.encode('utf-8')
                    salt = bcrypt.gensalt(rounds=12)
                    hashed_password = bcrypt.hashpw(password_bytes, salt)
                    user_password = hashed_password.decode('utf-8')
                    user.update({'password': user_password})
                    user_firstname = input('Введите Ваше имя ')
                    user.update({'firstname': user_firstname})
                    user_lastname = input('Введите Вашу фамилию ')
                    user.update({'lastname': user_lastname})
                    user.update({'location': 'test_location'})
                    userLib.create_user(user)
                    print('Регистрация успешна! Добро пожаловать!')
                    return True


def login_user():
    """
    Авторизация пользователя.

    Запрашивает логин и пароль, проверяет через bcrypt.

    Returns:
        True — всегда (для продолжения работы).
    """
    user = {}
    user_name = input('Введите ваш логин: ')
    user.update({'user_name': user_name})
    user_password = getpass.getpass("Введите ваш пароль: ")
    password_bytes = user_password.encode('utf-8')
    user_in_base = get_user_by_username(user_name)
    is_valid = bcrypt.checkpw(password_bytes, user_in_base['password'].encode('utf-8'))
    if is_valid:
        print('Добро пожаловать!')
    else:
        print('Неверный пароль. Попробуйте ещё раз')
    return True