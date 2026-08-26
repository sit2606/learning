# Лабораторная работа 7 — Управление данными о фермерских рынках

## Описание

Приложение для управления данными о фермерских рынках США. Загружает CSV-датасет (Export.csv) в SQLite-базу, предоставляет графический (PyQt5) и консольный интерфейс для просмотра, поиска, фильтрации, сортировки и отзывов.

Архитектура: MVC — View → Controller (AppController) → BusinessLogic → DAL + models.

### Возможности приложения

- Просмотр списка всех фермерских рынков с пагинацией
- Просмотр подробной информации о каждом рынке (адрес, расписание, соцсети, оплата, товары)
- Поиск и фильтрация по городу, штату, графству, названию, индексу, оценке
- Фильтрация по расстоянию от пользователя (формула Хаверсина)
- Сортировка по любой колонке (по возрастанию/убыванию)
- Регистрация и авторизация пользователей
- Добавление отзывов с оценкой 1-5
- Обновление данных пользователя (логин, имя, фамилия, координаты)
- Поиск рынков в радиусе от почтового индекса

---

## Развёртывание

### Требования

- Python 3.10+
- Файл `Export.csv` в корневой директории проекта

### Установка

1. Клонируйте репозиторий:
```bash
git clone <url>
cd lab7
```

2. Создайте виртуальное окружение:
```bash
python -m venv .venv
```

3. Активируйте окружение:
```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate
```

4. Установите зависимости:
```bash
pip install -r requirements.txt
```

5. Поместите файл `Export.csv` в корневую директорию проекта.

6. Запустите приложение:
```bash
python App.py
```

### Проблема с Qt на Windows

Если при запуске появляется ошибка `Could not find the Qt platform plugin "windows"`, установите переменную окружения перед запуском:

```powershell
$env:QT_QPA_PLATFORM_PLUGIN_PATH=".venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms"
python App.py
```

### Автоматическая инициализация

При первом запуске приложение автоматически:
- Создаёт SQLite-базу `database/base.db`
- Создаёт таблицы: MARKETS, USERS, REVIEWS, справочники (CITY, COUNTY, STATE, ZIP, STREET, MEDIA, GROCERY_TYPES, BANKING_INFO) и связующие таблицы
- Инициализирует справочники из CSV-констант
- Импортирует данные из `Export.csv` в таблицу MARKETS

---

## Структура проекта

```
lab7/
├── App.py                              # Точка входа приложения
├── config.py                           # DATABASE_PATH, DEFAULT_USER
├── controller/                         # Слой контроллера (MVC)
│   ├── AppController.py                # Центральный контроллер (класс с self.user)
│   └── workflow.py                     # Консольный View-контроллер, маршрутизация команд
├── BusinessLogic/                      # Слой бизнес-логики
│   ├── market_queries.py               # OOP-запросы к рынкам (сортировка, фильтрация)
│   ├── processFilter.py                # Обработка фильтрации рынков
│   └── geoLib.py                       # Библиотека геоданных и расчёта дистанций
├── DAL/                                # Слой доступа к данным (Data Access Layer)
│   ├── datalib2.py                     # CRUD-операции с рынками (SQLite)
│   ├── referencelib2.py                # CRUD-операции со справочниками и связями (SQLite)
│   ├── reviewlib2.py                   # CRUD-операции с отзывами (SQLite)
│   ├── userlib2.py                     # CRUD-операции с пользователями (SQLite)
│   ├── filelib2.py                     # Импорт Export.csv → SQLite
│   └── requiredFiles.py               # Константы категорий, создание таблиц
├── models/                             # Слой сущностей (OOP)
│   ├── entities/
│   │   ├── market.py                   # Market + dataclass-ы
│   │   ├── reference.py                # Reference — обёртка над справочниками
│   │   ├── review.py                   # Review — сущность отзыва
│   │   └── user.py                     # User — сущность пользователя
│   └── collections/
│       └── market_collection.py        # MarketCollection — коллекция рынков
├── view/                               # Слой представления (MVC)
│   ├── ui.py                           # Запуск GUI (PyQt5)
│   ├── uiLib.py                        # Функции вывода и ввода в консоль
│   ├── components/                     # Qt-виджеты (окна приложения)
│   │   ├── table_view.py               # Главное окно с таблицей рынков
│   │   ├── detail_view.py              # Окно подробностей о рынке
│   │   ├── login_view.py               # Окно авторизации
│   │   ├── register_view.py            # Окно регистрации
│   │   ├── add_review_view.py          # Окно добавления отзыва
│   │   ├── filter_view.py              # Окно фильтрации
│   │   ├── user_detail.py              # Окно профиля пользователя
│   │   ├── zipdistance_view.py         # Окно поиска по ZIP
│   │   └── paginationWidget.py         # Виджет пагинации
│   ├── helpers/                        # Вспомогательные константы
│   │   ├── column_helper.py            # Словари перевода названий колонок
│   │   └── comparison_helper.py        # Константы знаков сравнения
│   └── qtsrc/                          # Сгенерированные файлы Qt Designer
│       ├── table_view.ui / table_ui.py
│       ├── detail_form.ui / detail_ui.py
│       ├── login_form.ui / login_ui.py
│       ├── register_form.ui / register_ui.py
│       ├── add_review_form.ui / add_review_ui.py
│       ├── filter_form.ui / filter_ui.py
│       ├── user_form.ui / user_ui.py
│       └── pagination_widget.ui / pagination_widget.py
├── database/                           # SQLite-база данных
│   └── base.db
├── документация/                       # Диаграммы и пользовательские истории
├── Задание.md                          # Техническое задание
├── MVC_REFACTORING_PLAN.md             # План рефакторинга MVC
├── .gitignore                          # Исключения Git
├── README.md                           # Руководство пользователя
├── CONTRIBUTING.md                     # Руководство администратора
├── requirements.txt                    # Зависимости проекта
└── Export.csv                          # Исходный датасет
```

---

## Руководство пользователя

### Запуск

```bash
python App.py
```

Приложение запускается с графическим интерфейсом (PyQt5). Для переключения на консольный режим измените `App.py`:

```python
run_console(controller)   # консольный режим
# run_gui(controller)     # графический режим (по умолчанию)
```

### Графический интерфейс (GUI)

#### Главное окно

- Таблица со списком рынков с пагинацией
- Кнопки: **View** (переключение All/By page), **User** (профиль/вход), **Filter** (фильтрация)
- Панель пагинации: выбор размера страницы (5/10/20/30/50), навигация ←/→
- Клик по строке таблицы открывает подробности о рынке

#### Авторизация

- Кнопка **User** без авторизации → окно входа
- В окне входа: ввод логина/пароля, кнопка регистрации
- Кнопка **User** с авторизацией → профиль пользователя (выход, обновление данных)

#### Просмотр рынка

- Клик по строке таблицы → окно с подробной информацией
- Адрес, расписание, соцсети, способы оплаты, продаваемые товары
- Кнопка добавления отзыва (требуется авторизация)

#### Фильтрация

- Кнопка **Filter** → окно выбора колонки и критерия
- Для текстовых колонок: ввод подстроки
- Для числовых: выбор оператора (>, <, >=, <=, =) и значения
- Кнопка сброса фильтра возвращает полный список

#### Сортировка

- Через ComboBox в окне фильтрации или через меню

### Консольный интерфейс

| Команда | Описание | Требуется авторизация |
|---------|----------|:---------------------:|
| `help` | Вывод справки по командам | Нет |
| `list_all` | Вывод таблицы со списком всех рынков | Нет |
| `list` | Вывод таблицы рынков с пагинацией | Нет |
| `order` | Сортировка рынков по колонке (1-9) | Нет |
| `show` | Подробная информации о рынке по ID | Нет |
| `filter` | Фильтрация рынков по критерию | Да |
| `register` | Регистрация нового пользователя | Нет |
| `login` | Авторизация пользователя | Нет |
| `logout` | Выход из системы | Да |
| `review` | Добавление отзыва на рынок | Да |
| `update_user` | Обновление данных пользователя | Да |
| `delete` | Удаление рынка и его связей | Да |
| `zip` | Поиск рынков в радиусе от почтового индекса | Нет |
| `exit` | Выход из приложения | Нет |

---

## Архитектура

```
App.py
 │
 ├── controller/AppController.py     ← Controller (класс, хранит self.user)
 │    Методы: get_all_markets, get_market_by_id, get_ordered_markets,
 │    get_filtered_markets, get_market_reviews, delete_market,
 │    search_by_zip, register, login, logout, update_user,
 │    is_logged_in, add_review, init_db
 │
 ├── controller/workflow.py          ← View-контроллер консоли
 │    Связывает uiLib с AppController
 │
 ├── view/                           ← View (отображение)
 │    ├── ui.py                      — запуск GUI (PyQt5)
 │    ├── uiLib.py                   — консольный ввод/вывод
 │    ├── components/                — GUI-окна (каждое получает controller)
 │    ├── helpers/                   — константы колонок и сравнения
 │    └── qtsrc/                     — сгенерированный UI-код
 │
 ├── BusinessLogic/                  ← Бизнес-логика
 │    ├── market_queries.py          — запросы к рынкам
 │    ├── processFilter.py           — фильтрация
 │    └── geoLib.py                  — гео-расчёты
 │
 ├── models/                         ← Сущности (OOP)
 │    ├── entities/                  — Market, User, Review, Reference
 │    └── collections/               — MarketCollection
 │
 └── DAL/                            ← Доступ к данным (SQLite)
      ├── datalib2.py, userlib2.py, reviewlib2.py, referencelib2.py
      ├── filelib2.py               — импорт CSV
      └── requiredFiles.py          — создание таблиц
```

**Правило зависимостей:** View → Controller → BusinessLogic → models → DAL. View ничего не знает о DAL. Controller не содержит I/O.

---

## Схема данных (SQLite)

### Таблица MARKETS
```
id (INTEGER PK), marketname, street, city, county, state, zip,
longitude (REAL), latitude (REAL),
season1date, season1time, ..., season4date, season4time,
score (REAL)
```

### Справочники (Common)
```
CITY, COUNTY, STATE, ZIP, STREET: id (INTEGER PK), name (TEXT UNIQUE)
MEDIA, GROCERY_TYPES, BANKING_INFO: id (INTEGER PK), name (TEXT UNIQUE)
```

### Связующие таблицы (Connection)
```
MarketXSocialMedia, MarketXGrocery, MarketXBankingInfo:
  market_id (INTEGER), reference_id (INTEGER), status (TEXT)
  PRIMARY KEY (market_id, reference_id)
```

### Таблица USERS
```
id (INTEGER PK AUTOINCREMENT), username (TEXT UNIQUE), password (TEXT),
firstname, lastname, latitude (REAL), longitude (REAL)
```

### Таблица REVIEWS
```
id (INTEGER PK AUTOINCREMENT), review_date (TEXT), user_id (INTEGER),
market_id (INTEGER), review_text (TEXT), score (REAL)
```

---

## Требования

- Python 3.10+
- Стандартная библиотека: `csv`, `uuid`, `os`, `getpass`, `statistics`, `math`, `sqlite3`, `dataclasses`, `datetime`

## Установка зависимостей

```bash
pip install -r requirements.txt
```

| Пакет | Версия | Назначение |
|-------|--------|------------|
| bcrypt | ≥ 4.0 | Хеширование паролей пользователей |
| geopy | ≥ 2.4 | Геокодирование по почтовому индексу (get_zip_coords) |
| PyQt5 | ≥ 5.15 | Графический интерфейс (GUI) |

---

## Дополнительно

- [CONTRIBUTING.md](CONTRIBUTING.md) — руководство администратора (развёртывание, архитектура, добавление команд)
- [Задание.md](Задание.md) — техническое задание
