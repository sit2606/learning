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

### Проблема с Qt на Windows

Если при запуске появляется ошибка `qt.qpa.plugin: Could not find the Qt platform plugin "windows"`:

```powershell
$env:QT_QPA_PLATFORM_PLUGIN_PATH=".venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms"
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

1. Нажмите кнопку **User** → окно входа → кнопка регистрации
2. Укажите координаты для работы фильтра по расстоянию
3. Просматривайте рынки в таблице, кликайте по строкам для подробностей

---

## Архитектура приложения

### MVC с AppController

```
┌─────────────────────────────────────────┐
│                 view                     │
│  Отображение (GUI PyQt5 + консоль)      │
│  (ui.py, uiLib, components/, helpers/)  │
└──────────────────┬──────────────────────┘
                   │ вызывает методы контроллера
┌──────────────────▼──────────────────────┐
│              controller                  │
│  AppController (класс, хранит self.user) │
│  workflow.py (консольный View-контроллер)│
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│           BusinessLogic                  │
│  Бизнес-логика (запросы, фильтрация)    │
│  (market_queries, processFilter, geoLib) │
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

**Правило:** зависимости только вниз. View ничего не знает о DAL. Controller не содержит `input()`/`print()`.

### AppController

Центральный контроллер — класс, хранящий состояние сессии (`self.user`):

```python
class AppController:
    def __init__(self):
        self.user = None

    def init_db(self): ...           # инициализация таблиц и импорт CSV
    def get_all_markets(self): ...   # все рынки
    def get_market_by_id(self, id): ...  # один рынок
    def get_ordered_markets(self, column, order): ...  # сортировка
    def get_filtered_markets(self, column, filter_value, coords): ...  # фильтрация
    def get_market_reviews(self, market_id): ...  # отзывы
    def delete_market(self, market_id): ...  # удаление
    def search_by_zip(self, postalcode, radius): ...  # поиск по ZIP
    def register(self, username, password, ...): ...  # регистрация
    def login(self, username, password): ...  # авторизация
    def logout(self): ...            # выход
    def update_user(self, **fields): ...  # обновление профиля
    def is_logged_in(self): ...      # проверка авторизации
    def add_review(self, market_id, score, text): ...  # добавление отзыва
```

### Потоки данных

**GUI — просмотр рынков:**
```
MainWindow.__init__()
    → controller.get_all_markets()
    → MarketCollection.from_db() → get_as_dict()
    → QStandardItemModel → tableView
```

**GUI — фильтрация:**
```
MainWindow.filter(options)
    → controller.get_filtered_markets(column, filter_value)
    → processFilter.process() → отфильтрованный dict
    → show_paged_markets() → обновление таблицы
```

**GUI — добавление отзыва (цепочка сигналов):**
```
MainWindow → DetailView → AddReviewView
    AddReviewView.review_created.emit(score, text)
    → DetailView.on_review_created(score, text)
    → DetailView.review_created.emit(market_id, score, text)
    → MainWindow.on_review_created(market_id, score, text)
    → controller.add_review(market_id, score, text)
```

**GUI — авторизация:**
```
MainWindow.open_login()
    → LoginWindow(controller)
    → controller.login(username, password)
    → MainWindow.update_current_user()
```

**Консоль:**
```
App.py → run_console(controller)
    → get_command() → proceed_command(command, controller)
    → controller.method() → uiLib.print_*()
```

---

## Добавление новой команды (GUI)

### Шаг 1: Добавить метод в AppController

```python
# controller/AppController.py

def new_method(self, param):
    """Новая операция."""
    # бизнес-логика
    return result
```

### Шаг 2: Создать окно в Qt Designer

1. Создайте `.ui` файл в `view/qtsrc/` (Dialog)
2. Сгенерируйте Python-код: `pyuic5 view/qtsrc/form.ui -o view/qtsrc/form_ui.py`

### Шаг 3: Создать компонент

```python
# view/components/new_view.py

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from view.qtsrc.form_ui import Ui_Dialog

class NewView(QDialog, Ui_Dialog):
    result_ready = pyqtSignal(dict)  # сигнал с результатом

    def __init__(self, data):
        super().__init__()
        self.setupUi(self)
        self.submitButton.clicked.connect(self._submit)

    def _submit(self):
        self.result_ready.emit({'key': 'value'})
        self.accept()
```

### Шаг 4: Подключить в MainWindow

```python
# view/components/table_view.py

from view.components.new_view import NewView

def open_new_view(self):
    dialog = NewView(data)
    dialog.result_ready.connect(self.on_new_result)
    dialog.exec_()

def on_new_result(self, result):
    self.controller.new_method(result['key'])
```

---

## Добавление новой команды (консоль)

### Шаг 1: Добавить метод в AppController

```python
# controller/AppController.py

def new_method(self, param):
    # бизнес-логика
    return result
```

### Шаг 2: Добавить маршрутизацию в workflow.py

```python
# controller/workflow.py

def proceed_command(command, controller):
    match command:
        # ... существующие команды ...
        case 'new_command':
            return _new_command(controller)
```

### Шаг 3: Добавить обработчик

```python
# controller/workflow.py

def _new_command(controller):
    param = input('Введите параметр: ')
    result = controller.new_method(param)
    print(f'Результат: {result}')
    return True
```

### Шаг 4: Обновить справку

```python
# view/uiLib.py — в print_help()
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

```python
# models/entities/new_entity.py

class NewEntity:
    def __init__(self, id=None):
        self.id = id

    def save_to_db(self):
        from DAL.new_entity_lib import create_new_entity
        create_new_entity(self)

    @classmethod
    def from_dict(cls, data):
        entity = cls(id=data['id'])
        return entity

    def get_as_dict(self):
        return {'id': self.id}
```

### Шаг 2: Создать DAL-модуль

```python
# DAL/new_entity_lib.py

import sqlite3
from config import DATABASE_PATH

def create_new_entity(entity):
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

### Шаг 4: Вызвать создание в AppController.init_db()

```python
# controller/AppController.py

def init_db(self):
    from DAL import requiredFiles
    # ... существующий код ...
    requiredFiles.create_new_entity_table()
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

AppController хранит текущего пользователя в `self.user`:

- `self.user = None` — пользователь не авторизован
- `self.user = User(...)` — объект с данными пользователя

### Поток авторизации

1. **Регистрация** (`register`) — создаёт пользователя в USERS, сохраняет в `self.user`
2. **Вход** (`login`) — проверяет логин/пароль через bcrypt, сохраняет в `self.user`
3. **Выход** (`logout`) — сбрасывает `self.user = None`

### Проверка авторизации

```python
# В контроллере
if not self.controller.is_logged_in():
    return  # или показать ошибку

# В GUI — через сигналы
def on_action(self):
    if not self.controller.is_logged_in():
        QMessageBox.warning(self, "Ошибка", "Требуется авторизация")
        return
```

---

## Работа с Qt Designer

### Генерация Python-кода из .ui

```bash
pyuic5 view/qtsrc/form.ui -o view/qtsrc/form_ui.py
```

### Добавление кастомного виджета

Не используйте promote — добавляйте программно:

```python
# В __init__ окна:
from view.components.paginationWidget import PaginationWidget
self.pagination = PaginationWidget()
self.verticalLayout.addWidget(self.pagination)
```

### Сигналы между окнами

Дочерние окна не знают о контроллере. Данные передаются через сигналы:

```python
# Дочернее окно
class ChildWindow(QDialog):
    data_ready = pyqtSignal(int, str)

    def submit(self):
        self.data_ready.emit(42, "hello")
        self.accept()

# Родительское окно
def open_child(self):
    dialog = ChildWindow()
    dialog.data_ready.connect(self.on_data)
    dialog.exec_()

def on_data(self, number, text):
    self.controller.do_something(number, text)
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
| `Could not find Qt platform plugin` | PyQt5 не находит плагины | Установить QT_QPA_PLATFORM_PLUGIN_PATH |
| `AttributeError: 'tuple' has no attribute 'lower'` | tuple передан в текстовый фильтр | Проверять тип колонки перед фильтрацией |
| `TypeError: 'module' object is not callable` | Импортирован модуль вместо класса | `from module import Class` вместо `from package import module` |

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
- При изменении `.ui` файлов — перегенерировать `pyuic5`
