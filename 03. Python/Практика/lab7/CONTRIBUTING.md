# Руководство администратора и разработчика

## Развёртывание на клиентской машине

### Системные требования

- Python 3.10 или выше
- ОС: Windows, macOS, Linux
- ~50 МБ свободного места (включая данные)

### Пошаговая инструкция

1. **Установка Python**

   Скачайте Python 3.10+ с https://www.python.org/downloads/
   При установке отметьте галочку "Add Python to PATH".

2. **Клонирование репозитория**

   ```bash
   git clone <URL_репозитория>
   cd lab7
   ```

3. **Создание виртуального окружения**

   ```bash
   python -m venv .venv
   ```

4. **Активация окружения**

   ```bash
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1

   # Windows (CMD)
   .venv\Scripts\activate.bat

   # macOS/Linux
   source .venv/bin/activate
   ```

5. **Установка зависимостей**

   ```bash
   pip install -r requirements.txt
   ```

6. **Подготовка данных**

   Поместите файл `Export.csv` в корневую директорию проекта.

7. **Запуск**

   ```bash
   python App.py
   ```

### Автоматическая настройка

При первом запуске приложение автоматически:
- Создаёт SQLite-базу `database/base.db`
- Создаёт таблицы: MARKETS, USERS, REVIEWS
- Создаёт справочники: CITY, COUNTY, STATE, ZIP, STREET, MEDIA, GROCERY_TYPES, BANKING_INFO
- Создаёт связующие таблицы: MarketXSocialMedia, MarketXGrocery, MarketXBankingInfo
- Заполняет справочники значениями из CSV-констант
- Импортирует ~1700 рынков из `Export.csv`

### Первый запуск

1. Зарегистрируйтесь командой `register`
2. Укажите координаты для работы фильтра по расстоянию
3. Просматривайте рынки командой `list_all` или `list`

---

## Архитектура приложения

### Четырёхуровневая архитектура

```
┌─────────────────────────────────────────┐
│                  UI                      │
│  Вывод данных, ввод пользователя        │
│  (uiLib, column_helper, comparison)      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│            BusinessLogic                 │
│  Бизнес-логика, обработка команд        │
│  (workflowLib, commandHandler,           │
│   market_queries, processFilter, geoLib) │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│              models                      │
│  Сущности и коллекции (OOP)             │
│  (Market, User, Review, Reference,      │
│   MarketCollection)                      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│                DAL                       │
│  Доступ к данным (SQLite)               │
│  (datalib2, referencelib2, reviewlib2,  │
│   userlib2, filelib2, requiredFiles)    │
└─────────────────────────────────────────┘
```

### Хранение данных

Данные хранятся в SQLite-базе `database/base.db`. Справочники (CITY, COUNTY, STATE и др.) хранятся в отдельных таблицах с полями `id` (INTEGER PK) и `name` (TEXT UNIQUE). Связи между рынками и справочниками — в связующих таблицах с составным ключом `(market_id, reference_id)`.

### Потоки данных

**Просмотр рынков:**
```
user → get_command() → proceed_command('list') → command_list()
    → MarketCollection.from_db() → change_mode() → print_list()
```

**Фильтрация по расстоянию:**
```
user → proceed_command('filter') → show_filtered(user)
    → request_filter() → get_all_markets_filtered_by_column(col, filter, user)
    → geoLib.get_distance() → print_list()
```

**Добавление отзыва:**
```
user → proceed_command('review') → add_review(user)
    → command_show() → Review(user, market) → save_to_db()
    → market.calculate_score() → market.update()
```

---

## Добавление новой команды

### Шаг 1: Добавить обработчик в commandHandler.py

Создайте функцию-обработчик, которая возвращает данные для вывода:

```python
# BusinessLogic/commandHandler.py

def command_new_command():
    # Бизнес-логика (работа с данными)
    result = some_business_logic()
    return True, result  # (статус_работы, данные_для_UI)
```

### Шаг 2: Добавить маршрутизацию в workflowLib.py

Добавьте новую ветку в `match` внутри `proceed_command()`. Функция принимает `command` и `user`:

```python
# BusinessLogic/workflowLib.py

def proceed_command(command, user):
    is_run = True
    match command:
        # ... существующие команды ...
        case 'new_command':
            is_run, data = commandHandler.command_new_command()
            if data is None:
                print('Ошибка. Попробуйте ещё раз')
            else:
                uiLib.print_new_command(data)
        # ...
    return is_run, user
```

### Шаг 3: Добавить функцию вывода в uiLib.py

Создайте функцию для отображения результатов:

```python
# UI/uiLib.py

def print_new_command(data):
    print('======--------------------------------======')
    # Форматирование и вывод данных
    print('======--------------------------------======')
```

### Шаг 4: Обновить справку в uiLib.py

Добавьте описание новой команды в `print_help()`:

```python
def print_help():
    print('Доступные команды:')
    # ... существующие команды ...
    print('new_command - описание новой команды')
```

---

## Добавление нового справочника

### Шаг 1: Создать множество в requiredFiles.py

```python
# DAL/requiredFiles.py

NEW_REFERENCE = {'Value1', 'Value2', 'Value3'}
```

### Шаг 2: Добавить в REF_LIST в requiredFiles.py

```python
# DAL/requiredFiles.py

REF_LIST = {
    'required_refs': {
        # ... существующие справочники ...
        'NEW_REFERENCE': 'Common',
    },
    'values': {
        # ... существующие значения ...
        'NEW_REFERENCE': NEW_REFERENCE,
    }
}
```

### Шаг 3: Обработать в filelib2.py

Если справочник связан с рынками через CSV-колонку, добавьте обработку в `read_csv()`:

```python
# DAL/filelib2.py

def read_csv():
    # ... существующий код ...
    new_reference = Reference('NEW_REFERENCE')
    new_reference_dict = new_reference.get_all_with_names()
    NewXMarket = []

    for row in reader:
        # ... существующая обработка ...
        if key in requiredFiles.NEW_REFERENCE:
            reference_id = new_reference_dict[key]
            NewXMarket.append([current_id, reference_id, value])

    # После цикла — батчевая запись связи
    new_x_market = Reference('NewXMarket', 'Connection')
    new_x_market.add_many(NewXMarket)
```

---

## Добавление новой сущности

### Шаг 1: Создать модуль в models/entities/

Создайте файл `models/entities/new_entity.py`:

```python
# models/entities/new_entity.py

class NewEntity:
    """Сущность нового типа."""

    def __init__(self, id=None):
        self.id = id

    def save_to_db(self):
        """Сохраняет сущность в БД."""
        from DAL.new_entity_lib import create_new_entity
        create_new_entity(self)

    @classmethod
    def from_dict(cls, data):
        """Создаёт сущность из словаря (данные из БД)."""
        entity = cls(id=data['id'])
        # ... заполнение полей ...
        return entity

    def get_as_dict(self):
        """Конвертирует сущность в словарь."""
        return {'id': self.id}
```

### Шаг 2: Создать DAL-модуль

Создайте файл `DAL/new_entity_lib.py` с функциями CRUD:

```python
# DAL/new_entity_lib.py

import sqlite3
from config import DATABASE_PATH

def create_new_entity(entity):
    """Добавляет сущность в таблицу."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO NEW_ENTITY (...) VALUES (...)",
        (entity.field1, entity.field2)
    )
    conn.commit()
    conn.close()
```

### Шаг 3: Создать таблицу в requiredFiles.py

```python
# DAL/requiredFiles.py

def create_new_entity_table():
    """Создаёт таблицу NEW_ENTITY (если не существует)."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS NEW_ENTITY (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        field1 TEXT NOT NULL,
        field2 TEXT
    )''')
    conn.commit()
    conn.close()
```

### Шаг 4: Вызвать создание в workflowLib.py

```python
# BusinessLogic/workflowLib.py

def file_creation():
    # ... существующий код ...
    requiredFiles.create_new_entity_table()
```

### Шаг 5: Создать обработчик в commandHandler.py

```python
# BusinessLogic/commandHandler.py

def add_entity(user):
    """Добавление новой сущности."""
    if user is None:
        print('Требуется авторизация.')
        return True, user
    # ... создание и сохранение ...
    return True, user
```

### Шаг 6: Добавить команду в workflowLib.py

```python
# BusinessLogic/workflowLib.py

def proceed_command(command, user):
    match command:
        # ... существующие команды ...
        case 'new_entity':
            is_run, user = commandHandler.add_entity(user)
```

---

## Структура данных (SQLite)

### Справочники (Common)
```sql
CREATE TABLE CITY (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
```

### Связующие таблицы (Connection)
```sql
CREATE TABLE MarketXSocialMedia (
    market_id INTEGER NOT NULL,
    reference_id INTEGER NOT NULL,
    status TEXT,
    PRIMARY KEY (market_id, reference_id)
);
```

### MARKETS
```sql
CREATE TABLE MARKETS (
    id INTEGER PRIMARY KEY,
    marketname TEXT NOT NULL,
    street TEXT NOT NULL,
    city TEXT NOT NULL,
    county TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    longitude REAL,
    latitude REAL,
    season1date TEXT, season1time TEXT,
    season2date TEXT, season2time TEXT,
    season3date TEXT, season3time TEXT,
    season4date TEXT, season4time TEXT,
    score REAL
);
```

### USERS
```sql
CREATE TABLE USERS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    latitude REAL,
    longitude REAL
);
```

### REVIEWS
```sql
CREATE TABLE REVIEWS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_date TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    market_id INTEGER NOT NULL,
    review_text TEXT,
    score REAL
);
```

---

## Система сессий (авторизация)

Приложение поддерживает отслеживание текущего пользователя через объект `user` (экземпляр `User` или `None`):

- `user = None` — пользователь не авторизован
- `user = User(...)` — объект с данными пользователя

### Поток авторизации

1. **Регистрация** (`register`) — создаёт пользователя в USERS, возвращает `User`
2. **Вход** (`login`) — проверяет логин/пароль через bcrypt, возвращает `User` или `None`
3. **Выход** (`logout`) — сбрасывает `user` в `None`

### Передача user между функциями

Все функции обработки команд принимают и возвращают `user`:

```python
# commandHandler.py
def add_review(user):
    if user is None:
        print('Требуется авторизация.')
        return True, user
    # ... работа с user ...
    return True, user

# workflowLib.py
def proceed_command(command, user):
    match command:
        case 'review':
            is_run, user = commandHandler.add_review(user)
    return is_run, user
```

---

## Частые ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `TypeError: '<' not supported between NoneType` | Рынок без оценки при сортировке | None-рынки отделяются и идут в конец |
| `sqlite3.OperationalError: no such table` | Таблица не создана | Проверить requiredFiles.prepare_refs() |
| `ImportError: cannot import name` | Циклический импорт | Использовать lazy import внутри функции |
| `Invalid salt` при login | Пароль не хеширован | Проверить bcrypt при регистрации |
| `KeyError` в change_mode | Справочник не заполнен | Вызвать prepare_refs() перед импортом |

---

## Жизненный цикл приложения

### Развёртывание

1. Установить Python 3.10+, клонировать репозиторий, создать venv, установить зависимости
2. Поместить `Export.csv` в корневую директорию
3. Запустить `python App.py` — приложение само создаст `database/base.db` и все таблицы

### Эксплуатация

- Данные хранятся в SQLite-базе `database/base.db`
- Пользователи и отзывы добавляются через интерфейс приложения
- Резервное копирование: копировать `database/base.db`

### Обновление

- При добавлении нового функционала — следовать инструкции в разделе "Добавление новой команды"
- При изменении структуры таблиц — удалить `database/base.db` и запустить заново
