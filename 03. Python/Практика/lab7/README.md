# Лабораторная работа 7 — Управление данными о фермерских рынках

## Описание

Приложение для парсинга CSV-датасета фермерских рынков (Export.csv), создания справочников и связывания данных через промежуточные CSV-файлы. Построено по трёхуровневой архитектуре: UI → BusinessLogic → DAL.

### Возможности приложения

- Просмотр списка всех фермерских рынков с пагинацией
- Просмотр подробной информации о каждом рынке (адрес, расписание, соцсети, оплата, товары)
- Поиск и фильтрация по городу, штату, графству, названию, индексу, оценке
- Фильтрация по расстоянию от пользователя (формула Хаверсина)
- Сортировка по любой колонке (по возрастанию/убыванию)
- Регистрация и авторизация пользователей
- Добавление отзывов с оценкой 1-5
- Обновление данных пользователя (логин, имя, фамилия, координаты)

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
# Windows
.venv\Scripts\activate

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

### Автоматическая инициализация

При первом запуске приложение автоматически:
- Создаёт папку `files/`
- Парсит `Export.csv` и создаёт CSV-файлы
- Инициализирует справочники (MEDIA, GROCERY_TYPES, BANKING_INFO)
- Создаёт файлы пользователей и отзывов

---

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
│   ├── dataLib.py                  # CRUD-операции с рынками
│   ├── userLib.py                  # CRUD-операции с пользователями
│   ├── reviewLib.py                # CRUD-операции с отзывами
│   └── requiredFiles.py            # Константы категорий и список файлов
├── UI/                             # Слой интерфейса пользователя
│   ├── uiLib.py                    # Функции вывода и ввода в консоль
│   ├── column_helper.py            # Словари перевода названий колонок и описания типов
│   └── comparison_helper.py        # Константы знаков сравнения для фильтрации
├── files/                          # CSV-файлы (справочники, связи, данные)
├── документация/                   # Диаграммы и пользовательские истории
├── Задание.md                      # Техническое задание
├── .gitignore                      # Исключения Git
├── README.md                       # Руководство пользователя
├── CONTRIBUTING.md                 # Руководство администратора
├── requirements.txt                # Зависимости проекта
└── Export.csv                      # Исходный датасет
```

---

## Руководство пользователя

### Запуск

```bash
python App.py
```

### Доступные команды

| Команда | Описание | Требуется авторизация |
|---------|----------|:---------------------:|
| `help` | Вывод справки по командам | Нет |
| `list_all` | Вывод таблицы со списком всех рынков | Нет |
| `list` | Вывод таблицы рынков с пагинацией | Нет |
| `order` | Сортировка рынков по колонке (1-9) | Нет |
| `show` | Подробная информация о рынке по ID | Нет |
| `filter` | Фильтрация рынков по критерию | Да |
| `register` | Регистрация нового пользователя | Нет |
| `login` | Авторизация пользователя | Нет |
| `logout` | Выход из системы | Да |
| `review` | Добавление отзыва на рынок | Да |
| `update_user` | Обновление данных пользователя | Да |
| `exit` | Выход из приложения | Нет |

### Просмотр списка рынков

**Команда `list_all`** — выводит таблицу со всеми рынками:
```
| market_id | city | county | state | marketname | zip | score | distance |
```

**Команда `list`** — список с пагинацией:
1. Введите стартовый номер (по умолчанию 1)
2. Введите шаг (по умолчанию 10)
3. Нажмите `y` для продолжения или `n` для завершения

### Сортировка

**Команда `order`** — сортировка по колонке:
1. Введите номер колонки (1-9):
   - 1: Номер, 2: ID, 3: Город, 4: Графство, 5: Штат
   - 6: Название, 7: Индекс, 8: Оценка, 9: Расстояние
2. Введите порядок: `a` — по возрастанию, `d` — по убыванию

### Просмотр данных рынка

**Команда `show`** — подробная информация:
1. Введите ID рынка
2. Просмотрите информацию (адрес, расписание, соцсети, оплата, товары)
3. Введите `y` для просмотра отзывов или Enter для возврата

### Фильтрация

**Команда `filter`** — фильтрация по критерию (требуется авторизация):
1. Выберите номер колонки (1-9)
2. Для текстовых колонок: введите название (город, штат и т.д.)
3. Для числовых колонок: введите формулу (например, `> 100`, `< 50`, `= 0`)
4. Для расстояния (колонка 9): фильтрация по км от вашего местоположения

### Работа с отзывами

**Команда `review`** — добавление отзыва (требуется авторизация):
1. Введите ID рынка
2. Введите оценку от 1 до 5
3. Введите текст отзыва (опционально)
4. Введите `back` для отмены

### Управление профилем

**Команда `register`** — регистрация:
1. Введите логин (уникальный)
2. Введите пароль
3. Введите имя и фамилию
4. Укажите координаты (опционально, для фильтрации по расстоянию)

**Команда `login`** — авторизация:
1. Введите логин
2. Введите пароль

**Команда `update_user`** — обновление данных (требуется авторизация):
1. Выберите пункт для изменения (1-4)
2. Введите новое значение

---

## Скриншоты интерфейса

> Скриншоты будут добавлены позже.

---

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
      ├── dataLib.py                — CRUD рынков
      ├── userLib.py                — CRUD пользователей
      ├── reviewLib.py              — CRUD отзывов
      └── requiredFiles.py          — константы
```

Зависимости: `App.py` → `BusinessLogic` + `UI` → `DAL`

---

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
         ├─ get_command(user)        → BusinessLogic/workflowLib
         └─ proceed_command(cmd, user) → BusinessLogic/workflowLib
                 │
                 ├─ 'help'       → commandHandler.command_help() → True
                 │                   → uiLib.print_help()
                 │
                 ├─ 'list_all'   → commandHandler.command_list_all() → (True, markets)
                 │                   → marketList.get_all_markets('num')
                 │                   → uiLib.print_list(markets)
                 │
                 ├─ 'list'       → commandHandler.command_list() → (True, markets, start, step)
                 │                   → marketList.get_all_markets('num')
                 │                   → uiLib.print_list(markets, start, step)
                 │
                 ├─ 'order'      → commandHandler.command_order() → (True, markets, col, order)
                 │                   → marketList.get_all_markets_ordered_by_column()
                 │                   → uiLib.print_list(markets, col_name)
                 │
                 ├─ 'show'       → commandHandler.command_show() → (True, market_info)
                 │                   → marketList.get_market_by_id(market_id)
                 │                   → (опционально) get_review_by_market_id() → print_market_reviews()
                 │
                 ├─ 'filter'     → commandHandler.show_filtered(user) → (True, user)
                 │                   → uiLib.request_filter()
                 │                   → marketList.get_all_markets_filtered_by_column()
                 │
                 ├─ 'register'   → commandHandler.register_user() → (True, user)
                 │                   → uiLib.get_user_coordinates_manually()
                 │
                 ├─ 'login'      → commandHandler.login_user(user) → (True, user)
                 │
                 ├─ 'logout'     → commandHandler.logout_user(user) → (True, None)
                 │
                 ├─ 'review'     → commandHandler.add_review(user) → (True, user)
                 │                   → reviewLib.create_review(review)
                 │
                 ├─ 'update_user' → commandHandler.update_user(user) → (True, user)
                 │                   → uiLib.request_user_updates(user)
                 │
                 └─ 'exit'       → commandHandler.command_exit() → False
                                     → uiLib.print_exit()
```

---

## Требования

- Python 3.10+
- Стандартная библиотека: `csv`, `uuid`, `os`, `getpass`, `statistics`, `math`

## Установка зависимостей

```bash
pip install -r requirements.txt
```

| Пакет | Версия | Назначение |
|-------|--------|------------|
| bcrypt | ≥ 4.0 | Хеширование паролей пользователей |

---

## Дополнительно

- [CONTRIBUTING.md](CONTRIBUTING.md) — руководство администратора (развёртывание, архитектура, добавление команд)
- [Задание.md](Задание.md) — техническое задание
