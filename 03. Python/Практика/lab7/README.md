# Лабораторная работа 7 — Управление данными о фермерских рынках

## Описание

Приложение для парсинга CSV-датасета фермерских рынков (Export.csv), создания справочников и связывания данных через промежуточные CSV-файлы.

## Структура проекта

```
lab7/
├── App.py              # Точка входа приложения
├── workfowLib.py       # Оркестрация рабочего процесса
├── requiredFiles.py    # Константы категорий и список файлов для проверки
├── referenceLib.py     # CRUD-операции со справочниками и связями
├── dataLib.py          # CRUD-операции с рынками (заглушки)
├── fileLib.py          # Инициализация справочников, парсинг Export.csv, проверка файлов
├── userLib.py          # CRUD-операции с пользователями
├── files/              # CSV-файлы (справочники, связи, данные)
├── README.md           # Документация
└── Export.csv          # Исходный датасет (не включён)
```

## Запуск

```bash
python App.py
```

Для работы необходим файл `Export.csv` в текущей директории.

## Модули

### App.py

Точка входа. `main()` выполняет:
1. `directory_creation()` — создаёт папку `files/` для CSV-файлов
2. `user_lib_testing()` — демонстрация CRUD-операций с пользователями
3. `file_creation()` — проверка файлов и создание данных

### workfowLib.py

Оркестрация рабочего процесса. Создание директории для файлов, проверка наличия файлов, инициализация справочников и парсинг данных.

| Функция | Описание |
|---------|----------|
| `directory_creation()` | Создаёт папку `files/` для хранения CSV-файлов |
| `file_creation()` | Проверяет файлы через `file_status_check()`, при необходимости инициализирует справочники, создаёт MARKET_INFO.csv и USER_INFO.csv |

### requiredFiles.py

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

### dataLib.py

CRUD-операции с фермерскими рынками (все функции — заглушки в разработке).

| Функция | Описание |
|---------|----------|
| `create_market()` | Заглушка (в разработке) |
| `update_market()` | Заглушка (в разработке) |
| `delete_market()` | Заглушка (в разработке) |

### referenceLib.py

CRUD-операции со справочниками (справочные CSV-файлы) и связями между рынками и справочниками.

| Функция | Описание |
|---------|----------|
| `create_reference(name)` | Создаёт CSV-файл с заголовками Id, Name |
| `create_reference_entry(name, data)` | Добавляет запись [UUID, Name] (файл создаётся автоматически) |
| `read_reference_entry(name, uid, name)` | Ищет запись по UUID или имени, возвращает (Id, Name) |
| `update_reference_entry(name, data)` | Обновляет запись по ключу Id |
| `create_connection_reference(name)` | Создаёт CSV-файл связей (market_id, reference_id, status) |
| `create_connection_entry(name, mkt, ref, status)` | Добавляет связь (файл создаётся автоматически) |
| `read_connection_entry(name, mkt, ref)` | Ищет статус связи по market_id и reference_id |

### fileLib.py

Инициализация справочников, парсинг Export.csv, проверка наличия файлов, создание MARKET_INFO.csv и USER_INFO.csv.

| Функция | Описание |
|---------|----------|
| `prepare_ref()` | Инициализирует справочники MEDIA, GROCERY_TYPES, BANKING_INFO |
| `read_csv()` | Читает Export.csv, создаёт связи, возвращает dict {FMID: {атрибуты}} |
| `file_status_check()` | Проверяет наличие CSV-файлов из `FILES_TO_CHECK`, возвращает True при необходимости пересоздания |
| `create_market_base(data)` | Создаёт MARKET_INFO.csv из словаря market_info |
| `create_user_base()` | Создаёт USER_INFO.csv с заголовками: Id, user_name, password, firstname, lastname, location |

### userLib.py

CRUD-операции с пользователями через CSV-файл USER_INFO.csv.

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
 ├─ directory_creation()  → files/
 ├─ user_lib_testing()    → userLib (CRUD) → files/USER_INFO.csv
 └─ file_creation()
         │
         ├─ fileLib.file_status_check()  ← requiredFiles.FILES_TO_CHECK
         │       │
         │       └─ (если файлы отсутствуют)
         │
         ▼
   requiredFiles.py (константы категорий)
             │
             ▼
   fileLib.py                    referenceLib.py              dataLib.py
    ├─ prepare_ref()             ├─ create_reference()        ├─ create_market()     (заглушка)
    │   │                        ├─ create_reference_entry()  ├─ update_market()     (заглушка)
    │   ├── MEDIA.csv            ├─ read_reference_entry()    └─ delete_market()     (заглушка)
    │   ├── GROCERY_TYPES.csv    ├─ update_reference_entry()
    │   └── BANKING_INFO.csv     ├─ create_connection_reference()
    │                            ├─ create_connection_entry()
    ├─ read_csv()                └─ read_connection_entry()
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
    └─ create_user_base()
            └── USER_INFO.csv (файл пользователей)

    Все CSV-файлы хранятся в папке files/
```

## Требования

- Python 3.x
- Стандартная библиотека: `csv`, `uuid`, `os`
