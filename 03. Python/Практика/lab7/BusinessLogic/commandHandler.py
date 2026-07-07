"""
commandHandler — обработчики команд пользователя.

Модуль содержит функции-обработчики для каждой команды:
- command_help(): справка
- command_exit(): выход
- command_list_all(): список всех рынков
- command_list(): список с пагинацией
- command_order(column, order): сортировка по колонке (с optional параметрами)
- command_show(): показ данных одного рынка (запрашивает ID внутри)
- register_user(): регистрация нового пользователя
- login_user(user): авторизация пользователя
- logout_user(user): выход из системы
- add_review(user): добавление отзыва на рынок
- show_filtered(): фильтрация рынков по колонке (через UI.request_filter)

Зависимости:
- uuid, datetime: генерация ID и дат
- bcrypt, getpass: хеширование паролей
- BusinessLogic.marketList: бизнес-логика рынков
- DAL.userLib, DAL.reviewLib: доступ к данным пользователей и отзывов
- UI.uiLib: ввод фильтра и справка по колонкам
- UI.column_helper: COLUMNS_INFO для маппинга номеров колонок

Каждая функция возвращает кортеж (статус, данные) для передачи в UI.
Вызывается из workflowLib.proceed_command().

Использование:
    from BusinessLogic.commandHandler import command_help, command_list_all
"""
import uuid
from datetime import datetime


import bcrypt
import getpass

from BusinessLogic.marketList import  get_all_markets, get_all_markets_ordered_by_column, \
    prepare_ordered_list, get_market_by_id, get_all_markets_filtered_by_column
from DAL import userLib
from DAL.reviewLib import create_review, calculate_score
from DAL.userLib import get_user_by_username
from UI import uiLib
from UI.column_helper import COLUMNS_INFO


def command_help():
    """Возвращает True для продолжения работы."""
    return True


def command_exit():
    """Возвращает False для завершения работы."""
    return False


def command_list_all():
    """Возвращает (True, dict_всех_рынков)."""
    return True, get_all_markets('num')


def command_list():
    """
    Запрашивает у пользователя стартовую позицию и шаг.
    Возвращает (True, dict_рынков_с_нумерацией, старт, шаг).
    """
    start_num = int(input('Введите стартовый номер: ')) or 1
    step = int(input('Введите  шаг: ')) or 10
    return True, get_all_markets('num'), start_num, step


def command_order(column = None, order = None, start_num = None, step = None):
    """
    Сортирует список рынков по указанной колонке.

    Если column и order не заданы — запрашивает у пользователя.
    Возвращает (True, dict_рынков, колонка, порядок).

    Args:
        column: номер колонки (1-8) или None для запроса у пользователя.
        order: порядок сортировки ('a'/'d') или None для запроса у пользователя.
        start_num: стартовая позиция (не используется в текущей реализации).
        step: шаг пагинации (не используется в текущей реализации).

    Returns:
        tuple: (True, markets, column_info, order).
    """
    if column is None and order is None:
        column = int(input('Введите номер колонки, по которой вы хотите отсортировать список: '))
        order = input('Введите порядок сортировки d - от большего к меньшему, a - от меньшего к большему: ')
    markets, column = get_all_markets_ordered_by_column(column, order)
    markets = prepare_ordered_list(markets)
    return True, markets, column, order


def command_show():
    """
    Запрашивает у пользователя ID рынка и получает его данные.

    Returns:
        (True, market_info) — кортеж (статус, данные рынка),
        (True, None) — при ошибке (рынок не найден).
    """
    market_id = int(input('Введите ID рынка: '))
    market_info = get_market_by_id(market_id)
    if market_info is None:
        print('Ошибка в ID, попробуйте ещё раз')
        return True, None
    else:
        return True, market_info


def register_user():
    """
    Регистрация нового пользователя.

    Запрашивает логин, пароль (хешируется через bcrypt), имя и фамилию.
    Проверяет уникальность логина. Ввод 'stop' отменяет регистрацию.

    Returns:
        (True, user) — после успешной регистрации,
        (True, None) — при отмене или ошибке.
    """
    registration_process = True
    while registration_process:
        user_name = input('Введите ваш логин: ')
        match user_name:
            case 'stop':
                return True, None
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
                    user = get_user_by_username(user_name)
                    print('Регистрация успешна! Добро пожаловать!')
                    return True, user
def login_user(user):
    """
    Авторизация пользователя.

    Если пользователь уже авторизован — выводит сообщение и возвращает текущего пользователя.
    Иначе запрашивает логин и пароль, проверяет через bcrypt.

    Args:
        user: Текущий авторизованный пользователь или None.

    Returns:
        (True, user) — после успешной авторизации или если уже авторизован,
        (True, None) — при ошибке (пользователь не найден или неверный пароль).
    """
    if user is None:
        user = {}
        user_name = input('Введите ваш логин: ')
        user_in_base = get_user_by_username(user_name)
        if user_in_base is None:
            print('Пользователь не найден, попробуйте снова')
            return True, None
        else:
            user.update({'user_name': user_name})
            user_password = getpass.getpass("Введите ваш пароль: ")
            password_bytes = user_password.encode('utf-8')
            is_valid = bcrypt.checkpw(password_bytes, user_in_base['password'].encode('utf-8'))
            if is_valid:
                print('Добро пожаловать!')
                return True, user_in_base
            else:
                print('Неверный пароль. Попробуйте ещё раз')
                return True, None
    else:
        print("Вы уже вошли в Систему")
        return True, user

def logout_user(user):
    """
    Выход пользователя из системы.

    Args:
        user: Текущий авторизованный пользователь.

    Returns:
        (True, None) — всегда сбрасывает пользователя.
    """
    if user is None:
        print('Чтобы выйти, нужно войти')
        return True, None
    else:
        user = None
        print('Вы успешно вышли из системы')
        return True, user


def add_review(user):
    """
    Добавление отзыва на рынок.

    Требуется авторизация. Запрашивает ID рынка, оценку (1-5) и опциональный текст.
    Сохраняет отзыв в файл REVIEWS.csv.

    Args:
        user: Текущий авторизованный пользователь или None.

    Returns:
        (True, user) — после успешного добавления отзыва или если не авторизован.
    """
    if user is None:
        print('Чтобы оставить отзыв на рынок, вы должны войти в Систему.')
        return True, user
    else:
            status, market_info = command_show()
            if market_info is None:
                return True, user
            else:
                review = True
                while review:
                    score = input('Введите оценку по пятибальной шкале, где 1 - плохо, 5 - отлично. \nВведите `back`'
                                  'чтобы выйти из процесса оценки\n')
                    match score:
                        case 'back':
                            review = False
                            return True, user
                        case _:
                            try:
                                score = int(score)
                                if not (1 <= score <= 5):
                                    print('Оценка должна быть от 1 до 5. Попробуйте снова')
                                    continue
                                review_text = input('Введите дополнительный отзыв, или оставьте поле ввода пустым, если не хотите\n'
                                      'добавлять развёрнутый отзыв \n')
                                review = {}
                                review["Id"] = str(uuid.uuid4())
                                review['review_date'] = str(datetime.now())
                                review['user_id'] = user['Id']
                                review['market_id'] = market_info['basic_info']['market_id']
                                review['review_text'] = review_text
                                review['score'] = score
                                create_review(review)
                                print('Оценка успешно добавлена!')
                                calculate_score(market_info['basic_info']['market_id'])
                                return True, user
                            except ValueError:
                                print('Оценка должна быть целым, положительным числом. Попробуйте снова')
                                continue





def show_filtered():
    """
    Фильтрует список рынков по критерию, введённому пользователем.

    Использует uiLib.request_filter() для получения номера колонки
    и значения фильтра. Для текстовых колонок — точное совпадение.
    Для числовых — сравнение с оператором (>, <, >=, <=, =).

    Returns:
        True — статус продолжения работы.
    """
    column, filter_value = uiLib.request_filter()
    if column is None and filter_value is None:
        return True
    get_all_markets_filtered_by_column(COLUMNS_INFO[column], filter_value)
    return True