# Лабораторная работа 7 — Управление данными о фермерских рынках

## Описание

Приложение для парсинга CSV-датасета фермерских рынков (Export.csv), создания справочников и связывания данных через промежуточные CSV-файлы. Построено по трёхуровневой архитектуре: UI → BusinessLogic → DAL.

## Структура проекта

```
lab7/
├── App.py                          # Точка входа приложения
├── BusinessLogic/                  # Слой бизнес-логики
│   ├── workflowLib.py              # Оркестрация процесса и обработка команд
│   ├── commandHandler.py           # Обработчики команд (help, list, exit)
│   └── marketList.py               # Бизнес-логика получения списка рынков
├── DAL/                            # Слой доступа к данным (Data Access Layer)
│   ├── fileLib.py                  # Парсинг Export.csv, инициализация справочников
│   ├── referenceLib.py             # CRUD-операции со справочниками и связями
│   ├── dataLib.py                  # CRUD-операции с рынками (заглушки)
│   ├── userLib.py                  # CRUD-операции с пользователями
│   └── requiredFiles.py            # Константы категорий и список файлов
├── UI/                             # Слой интерфейса пользователя
│   └── uiLib.py                    # Функции вывода в консоль
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
 │    ├── workflowLib.py            — оркестрация, командный цикл
 │    ├── commandHandler.py         — обработчики команд
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

## Модули

### App.py

Точка входа. `main()` выполняет:
1. `directory_creation()` — создаёт папку `files/` для CSV-файлов
2. `user_lib_testing()` — демонстрация CRUD-операций с пользователями
3. `file_creation()` — проверка файлов и создание данных
4. Цикл команд: вывод приветствия, чтение и обработка команд пользователя

### BusinessLogic/workflowLib.py

Оркестрация рабочего процесса и обработка пользовательских команд.

| Функция | Описание |
|---------|----------|
| `directory_creation()` | Создаёт папку `files/` для хранения CSV-файлов |
| `file_creation()` | Проверяет файлы через `file_status_check()`, при необходимости инициализирует справочники, создаёт MARKET_INFO.csv и USER_INFO.csv |
| `get_command()` | Считывает команду пользователя из stdin |
| `proceed_command(command)` | Обрабатывает команду (help/list/exit), возвращает True для продолжения, False для выхода |

### BusinessLogic/commandHandler.py

Обработчики команд пользователя.

| Функция | Описание |
|---------|----------|
| `command_help()` | Выводит список доступных команд через uiLib |
| `command_list()` | Получает список рынков через marketList и выводит через uiLib |
| `command_exit()` | Выводит сообщение о завершении, возвращает False |

### BusinessLogic/marketList.py

Бизнес-логика для работы со списком рынков.

| Функция | Описание |
|---------|----------|
| `get_all_markets()` | Получает данные о рынках через fileLib.get_markets_base() |

### UI/uiLib.py

Функции вывода текста в консоль (интерфейс пользователя).

| Функция | Описание |
|---------|----------|
| `print_welcome()` | Выводит приветственное сообщение |
| `print_help()` | Выводит список доступных команд |
| `print_list(markets)` | Выводит таблицу со списком всех рынков |
| `print_exit()` | Выводит сообщение о завершении работы |

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

CRUD-операции со справочниками (справочные CSV-файлы) и связями между рынками и справочниками.

| Функция | Описание |
|---------|----------|
| `create_reference(name)` | Создаёт CSV-файл с заголовками Id, Name |
| `get_reference(name, type)` | Читает справочник в dict {Name: Id} или {market_id: [ref_id, status]} |
| `create_reference_entry(name, data)` | Добавляет запись [UUID, Name] (файл создаётся автоматически) |
| `read_reference_entry(name, uid, name)` | Ищет запись по UUID или имени, возвращает (Id, Name) |
| `update_reference_entry(name, data)` | Обновляет запись по ключу Id |
| `create_connection_reference(name)` | Создаёт CSV-файл связей (market_id, reference_id, status) |
| `create_connection_entry(name, mkt, ref, status)` | Добавляет связь (файл создаётся автоматически) |
| `create_connection_entry_by_list(name, list)` | Батчевая запись списка связей в CSV-файл |
| `read_connection_entry(name, mkt, ref)` | Ищет статус связи по market_id и reference_id |

### DAL/fileLib.py

Инициализация справочников, парсинг Export.csv, проверка наличия файлов, создание MARKET_INFO.csv и USER_INFO.csv.

| Функция | Описание |
|---------|----------|
| `prepare_ref()` | Инициализирует справочники MEDIA, GROCERY_TYPES, BANKING_INFO |
| `read_csv()` | Читает Export.csv, создаёт связи, возвращает dict {FMID: {атрибуты}} |
| `file_status_check()` | Проверяет наличие CSV-файлов из `FILES_TO_CHECK`, возвращает True при необходимости пересоздания |
| `create_market_base(data)` | Создаёт MARKET_INFO.csv из словаря market_info |
| `get_markets_base()` | Читает MARKET_INFO.csv и возвращает данные о рынках |
| `create_user_base()` | Создаёт USER_INFO.csv с заголовками: Id, user_name, password, firstname, lastname, location |

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
 ├─ directory_creation()           → files/
 ├─ user_lib_testing()             → DAL/userLib (CRUD) → files/USER_INFO.csv
 ├─ print_welcome()                → UI/uiLib
 └─ цикл команд:
         │
         ├─ get_command()          → BusinessLogic/workflowLib
         └─ proceed_command()      → BusinessLogic/workflowLib
                 │
                 ├─ 'help'  → commandHandler.command_help()  → UI/uiLib.print_help()
                 ├─ 'list'  → commandHandler.command_list()
                 │              → marketList.get_all_markets()
                 │                  → DAL/fileLib.get_markets_base()
                 │              → UI/uiLib.print_list(markets)
                 └─ 'exit'  → commandHandler.command_exit()  → UI/uiLib.print_exit()

 file_creation()
         │
         ├─ DAL/fileLib.file_status_check()  ← DAL/requiredFiles.FILES_TO_CHECK
         │       │
         │       └─ (если файлы отсутствуют)
         │
         ▼
   DAL/requiredFiles.py (константы категорий)
             │
             ▼
   DAL/fileLib.py                DAL/referenceLib.py          DAL/dataLib.py
    ├─ prepare_ref()             ├─ create_reference()        ├─ create_market()     (заглушка)
    │   │                        ├─ get_reference()           ├─ update_market()     (заглушка)
    │   ├── MEDIA.csv            ├─ create_reference_entry()  └─ delete_market()     (заглушка)
    │   ├── GROCERY_TYPES.csv    ├─ read_reference_entry()
    │   └── BANKING_INFO.csv     ├─ update_reference_entry()
    │                            ├─ create_connection_reference()
    ├─ read_csv()                ├─ create_connection_entry()
    │   │ (кэширование +         ├─ create_connection_entry_by_list()
    │   │  батчевая запись)      └─ read_connection_entry()
    │   │
    │   ├── MarketXSocialMedia.csv   (market ↔ соцсети)
    │   ├── MarketXGrocery.csv       (market ↔ товары)
    │   ├── MarketXBankingInfo.csv   (market ↔ оплата)
    │   ├── CITY.csv                 (market ↔ город)
    │   ├── COUNTY.csv               (market ↔ округ)
    │   └── STATE.csv                (market ↔ штат)
    │
    ├─ file_status_check()
    │       └── (проверка наличия файлов из FILES_TO_CHECK)
    │
    ├─ create_market_base()
    │       └── MARKET_INFO.csv (итоговый файл)
    │
    ├─ get_markets_base()
    │       └── чтение MARKET_INFO.csv
    │
    └─ create_user_base()
            └── USER_INFO.csv (файл пользователей)

    Все CSV-файлы хранятся в папке files/
```

## Требования

- Python 3.x
- Стандартная библиотека: `csv`, `uuid`, `os`
