"""
workflowLib — модуль оркестрации рабочего процесса.

Зависимости:
- os: работа с файловой системой
- BusinessLogic.commandHandler: обработчики команд
- DAL.fileLib: инициализация CSV-файлов
- DAL.reviewLib: чтение отзывов
- DAL.userLib: чтение данных пользователей
- UI.uiLib: вывод в консоль

Основные функции:
- directory_creation(): создание папки files/
- file_creation(): проверка и пересоздание CSV-файлов
- get_command(user): ввод команды от пользователя (с приветствием для авторизованных)
- proceed_command(command, user): маршрутизация и выполнение команды

Поддерживаемые команды:
- help — справка
- list_all — все рынки
- list — список с пагинацией
- order — сортировка по колонке
- show — данные одного рынка по Id (с просмотром отзывов)
- filter — фильтрация рынков по колонке
- register — регистрация пользователя (с запросом координат)
- login — авторизация пользователя
- logout — выход из системы
- review — добавление отзыва
- update_user — обновление данных пользователя
- delete — удаление рынка и его связей
- exit — выход

Использование:
    from BusinessLogic.workflowLib import directory_creation, file_creation, proceed_command
"""
import os

from BusinessLogic import commandHandler
from DAL import fileLib, requiredFiles, filelib2, datalib2
from DAL.reviewLib import get_review_by_market_id
from DAL.userLib import read_user
from UI import uiLib


def directory_creation():
    """
    Создаёт папку 'files/' для хранения CSV-файлов.

    Использует os.makedirs() с exist_ok=True для безопасного создания.

    Raises:
        Exception: при ошибке создания директории выводит сообщение
        "Error in directory_creation" и текст исключения в консоль.
    """
    try:
        os.makedirs("files", exist_ok=True)
    except Exception as e:
        print(e)
        print("Error in directory_creation")
def file_creation():
    requiredFiles.prepare_refs()
    requiredFiles.create_market_table()
    requiredFiles.create_review_table()
    requiredFiles.create_user_table()
    datalib2.add_many(filelib2.read_csv())
def get_command(user):
    """
    Считывает команду пользователя из stdin.

    Если пользователь авторизован — выводит приветствие с именем.
    Если не авторизован — выводит предупреждение о недоступных функциях.

    Args:
        user: Текущий авторизованный пользователь или None.

    Returns:
        str: введённая пользователем команда.
    """
    if user is None:
        print('Часть функций недоступна, неавторизованным пользователям.\nИспользуйте `login` чтобы войти')
        command = input('Пожалуйста, введите команду: ').strip()
        return command
    else:
        command = input(f'Привет, {str(user.firstname)}! \nПожалуйста, введите команду: ').strip()
        return command
def proceed_command(command, user):
    """
    Обрабатывает команду пользователя и возвращает состояние сессии.

    Args:
        command: Строка команды от пользователя.
        user: Текущий авторизованный пользователь или None.

    Returns:
        (is_run, user) — кортеж (продолжать ли работу, текущий пользователь).
    """
    is_run = True
    match command:
        case 'help':
            uiLib.print_help()
            is_run = commandHandler.command_help()
        case 'list_all':
            is_run, market_list = commandHandler.command_list_all()
            if market_list is None:
                print('Ошибка. Попробуйте ещё раз')
            else:
                uiLib.print_list(market_list)
        case 'list':
            is_run, market_list, start_pos, step = commandHandler.command_list()
            if market_list is None:
                print('Ошибка. Попробуйте ещё раз')
            else:

                uiLib.print_list(markets_for_show= market_list,start_pos=start_pos, step= step)
                is_continue = True
                while is_continue:
                    continue_command = input('Желаете продолжить? Введите \'y\' для продолжения, или \'n\' для завершения: ')
                    match continue_command:
                        case 'y':
                            market_list, start_pos, step = uiLib.print_list(markets_for_show=market_list,
                                                                            step= step,start_pos=start_pos)
                        case 'n':
                            is_continue = False
                        case _:
                            print('Ошибка ввода')
        case 'order':
            uiLib.print_header_numbers()
            uiLib.print_table_header()
            is_run, market_list, column, order = commandHandler.command_order()
            if market_list is None:
                print('Ошибка. Попробуйте ещё раз')
            else:
                ordered_list, position, step = uiLib.print_list(markets_for_show=market_list, column_name= column, step= 10)
                is_continue = True
                while is_continue:
                    continue_command = input('Желаете продолжить? Введите \'y\' для продолжения, или \'n\' для завершения: ')
                    match continue_command:
                        case 'y':
                            ordered_list, position, step = uiLib.print_list(markets_for_show=ordered_list, column_name= column,
                                                                            step= step,start_pos=position)
                        case 'n':
                            is_continue = False
                        case _:
                            print('Ошибка ввода')
        case 'show':
            try:
                is_run, market_info = commandHandler.command_show()
                if market_info is None:
                    return is_run, user
                uiLib.print_detailed_market_info(market_info.get_ui_dict())
                should_continue = input('Если хотите увидеть отзывы на рынок, введите `y`\n'
                                        'Если хотите вернуться к вводу команд, нажмите Enter\n')
                match should_continue:
                    case 'y':
                        reviews = get_review_by_market_id(market_info["basic_info"]["market_id"])
                        for review in reviews:
                            review_author = read_user(review["user_id"])
                            review.update({"user_name": review_author["firstname"] + " " + review_author["lastname"]})
                        uiLib.print_market_reviews(reviews, market_info['basic_info']['score'])
                    case  _:
                        return is_run, user
            except ValueError:
                print('Пожалуйста, введите число.')
        case 'register':
            is_run, user = commandHandler.register_user()
        case 'login':
            is_run, user = commandHandler.login_user(user)
        case 'logout':
            is_run, user = commandHandler.logout_user(user)
        case 'review':
            is_run, user = commandHandler.add_review(user)
        case 'update_user':
            is_run, user = commandHandler.update_user(user)
        case 'filter':
            is_run, user = commandHandler.show_filtered(user)
        case 'delete':
            is_run, user = commandHandler.delete_market(user)
        case 'exit':
            uiLib.print_exit()
            is_run = commandHandler.command_exit()
        case _:
            print('Такой команды нет. Введите help, чтобы вывести список всех команд')
    return is_run, user
