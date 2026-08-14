"""
workflow — View-контроллер консоли.

Связывает uiLib (ввод/вывод) с AppController (бизнес-логика).
Зависимости только вниз: workflow → uiLib + AppController.

Использование:
    from controller.workflow import run_console
"""
import os
import getpass

from controller.AppController import AppController
from view import uiLib
from view.helpers.column_helper import COLUMNS_INFO


def run_console(controller: AppController):
    """Главный цикл консольного приложения."""
    uiLib.print_welcome()
    run_app = True
    while run_app:
        command = get_command(controller)
        run_app = proceed_command(command, controller)


def directory_creation():
    """Создаёт папку 'files/' для хранения CSV-файлов."""
    try:
        os.makedirs("files", exist_ok=True)
    except Exception as e:
        print(e)
        print("Error in directory_creation")


def get_command(controller: AppController) -> str:
    """Считывает команду пользователя из stdin."""
    return uiLib.print_invitation(controller.user)


def proceed_command(command: str, controller: AppController) -> bool:
    """Маршрутизация и выполнение команды."""
    match command:
        case 'help':
            return _command_help()
        case 'list_all':
            return _command_list_all(controller)
        case 'list':
            return _command_list(controller)
        case 'order':
            return _command_order(controller)
        case 'show':
            return _command_show(controller)
        case 'register':
            return _register_user(controller)
        case 'login':
            return _login_user(controller)
        case 'logout':
            return _logout_user(controller)
        case 'review':
            return _add_review(controller)
        case 'update_user':
            return _update_user(controller)
        case 'filter':
            return _show_filtered(controller)
        case 'delete':
            return _delete_market(controller)
        case 'exit':
            return _command_exit()
        case 'zip':
            return _command_zip(controller)
        case _:
            return _unknown_command()


# ── Простые команды ───────────────────────────────────────


def _command_help() -> bool:
    uiLib.print_help()
    return True


def _command_exit() -> bool:
    uiLib.print_exit()
    return False


def _unknown_command() -> bool:
    uiLib.print_unknown_command()
    return True


# ── Рынки: просмотр ──────────────────────────────────────


def _command_list_all(controller: AppController) -> bool:
    market_list = controller.get_all_markets()
    if market_list is None:
        uiLib.print_input_error()
    else:
        uiLib.print_list(market_list)
    return True


def _command_list(controller: AppController) -> bool:
    market_list = controller.get_all_markets()
    if market_list is None:
        uiLib.print_input_error()
        return True

    start_pos, step = uiLib.request_start_and_step()
    uiLib.print_list(markets_for_show=market_list, start_pos=start_pos, step=step)

    is_continue = True
    while is_continue:
        continue_command = uiLib.request_continue()
        match continue_command:
            case 'y':
                market_list, start_pos, step = uiLib.print_list(
                    markets_for_show=market_list, step=step, start_pos=start_pos)
            case 'n':
                is_continue = False
            case _:
                uiLib.print_input_error()
    return True


def _command_order(controller: AppController) -> bool:
    uiLib.print_header_numbers()
    uiLib.print_table_header()
    column, order = uiLib.request_column_and_order()

    markets, column_info = controller.get_ordered_markets(column, order)
    if markets is None:
        uiLib.print_input_error()
        return True

    ordered_list, position, step = uiLib.print_list(
        markets_for_show=markets, column_name=column_info, step=10)

    is_continue = True
    while is_continue:
        continue_command = uiLib.request_continue()
        match continue_command:
            case 'y':
                ordered_list, position, step = uiLib.print_list(
                    markets_for_show=ordered_list, column_name=column_info,
                    step=step, start_pos=position)
            case 'n':
                is_continue = False
            case _:
                uiLib.print_input_error()
    return True


def _command_show(controller: AppController) -> bool:
    market_id = uiLib.request_market_id()
    market_info = controller.get_market_by_id(market_id)
    if market_info is None:
        uiLib.print_invalid_id_error()
        return True

    uiLib.print_detailed_market_info(market_info.get_ui_dict())
    should_continue = uiLib.request_review_for_market()

    match should_continue:
        case 'y':
            reviews, score = controller.get_market_reviews(market_id)
            uiLib.print_market_reviews(reviews, score)
    return True


def _command_zip(controller: AppController) -> bool:
    postalcode = input('Введите индекс: ')
    dist = input('Введите радиус поиска: ')

    result = controller.search_by_zip(postalcode, dist)
    if result is None:
        print('Неверный индекс')
    else:
        uiLib.print_list(result[0], column_name=COLUMNS_INFO[9])
    return True


# ── Рынки: фильтрация ────────────────────────────────────


def _show_filtered(controller: AppController) -> bool:
    if not controller.is_logged_in():
        print('Чтобы отфильтровать рынки, вы должны войти в Систему.')
        return True

    column, filter_value = uiLib.request_filter()
    if column is None and filter_value is None:
        return True

    markets, column_info = controller.get_filtered_markets(column, filter_value)
    uiLib.print_list(markets, column_name=COLUMNS_INFO[column])
    return True


# ── Рынки: удаление ──────────────────────────────────────


def _delete_market(controller: AppController) -> bool:
    if not controller.is_logged_in():
        print('Для удаления рынков необходимо войти в Систему')
        return True

    market_id = uiLib.request_market_id()
    market_info = controller.get_market_by_id(market_id)
    if market_info is None:
        uiLib.print_invalid_id_error()
        return True

    uiLib.print_detailed_market_info(market_info.get_ui_dict())

    delete_process = True
    while delete_process:
        command = input(
            'Введите `yes` чтобы удалить рынок. Операцию удаления нельзя отменить! \n'
            'Введите `back` чтобы выйти из удаления\n')
        match command:
            case 'yes':
                controller.delete_market(market_id)
                print(f'Рынок {market_id} успешно удалён!')
                delete_process = False
            case 'back':
                print('Удаление рынка прервано')
                delete_process = False
            case _:
                print('Команда не распознана')
    return True


# ── Пользователи ─────────────────────────────────────────


def _register_user(controller: AppController) -> bool:
    registration_process = True
    while registration_process:
        user_name = input('Введите ваш логин: ')
        user_password = getpass.getpass("Введите ваш пароль: ")
        firstname = input('Введите Ваше имя: ')
        lastname = input('Введите Вашу фамилию: ')

        command = input(
            'Вы хотите указать свои координаты?\n'
            'Введите `y` чтобы указать\n'
            'Введите `n` чтобы не указывать\n')
        match command:
            case 'y':
                latitude, longitude = uiLib.get_user_coordinates_manually()
                latitude = str(latitude) if latitude is not None else ''
                longitude = str(longitude) if longitude is not None else ''
            case _:
                latitude, longitude = '', ''

        user = controller.register(user_name, user_password, firstname, lastname, latitude, longitude)
        if user is not None:
            print('Регистрация успешна! Добро пожаловать!')
            registration_process = False
        else:
            print('Пожалуйста, введите другой username или введите stop для завершения регистрации')
            stop = input()
            if stop == 'stop':
                registration_process = False
    return True


def _login_user(controller: AppController) -> bool:
    if controller.is_logged_in():
        print("Вы уже вошли в Систему")
        return True

    user_name = input('Введите ваш логин: ')
    user_password = getpass.getpass("Введите ваш пароль: ")

    user = controller.login(user_name, user_password)
    if user is not None:
        print('Добро пожаловать!')
    else:
        print('Пользователь не найден или неверный пароль')
    return True


def _logout_user(controller: AppController) -> bool:
    if not controller.is_logged_in():
        print('Чтобы выйти, нужно войти')
    else:
        controller.logout()
        print('Вы успешно вышли из системы')
    return True


def _update_user(controller: AppController) -> bool:
    if not controller.is_logged_in():
        print('Чтобы изменить пользователя, вы должны войти в Систему.')
        return True

    field, value = uiLib.request_user_updates(controller.user)
    if field is None:
        return True

    if field == 'coordinates':
        controller.update_user(latitude=value[0], longitude=value[1])
    else:
        controller.update_user(**{field: value})
    return True


# ── Отзывы ───────────────────────────────────────────────


def _add_review(controller: AppController) -> bool:
    if not controller.is_logged_in():
        print('Чтобы оставить отзыв на рынок, вы должны войти в Систему.')
        return True

    market_id = uiLib.request_market_id()
    market_info = controller.get_market_by_id(market_id)
    if market_info is None:
        uiLib.print_invalid_id_error()
        return True

    uiLib.print_detailed_market_info(market_info.get_ui_dict())

    review = True
    while review:
        score = input(
            'Введите оценку по пятибальной шкале, где 1 - плохо, 5 - отлично.\n'
            'Введите `back` чтобы выйти из процесса оценки\n')
        match score:
            case 'back':
                review = False
            case _:
                try:
                    score = int(score)
                    if not (1 <= score <= 5):
                        print('Оценка должна быть от 1 до 5. Попробуйте снова')
                        continue
                    review_text = input(
                        'Введите дополнительный отзыв, или оставьте поле ввода пустым\n')
                    controller.add_review(market_id, score, review_text)
                    print('Оценка успешно добавлена!')
                    review = False
                except ValueError:
                    print('Оценка должна быть целым, положительным числом. Попробуйте снова')
    return True
