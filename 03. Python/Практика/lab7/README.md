# Лабораторная работа 7 — Управление данными о фермерских рынках

## Описание

Приложение для парсинга CSV-датасета фермерских рынков (Export.csv), создания справочников и связывания данных через промежуточные CSV-файлы. Построено по трёхуровневой архитектуре: UI → BusinessLogic → DAL.

## Структура проекта

```
lab7/
├── App.py                          # Точка входа приложения
├── BusinessLogic/                  # Слой бизнес-логики
│   ├── workflowLib.py              # Оркестрация процесса и обработка команд
│   ├── commandHandler.py           # Обработчики команд
│   ├── marketList.py               # Бизнес-логика получения списка рынков
│   ├── processFilter.py            # Обработка фильтрации рынков
│   └── geoLib.py                   # Библиотека геоданных и расчёта дистанций
├── DAL/                            # Слой доступа к данным (Data Access Layer)
│   ├── fileLib.py                  # Парсинг Export.csv, инициализация справочников
│   ├── referenceLib.py             # CRUD-операции со справочниками и связями
│   ├── dataLib.py                  # CRUD-операции с рынками (заглушки)
│   ├── userLib.py                  # CRUD-операции с пользователями
│   ├── reviewLib.py                # CRUD-операции с отзывами
│   └── requiredFiles.py            # Константы категорий и список файлов
├── UI/                             # Слой интерфейса пользователя
│   ├── uiLib.py                    # Функции вывода и ввода в консоль
│   ├── column_helper.py            # Словари перевода названий колонок и описания типов
│   └── comparison_helper.py        # Константы знаков сравнения для фильтрации
├── files/                          # CSV-файлы (справочники, связи, данные)
├── документация/                   # Диаграммы и пользовательские истории
├── .gitignore                      # Исключения Git
├── README.md                       # Документация
├── CONTRIBUTING.md                 # Руководство разработчика
├── requirements.txt                # Зависимости проекта
└── Export.csv                      # Исходный датасет (не включён)
```

## Запуск

```bash
python App.py
```

Для работы необходим файл `Export.csv` в корневой директории проекта.

## Архитектура

```
App.py
 │
 ├── UI/
 │    ├── uiLib.py                    — приветствие, справка, ввод фильтра, вывод данных
 │    ├── column_helper.py            — COLUMNS (перевод), COLUMNS_INFO (тип и имя колонок)
 │    └── comparison_helper.py        — COMPARISON_SIGNS (знаки сравнения для фильтров)
 │
 ├── BusinessLogic/
 │    ├── workflowLib.py            — оркестрация, командный цикл, вызов UI
 │    ├── commandHandler.py         — обработчики команд (ввод + бизнес-логика)
 │    ├── marketList.py             — бизнес-логика списка рынков
 │    ├── processFilter.py          — обработка фильтрации
 │    └── geoLib.py                 — геоданные и расчёт дистанций
 │
 └── DAL/
      ├── fileLib.py                — парсинг CSV, инициализация, чтение данных
      ├── referenceLib.py           — CRUD справочников и связей
      ├── dataLib.py                — CRUD рынков (заглушки)
      ├── userLib.py                — CRUD пользователей
      ├── reviewLib.py              — CRUD отзывов
      └── requiredFiles.py          — константы
```

Зависимости: `App.py` → `BusinessLogic` + `UI` → `DAL`

```
workflowLib (BL) → commandHandler (BL) → marketList (BL) → fileLib (DAL)  ✓
workflowLib (BL) → uiLib (UI)                                                  ✓
commandHandler (BL) → только marketList (BL)                                   ✓
```

## Модули

### App.py

Точка входа. Содержит:
- `main()` — основная функция запуска
- `user_lib_testing()` — проверка наличия пользователей, создание тестовых при необходимости
- `testing()` — заглушка для тестирования (закомментирована в main)

Порядок выполнения `main()`:
1. `directory_creation()` — создаёт папку `files/`
2. `file_creation()` — проверка и инициализация CSV-файлов
3. `user_lib_testing()` — тестирование CRUD пользователей
4. Цикл команд: вывод приветствия, чтение и обработка команд с отслеживанием сессии (user)

### BusinessLogic/workflowLib.py

Оркестрация рабочего процесса, обработка пользовательских команд и вывод в консоль.

| Функция | Описание |
|---------|----------|
| `directory_creation()` | Создаёт папку `files/` для хранения CSV-файлов |
| `file_creation()` | Проверяет файлы, при необходимости инициализирует справочники, создаёт MARKET_INFO.csv, USER_INFO.csv, Reference_Base.csv, REVIEWS.csv |
| `get_command(user)` | Считывает команду пользователя из stdin (с приветствием для авторизованных) |
| `proceed_command(command, user)` | Обрабатывает команду (help/list/list_all/order/show/filter/register/login/logout/review/update_user/exit) |

Поддерживаемые команды:
- `help` — справка
- `list_all` — все рынки
- `list` — список с пагинацией
- `order` — сортировка по колонке
- `show` — данные одного рынка по Id (с просмотром отзывов)
- `filter` — фильтрация рынков по колонке (включая расстояние)
- `register` — регистрация пользователя (с запросом координат)
- `login` — авторизация пользователя
- `logout` — выход из системы
- `review` — добавление отзыва на рынок
- `update_user` — обновление данных пользователя
- `exit` — выход

### BusinessLogic/commandHandler.py

Обработчики команд. Содержат ввод данных от пользователя и бизнес-логику.

| Функция | Возвращает | Описание |
|---------|------------|----------|
| `command_help()` | `True` | Подтверждение продолжения работы |
| `command_list_all()` | `(True, markets)` | Кортеж (статус, все рынки) |
| `command_list()` | `(True, markets, start, step)` | Кортеж (статус, рынки с нумерацией, старт, шаг) |
| `command_order(column, order)` | `(True, markets, col, order)` | Сортировка (column/order опциональны) |
| `command_show()` | `(True, market_info)` или `(True, None)` | Данные рынка, ошибка ID или неверный ввод |
| `register_user()` | `(True, user)` или `(True, None)` | Регистрация (с запросом координат) |
| `login_user(user)` | `(True, user)` или `(True, None)` | Авторизация пользователя |
| `logout_user(user)` | `(True, None)` | Выход из системы |
| `add_review(user)` | `(True, user)` | Добавление отзыва на рынок |
| `show_filtered(user)` | `(True, user)` | Фильтрация (требуется авторизация) |
| `update_user(user)` | `(True, user)` | Обновление данных пользователя |
| `command_exit()` | `False` | Сигнал завершения работы |

### BusinessLogic/processFilter.py

Модуль обработки фильтрации рынков. Для текстовых колонок — поиск подстроки. Для числовых — сравнение с оператором.

| Функция | Описание |
|---------|----------|
| `process(market_list, column, filter_value)` | Фильтрует рынки: text → подстрока, numeric → сравнение (>, <, >=, <=, =) |

### BusinessLogic/geoLib.py

Библиотека для работы с геоданными и расчёта дистанций.

| Функция | Описание |
|---------|----------|
| `haversine(lat1, lon1, lat2, lon2)` | Расчёт расстояния между двумя точками (формула Хаверсина), результат в км |
| `get_distance(user, market_base)` | Добавляет поле `distance` (км) в каждый рынок относительно пользователя |

Поля `latitude` и `longitude` в USER_INFO.csv хранят координаты пользователя (строки).

### BusinessLogic/marketList.py

Бизнес-логика для работы со списком рынков.

| Функция | Описание |
|---------|----------|
| `get_all_markets(mode)` | Получает данные о рынках (mode='uid' — ключ market_id, mode='num' — ключ порядковый номер) |
| `get_all_markets_ordered_by_column(col, order, user)` | Сортировка по колонке (1-9), user обязателен для distance |
| `get_all_markets_filtered_by_column(col, filter, user)` | Фильтрация по колонке с критерием, user для distance |
| `prepare_ordered_list(markets)` | Переиндексация dict с 1 для пагинации |
| `get_market_by_id(market_id)` | Получение подробных данных рынка: basic_info, media_info, bank_info, grocery_info |

### UI/uiLib.py

Функции вывода и ввода в консоль (интерфейс пользователя).

| Функция | Описание |
|---------|----------|
| `print_welcome()` | Выводит приветственное сообщение |
| `print_help()` | Выводит список доступных команд |
| `print_table_header()` | Выводит шапку таблицы (русские названия колонок) |
| `print_header_numbers()` | Выводит нумерацию колонок для сортировки/фильтрации (1-9, включая расстояние) |
| `print_list(markets, start_pos, step, column_name)` | Выводит таблицу с пагинацией и опциональной сортировкой |
| `print_exit()` | Выводит сообщение о завершении работы |
| `print_detailed_market_info(market_info)` | Выводит подробную информацию о рынке |
| `print_market_reviews(reviews, average_score)` | Выводит список отзывов о рынке и среднюю оценку |
| `print_comparison_rules()` | Выводит инструкцию по знакам сравнения для фильтрации |
| `request_filter()` | Запрашивает у пользователя критерий фильтрации (колонка + значение) |
| `get_user_coordinates_manually()` | Ручной ввод координат (широта, долгота) с валидацией диапазонов |
| `request_user_updates(user)` | Интерфейс обновления данных пользователя (username, имя, фамилия, координаты) |

### UI/column_helper.py

Словари для перевода названий колонок и описания типов.

| Константа | Описание |
|-----------|----------|
| `COLUMNS` | `{англ_название: русское_название}` для шапки таблицы |
| `COLUMNS_INFO` | `{номер: {name, type}}` для маппинга номеров колонок |
| `COLUMNS_INFO_REVERSED` | `{имя_колонки: номер}` — обратный маппинг |
| `COLUMN_TO_SHOW` | Список имён колонок для отображения в таблице |

| Ключ COLUMNS | Значение |
|------|----------|
| `number` | Номер |
| `market_id` | ID |
| `city` | город |
| `county` | графство |
| `state` | штат |
| `marketname` | название рынка |
| `zip` | п. индекс |
| `score` | ср. оценка |
| `distance` | расстояние (км) |

### UI/comparison_helper.py

Константы знаков сравнения для фильтрации числовых колонок.

| Константа | Значения |
|-----------|----------|
| `COMPARISON_SIGNS` | `['>', '<', '>=', '<=', '=']` |

### DAL/requiredFiles.py

Модуль констант. Содержит множества столбцов CSV-датасета, сгруппированные по категориям, а также список файлов для проверки:

| Константа | Описание |
|-----------|----------|
| `MARKET_INFO` | Столбцы: MarketName, street, zip |
| `TIMESHEET_INFO` | Столбцы: Season1-4 Date/Time |
| `COORDINATES` | Столбцы: LON, LAT |
| `MEDIA` | Website, Facebook, Twitter, Youtube, OtherMedia |
| `LOCATION` | city, County, State |
| `BANKING_INFO` | Credit, WIC, WICcash, SFMNP, SNAP |
| `GROCERY_TYPES` | Organic, Vegetables, Honey, Meat и др. (29 типов) |
| `FILES_TO_CHECK` | Множество имён CSV-файлов для проверки наличия перед работой |

### DAL/dataLib.py

CRUD-операции с фермерскими рынками.

| Функция | Описание |
|---------|----------|
| `create_market()` | Заглушка (в разработке) |
| `update_market(data)` | Обновляет данные рынка в MARKET_INFO.csv по market_id |
| `delete_market()` | Заглушка (в разработке) |

### DAL/referenceLib.py

CRUD-операции со справочниками и связями.

| Функция | Описание |
|---------|----------|
| `create_reference(name)` | Создаёт CSV-файл с заголовками Id, Name |
| `get_reference_with_name_as_key(name, type)` | Читает справочник: Common → {Name: Id}, Connection → {market_id: [ref_id, status]} |
| `get_reference_with_uid_as_key(name, type)` | Читает справочник: Common → {Id: Name}, Connection → {market_id: [ref_id, status]} |
| `create_reference_entry(name, data)` | Добавляет запись [UUID, Name] (автосоздание файла) |
| `read_reference_entry(name, uid, name)` | Ищет запись по UUID или имени, возвращает (Id, Name) |
| `update_reference_entry(name, data)` | Обновляет запись по ключу Id |
| `create_connection_reference(name)` | Создаёт CSV-файл связей |
| `create_connection_entry(name, mkt, ref, status)` | Добавляет связь (автосоздание файла) |
| `create_connection_entry_by_list(name, list)` | Батчевая запись списка связей |
| `read_connection_entry(name, mkt, ref)` | Ищет статус связи по market_id и reference_id |
| `get_all_connections_by_market_id(name, mkt_id)` | Все связи для рынка → {market_id: {ref_id: status}} |

### DAL/fileLib.py

Инициализация справочников, парсинг Export.csv, проверка файлов, создание CSV.

| Функция | Описание |
|---------|----------|
| `prepare_ref()` | Инициализирует справочники MEDIA, GROCERY_TYPES, BANKING_INFO |
| `read_csv()` | Читает Export.csv, создаёт связи, возвращает dict {FMID: {атрибуты}} |
| `file_status_check()` | Проверяет наличие CSV-файлов из FILES_TO_CHECK |
| `create_market_base(data)` | Создаёт MARKET_INFO.csv из словаря market_info |
| `get_raw_markets_from_file()` | Читает MARKET_INFO.csv, возвращает dict {market_id: {атрибуты}} |
| `create_user_base()` | Создаёт USER_INFO.csv |
| `create_review_base()` | Создаёт REVIEWS.csv |
| `create_reference_base()` | Создаёт Reference_Base.csv со списком всех справочников |

### DAL/userLib.py

CRUD-операции с пользователями через CSV-файл files/USER_INFO.csv.

| Элемент | Описание |
|---------|----------|
| `field_names` | Столбцы CSV: Id, user_name, password, firstname, lastname, latitude, longitude |
| `DEFAULT_USER` | Значения по умолчанию для нового пользователя |
| `create_user(user)` | Создаёт пользователя, возвращает UUID |
| `read_user(user_id)` | Читает пользователя по Id, возвращает dict |
| `get_user(pattern, mode)` | Читает по username (mode='username') или uid (mode='uid') |
| `update_user(user)` | Обновляет данные пользователя по Id |
| `delete_user(user_id)` | Удаляет пользователя по Id |

### DAL/reviewLib.py

CRUD-операции с отзывами о фермерских рынках через CSV-файл files/REVIEWS.csv.

| Функция | Описание |
|---------|----------|
| `create_review(review)` | Добавляет отзыв в файл REVIEWS.csv |
| `get_review_by_market_id(market_id)` | Читает отзывы для указанного рынка, возвращает list |
| `calculate_score(market_id)` | Рассчитывает среднюю оценку и обновляет MARKET_INFO.csv |

Структура CSV REVIEWS.csv:
- `Id` — UUID отзыва
- `review_date` — дата и время создания
- `user_id` — ID пользователя
- `market_id` — ID рынка
- `review_text` — текст отзыва
- `score` — оценка от 1 до 5

## Схема данных

```
App.py
 ├─ testing()                        → тестирование новых функций
 ├─ directory_creation()             → files/
 ├─ file_creation()                  → CSV-файлы (MARKET_INFO, USER_INFO, Reference_Base, REVIEWS)
 ├─ user_lib_testing()               → DAL/userLib (CRUD) → files/USER_INFO.csv
 ├─ print_welcome()                  → UI/uiLib
 └─ цикл команд (с user = None):
         │
         ├─ get_command()            → BusinessLogic/workflowLib
         └─ proceed_command(cmd, user) → BusinessLogic/workflowLib
                 │
                 ├─ 'help'     → commandHandler.command_help() → True
                 │                 → uiLib.print_help()
                 │
                 ├─ 'list_all' → commandHandler.command_list_all() → (True, markets)
                 │                 → marketList.get_all_markets('num')
                 │                 → uiLib.print_list(markets)
                 │
                 ├─ 'list'     → commandHandler.command_list() → (True, markets, start, step)
                 │                 → marketList.get_all_markets('num')
                 │                 → uiLib.print_list(markets, start, step)
                 │
                 ├─ 'order'    → commandHandler.command_order() → (True, markets, col, order)
                 │                 → marketList.get_all_markets_ordered_by_column()
                 │                 → uiLib.print_list(markets, col_name)
                 │
                 ├─ 'show'     → commandHandler.command_show() → (True, market_info)
                 │                 → marketList.get_market_by_id(market_id)
                 │                 → (опционально) get_review_by_market_id() → print_market_reviews()
                 │
                 ├─ 'filter'   → commandHandler.show_filtered() → (True, markets, col)
                 │                 → marketList.get_all_markets_filtered_by_column()
                 │
                 ├─ 'register' → commandHandler.register_user() → (True, user)
                 │                 → uiLib.get_user_coordinates_manually()
                 │
                 ├─ 'login'    → commandHandler.login_user(user) → (True, user)
                 │
                 ├─ 'logout'   → commandHandler.logout_user(user) → (True, None)
                 │
                 ├─ 'review'   → commandHandler.add_review(user) → (True, user)
                 │                 → reviewLib.create_review(review)
                 │
                 ├─ 'update_user' → commandHandler.update_user(user) → None (заглушка)
                 │
                 └─ 'exit'     → commandHandler.command_exit() → False
                                   → uiLib.print_exit()

 file_creation()
         │
         ├─ file_status_check()     ← FILES_TO_CHECK
         ├─ prepare_ref()           → MEDIA.csv, GROCERY_TYPES.csv, BANKING_INFO.csv
         ├─ create_market_base()    → MARKET_INFO.csv
         ├─ create_user_base()      → USER_INFO.csv
         ├─ create_reference_base() → Reference_Base.csv
         └─ create_review_base()    → REVIEWS.csv
```

## Требования

- Python 3.x
- Стандартная библиотека: `csv`, `uuid`, `os`, `getpass`, `statistics`

## Установка зависимостей

```bash
pip install -r requirements.txt
```

| Пакет | Версия | Назначение |
|-------|--------|------------|
| bcrypt | ≥ 4.0 | Хеширование паролей пользователей |

## Дополнительно

- [CONTRIBUTING.md](CONTRIBUTING.md) — руководство разработчика (добавление команд, колонок, справочников)
