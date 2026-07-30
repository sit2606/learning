"""
commandHandler — обработчики команд пользователя.

Модуль содержит функции-обработчики для каждой команды:
- command_help(): справка
- command_exit(): выход
- command_list_all(): список всех рынков
- command_list(): список с пагинацией
- command_order(column, order): сортировка по колонке (с optional параметрами)
- command_show(): показ данных одного рынка (запрашивает ID внутри)
- register_user(): регистрация нового пользователя (с запросом координат)
- login_user(user): авторизация пользователя
- logout_user(user): выход из системы
- add_review(user): добавление отзыва на рынок
- show_filtered(user): фильтрация рынков по колонке (через UI.request_filter)
- update_user(user): обновление данных пользователя
- delete_market(user): удаление рынка и его связей

Зависимости:
- uuid, datetime: генерация ID и дат
- bcrypt, getpass: хеширование паролей
- BusinessLogic.marketList: бизнес-логика рынков
- BusinessLogic.geoLib: расчёт расстояний (для фильтрации distance)
- DAL.userLib, DAL.reviewLib, DAL.dataLib, DAL.referenceLib: доступ к данным
- UI.uiLib: ввод координат, фильтра, обновление пользователя
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



from BusinessLogic.market_queries import get_markets_ordered_by_mode, get_all_markets_ordered_by_column, \
    prepare_ordered_list, get_market_by_id, get_all_markets_filtered_by_column
from DAL import userLib,  dataLib, referenceLib
from DAL.reviewLib import create_review, calculate_score
from UI import uiLib
from UI.column_helper import COLUMNS_INFO
from models.entities.user import User


def command_help():
    """Возвращает True для продолжения работы."""
    return True


def command_exit():
    """Возвращает False для завершения работы."""
    return False


def command_list_all():
    """Возвращает (True, dict_всех_рынков)."""
    return True, get_markets_ordered_by_mode('num')

def command_list():
    """
    Запрашивает у пользователя стартовую позицию и шаг.
    Возвращает (True, dict_рынков_с_нумерацией, старт, шаг).
    """
    start_input = input('Введите стартовый номер: ').strip()
    start_num = int(start_input) if start_input else 1
    step_input = input('Введите  шаг: ').strip()
    step = int(step_input) if step_input else 10
    return True, get_markets_ordered_by_mode('num'), start_num, step


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

    Обрабатывает ValueError при вводе нечислового ID.

    Returns:
        (True, market_info) — кортеж (статус, данные рынка),
        (True, None) — при ошибке (рынок не найден или неверный ввод).
    """
    try:
        market_id = int(input('Введите ID рынка: '))
        market_info = get_market_by_id(market_id)
        if market_info is None:
            print('Ошибка в ID, попробуйте ещё раз')
            return True, None
        else:
            return True, market_info
    except ValueError:
        print('ID рынка должно быть числом')
        return True, None


def register_user():
    """
    Регистрация нового пользователя.

    Запрашивает логин, пароль (хешируется через bcrypt), имя и фамилию.
    Предлагает указать координаты (широта, долгота) для фильтрации по дистанции.
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
                user = User.from_db(username = user_name)
                if user.username == user_name:
                    print('Пожалуйста, введите другой username или введите stop для завершения регистрации')
                else:
                    user.username = user_name
                    user_password = getpass.getpass("Введите ваш пароль: ")
                    password_bytes = user_password.encode('utf-8')
                    salt = bcrypt.gensalt(rounds=12)
                    hashed_password = bcrypt.hashpw(password_bytes, salt)
                    user_password = hashed_password.decode('utf-8')
                    user.password = user_password
                    user.firstname = input('Введите Ваше имя ')
                    user.lastname = input('Введите Вашу фамилию ')
                    command = input('Вы хотите указать свои координаты?\n'
                                    'Введите `y` чтобы указать\n'
                                    'Введите `n` чтобы не указывать (координаты нужны, чтобы работала'
                                    'функция определения дистанции до рынков\n')
                    match command:
                        case 'y':
                            latitude, longitude = uiLib.get_user_coordinates_manually()
                            user.latitude = str(latitude)
                            user.longitude = str(longitude)
                        case 'n':
                            user.latitude, user.longitude = ('','')
                        case _:
                            print('Команда не распознана, вы сможете указать координаты позже')
                            user.latitude, user.longitude = ('','')
                    user.add_to_db()
                    print('Регистрация успешна! Добро пожаловать!')
                    return True, user
def login_user(user):
    if user is None:
        user_name = input('Введите ваш логин: ')
        user_in_base = User.from_db(username = user_name)
        if user_in_base.username != user_name:
            print('Пользователь не найден, попробуйте снова')
            return True, None
        else:
            user_password = getpass.getpass("Введите ваш пароль: ")
            password_bytes = user_password.encode('utf-8')
            is_valid = bcrypt.checkpw(password_bytes, user_in_base.password.encode('utf-8'))
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

def show_filtered(user):
    """
    Фильтрует список рынков по критерию, введённому пользователю.

    Требуется авторизация. Использует uiLib.request_filter() для получения
    номера колонки и значения фильтра. Поддерживает фильтрацию по расстоянию.

    Args:
        user: Текущий авторизованный пользователь или None.

    Returns:
        (True, user) — статус продолжения работы.
    """
    if user is None:
        print('Чтобы отфильтровать рынки, вы должны войти в Систему.')
        return True, user
    column, filter_value = uiLib.request_filter()
    if column is None and filter_value is None:
        return True, user
    markets_to_show = get_all_markets_filtered_by_column(column, filter_value, user)

    uiLib.print_list(markets_to_show[0], column_name=COLUMNS_INFO[column])
    return True, user
def update_user(user):
    """
    Обновление данных пользователя.

    Требуется авторизация. Использует uiLib.request_user_updates()
    для получения изменений, затем сохраняет через userLib.update_user().

    Args:
        user: Текущий авторизованный пользователь или None.

    Returns:
        (True, user) — обновлённый пользователь,
        (True, None) — если не авторизован.
    """
    if user is None:
        print('Чтобы изменить пользователя, вы должны войти в Систему.')
        return True, user
    user = uiLib.request_user_updates(user)
    userLib.update_user(user)
    return True, user


def delete_market(user):
    """
    Удаление рынка и его связей.

    Требуется авторизация. Запрашивает ID рынка, показывает данные,
    запрашивает подтверждение удаления. Удаляет рынок из MARKET_INFO.csv
    и все связанные записи из MarketXBankingInfo, MarketXGrocery, MarketXSocialMedia.

    Args:
        user: Текущий авторизованный пользователь или None.

    Returns:
        (True, user) — после удаления или отмены,
        (True, None) — если не авторизован.
    """
    if user is None:
        print('Для удаления рынков необходимо войти в Систему')
        return True, user
    else:
            delete_process = True
            status, market_info = command_show()
            if market_info is None:
                return True, user
            else:
                while delete_process:
                    command = input('Введите `yes` чтобы удалить рынок. Операцию удаления нельзя отменить! \nВведите `back`'
                                  'чтобы выйти из удаления\n')
                    match command:
                        case 'yes':
                            dataLib.delete_market(market_info)
                            referenceLib.delete_all_connections_by_market_id(market_id= market_info['basic_info']['market_id'],reference_name= 'MarketXBankingInfo')
                            referenceLib.delete_all_connections_by_market_id(market_id= market_info['basic_info']['market_id'], reference_name='MarketXGrocery')
                            referenceLib.delete_all_connections_by_market_id(market_id= market_info['basic_info']['market_id'],reference_name='MarketXSocialMedia')
                            print(f'Рынок {market_info['basic_info']['market_id']} успешно удалён!')
                            return True, user
                        case 'back':
                            print('Удаление рынка прервано')
                            return True, user
                        case _:
                            print('Команда не распознана')
    return None