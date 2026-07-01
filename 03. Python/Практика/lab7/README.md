# Лабораторная работа 7 — Управление данными о фермерских рынках

## Описание

Приложение для парсинга CSV-датасета фермерских рынков (FMSS/Export.csv), создания справочников и связывания данных через промежуточные CSV-файлы.

## Структура проекта

```
lab7/
├── App.py          # Точка входа приложения
├── dataLib.py      # CRUD-операции со справочниками и связями
├── fileLib.py      # Парсинг Export.csv, инициализация справочников
├── userLib.py      # Управление пользователями (в разработке)
├── README.md       # Документация
└── Export.csv      # Исходный датасет (не включён)
```

## Запуск

```bash
python App.py
```

Для работы необходим файл `Export.csv` в текущей директории.

## Модули

### App.py

Точка входа. `testing()` выполняет полный цикл:
1. Инициализирует справочники (MEDIA, GROCERY_TYPES, BANKING_INFO)
2. Читает Export.csv и создаёт связи рынков со справочниками
3. Создаёт итоговый файл MARKET_INFO.csv

### dataLib.py

CRUD-операции со справочниками и связями через CSV-файлы.

| Функция | Описание |
|---------|----------|
| `create_reference(name)` | Создаёт CSV-файл с заголовками Id, Name |
| `create_reference_entry(name, data)` | Добавляет запись [UUID, Name] (файл создаётся автоматически) |
| `read_reference_entry(name, uid, name)` | Ищет запись по UUID или имени, возвращает (Id, Name) |
| `update_reference_entry(name, data)` | Обновляет запись по ключу Id |
| `create_connection_reference(name)` | Создаёт CSV-файл связей (market_id, reference_id, status) |
| `create_connection_entry(name, mkt, ref, status)` | Добавляет связь (файл создаётся автоматически) |
| `read_connection_entry(name, mkt, ref)` | Ищет статус связи по market_id и reference_id |
| `create_market_base(data)` | Создаёт MARKET_INFO.csv из словаря market_info |
| `create_market()` | Заглушка (в разработке) |
| `update_market()` | Заглушка (в разработке) |
| `delete_market()` | Заглушка (в разработке) |

### fileLib.py

Парсинг Export.csv и подготовка справочников.

| Элемент | Описание |
|---------|----------|
| `prepare_ref()` | Инициализирует справочники MEDIA, GROCERY_TYPES, BANKING_INFO |
| `read_csv()` | Читает Export.csv, создаёт связи, возвращает dict {FMID: {атрибуты}} |
| `ref_list` | Список справочников для инициализации |
| `MARKET_INFO` | Столбцы: MarketName, street, zip |
| `COORDINATES` | Столбцы: LON, LAT |
| `TIMESHEET_INFO` | Столбцы: Season1-4 Date/Time |
| `MEDIA` | Website, Facebook, Twitter, Youtube, OtherMedia |
| `LOCATION` | city, County, State |
| `BANKING_INFO` | Credit, WIC, WICcash, SFMNP, SNAP |
| `GROCERY_TYPES` | Organic, Vegetables, Honey, Meat и др. (29 типов) |

### userLib.py

Управление пользователями (все функции — заглушки).

| Функция | Описание |
|---------|----------|
| `create_user()` | Создание пользователя |
| `update_user()` | Обновление данных |
| `delete_user()` | Удаление пользователя |

## Схема данных

```
Export.csv
    │
    ├── read_csv() → market_info dict
    │       │
    │       ├── MarketXSocialMedia.csv   (market ↔ соцсети)
    │       ├── MarketXGrocery.csv       (market ↔ товары)
    │       ├── MarketXBankingInfo.csv   (market ↔ оплата)
    │       ├── CITY.csv                 (market ↔ город)
    │       ├── COUNTY.csv               (market ↔ округ)
    │       └── STATE.csv                (market ↔ штат)
    │
    └── create_market_base()
            └── MARKET_INFO.csv (итоговый файл)
```

## Требования

- Python 3.x
- Стандартная библиотека: `csv`, `uuid`, `os`
