# Лабораторная работа 7 — Управление данными о фермерских рынках

## Описание

Приложение для парсинга CSV-датасета фермерских рынков (Export.csv), создания справочников и связывания данных через промежуточные CSV-файлы. Построено по трёхуровневой архитектуре: UI → BusinessLogic → DAL.

## Структура проекта

```
lab7/
├── App.py                          # Точка входа приложения
├── BusinessLogic/                  # Слой бизнес-логики
│   ├── workflowLib.py              # Оркестрация процесса и обработка команд
│   ├── commandHandler.py           # Обработчики команд (help, list, list_all, order, exit)
│   └── marketList.py               # Бизнес-логика получения списка рынков
├── DAL/                            # Слой доступа к данным (Data Access Layer)
│   ├── fileLib.py                  # Парсинг Export.csv, инициализация справочников
│   ├── referenceLib.py             # CRUD-операции со справочниками и связями
│   ├── dataLib.py                  # CRUD-операции с рынками (заглушки)
│   ├── userLib.py                  # CRUD-операции с пользователями
│   └── requiredFiles.py            # Константы категорий и список файлов
├── UI/                             # Слой интерфейса пользователя
│   ├── uiLib.py                    # Функции вывода в консоль
│   └── columnToRu.py               # Словарь перевода названий колонок на русский
├── files/                          # CSV-файлы (справочники, связи, данные)
├── документация/                   # Диаграммы и пользовательские истории
├── .gitignore                      # Исключения Git
├── README.md                       # Документация
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
 ├── UI/uiLib.py                    — приветствие, справка, список рынков, выход
 │
 ├── BusinessLogic/
 │    ├── workflowLib.py            — оркестрация, командный цикл, вызов UI
 │    ├── commandHandler.py         — обработчики команд (только данные, без UI)
 │    └── marketList.py             — бизнес-логика списка рынков
 │
 └── DAL/
      ├── fileLib.py                — парсинг CSV, инициализация, чтение данных
      ├── referenceLib.py           — CRUD справочников и связей
      ├── dataLib.py                — CRUD рынков (заглушки)
      ├── userLib.py                — CRUD пользователей
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
- `user_lib_testing()` — демонстрация CRUD-операций с пользователями (создание, чтение, обновление, удаление)
- `testing()` — заглушка для тестирования

Порядок выполнения `main()`:
1. `directory_creation()` — создаёт папку `files/`
2. `user_lib_testing()` — тестирование CRUD пользователей
3. `file_creation()` — проверка и инициализация CSV-файлов
4. Цикл команд: вывод приветствия, чтение и обработка команд

### BusinessLogic/workflowLib.py

Оркестрация рабочего процесса, обработка пользовательских команд и вывод в консоль.

| Функция | Описание |
|---------|----------|
| `directory_creation()` | Создаёт папку `files/` для хранения CSV-файлов |
| `file_creation()` | Проверяет файлы, при необходимости инициализирует справочники, создаёт MARKET_INFO.csv, USER_INFO.csv, Reference_Base.csv |
| `get_command()` | Считывает команду пользователя из stdin |
| `proceed_command(command)` | Обрабатывает команду (help/list/list_all/order/show/exit) |

Поддерживаемые команды:
- `help` — справка
- `list_all` — все рынки
- `list` — список с пагинацией
- `order` — сортировка по колонке
- `show` — данные одного рынка по Id
- `exit` — выход

### BusinessLogic/commandHandler.py

Обработчики команд. Возвращают данные для вывода, не зависят от UI.

| Функция | Возвращает | Описание |
|---------|------------|----------|
| `command_help()` | `True` | Подтверждение продолжения работы |
| `command_list_all()` | `(True, markets)` | Кортеж (статус, все рынки) |
| `command_list()` | `(True, markets, start, step)` | Кортеж (статус, рынки с нумерацией, старт, шаг) |
| `command_order()` | `(True, markets, col, order)` | Кортеж (статус, рынки, колонка, порядок) |
| `command_show(market_id)` | `(True, market_info)` или `True` | Данные рынка или ошибка |
| `command_exit()` | `False` | Сигнал завершения работы |

### BusinessLogic/marketList.py

Бизнес-логика для работы со списком рынков.

| Функция | Описание |
|---------|----------|
| `get_all_markets()` | Получает данные о рынках (ключ — market_id), резолвит ID → имена |
| `get_all_markets_ordered_by_num()` | То же, но ключ — порядковый номер (для пагинации) |
| `get_all_markets_ordered_by_column(col, order)` | Сортировка по колонке (1-7), order: 'a'/ 'd' |
| `prepare_ordered_list(markets)` | Переиндексация dict с 1 для пагинации |
| `get_market_by_id(market_id)` | Получение подробных данных рынка: basic_info, media_info, bank_info, grocery_info |

### UI/uiLib.py

Функции вывода текста в консоль (интерфейс пользователя).

| Функция | Описание |
|---------|----------|
| `print_welcome()` | Выводит приветственное сообщение |
| `print_help()` | Выводит список доступных команд |
| `print_table_header()` | Выводит шапку таблицы (русские названия колонок) |
| `print_list_all(markets)` | Выводит таблицу со списком всех рынков |
| `print_list(markets, start_pos, step, column_name)` | Выводит таблицу с пагинацией и опциональной сортировкой |
| `print_ordered_instruction()` | Выводит инструкцию по выбору колонки для сортировки |
| `print_exit()` | Выводит сообщение о завершении работы |
| `print_detailed_market_info(market_info)` | Выводит подробную информацию о рынке (адрес, расписание, соцсети, оплата, товары) |

### UI/columnToRu.py

Словарь для перевода названий колонок с английского на русский язык.

| Ключ | Значение |
|------|----------|
| `number` | Номер |
| `market_id` | ID |
| `city` | город |
| `county` | графство |
| `state` | штат |
| `marketname` | название рынка |
| `zip` | п. индекс |

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

CRUD-операции с фермерскими рынками (все функции — заглушки в разработке).

| Функция | Описание |
|---------|----------|
| `create_market()` | Заглушка (в разработке) |
| `update_market()` | Заглушка (в разработке) |
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
| `humanize_reference(ref)` | Заглушка для преобразования ID → имя |

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
| `create_reference_base()` | Создаёт Reference_Base.csv со списком всех справочников |

### DAL/userLib.py

CRUD-операции с пользователями через CSV-файл files/USER_INFO.csv.

| Элемент | Описание |
|---------|----------|
| `field_names` | Столбцы CSV: Id, user_name, password, firstname, lastname, location |
| `DEFAULT_USER` | Значения по умолчанию для нового пользователя |
| `create_user(user)` | Создаёт пользователя, возвращает UUID |
| `read_user(user_id)` | Читает пользователя по Id, возвращает dict |
| `update_user(user)` | Обновляет данные пользователя по Id |
| `delete_user(user_id)` | Удаляет пользователя по Id |

## Схема данных

```
App.py
 ├─ testing()                        → тестирование новых функций
 ├─ directory_creation()             → files/
 ├─ user_lib_testing()               → DAL/userLib (CRUD) → files/USER_INFO.csv
 ├─ print_welcome()                  → UI/uiLib
 └─ цикл команд:
         │
         ├─ get_command()            → BusinessLogic/workflowLib
         └─ proceed_command()        → BusinessLogic/workflowLib
                 │
                 ├─ 'help'     → commandHandler.command_help() → True
                 │                 → uiLib.print_help()
                 │
                 ├─ 'list_all' → commandHandler.command_list_all() → (True, markets)
                 │                 → marketList.get_all_markets()
                 │                 → uiLib.print_list_all(markets)
                 │
                 ├─ 'list'     → commandHandler.command_list() → (True, markets, start, step)
                 │                 → marketList.get_all_markets_ordered_by_num()
                 │                 → uiLib.print_list(markets, start, step)
                 │
                 ├─ 'order'    → commandHandler.command_order() → (True, markets, col, order)
                 │                 → marketList.get_all_markets_ordered_by_column()
                 │                 → uiLib.print_list(markets, col_name)
                 │
                 ├─ 'show'     → commandHandler.command_show(market_id) → None/True
                 │                 → marketList.get_market_by_id(market_id)
                 │
                 └─ 'exit'     → commandHandler.command_exit() → False
                                   → uiLib.print_exit()

 file_creation()
         │
         ├─ file_status_check()     ← FILES_TO_CHECK
         ├─ prepare_ref()           → MEDIA.csv, GROCERY_TYPES.csv, BANKING_INFO.csv
         ├─ create_market_base()    → MARKET_INFO.csv
         ├─ create_user_base()      → USER_INFO.csv
         └─ create_reference_base() → Reference_Base.csv
```

## Требования

- Python 3.x
- Стандартная библиотека: `csv`, `uuid`, `os`

## Дополнительно

- [CONTRIBUTING.md](CONTRIBUTING.md) — руководство разработчика (добавление команд, колонок, справочников)
