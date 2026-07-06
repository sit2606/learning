# Руководство разработчика

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

### Шаг 5: Добавить константу перевода (опционально)

Если команда работает с колонками, добавьте перевод в `column_helper.py`:

```python
# UI/column_helper.py

COLUMNS = {
    # ... существующие колонки ...
    'new_column': 'новая колонка'
}
```

### Пример: команда show

Команда `show` выводит данные одного рынка по Id:

1. `commandHandler.command_show()` — запрашивает ID у пользователя, получает данные через `get_market_by_id()`
2. `workflowLib.proceed_command('show', user)` — вызывает обработчик
3. `uiLib.print_detailed_market_info(market_info)` — выводит подробную информацию

---

## Добавление новой колонки в Export.csv

### Шаг 1: Определить категорию

Решите, к какой категории относится колонка:

| Категория | Назначение | Файл связей |
|-----------|------------|-------------|
| MARKET_INFO | Основная информация | нет (в MARKET_INFO.csv) |
| COORDINATES | Координаты | нет (в MARKET_INFO.csv) |
| TIMESHEET_INFO | Расписание | нет (в MARKET_INFO.csv) |
| MEDIA | Соцсети | MarketXSocialMedia.csv |
| GROCERY_TYPES | Товары | MarketXGrocery.csv |
| BANKING_INFO | Оплата | MarketXBankingInfo.csv |
| LOCATION | Местоположение | CITY/COUNTY/STATE.csv |

### Шаг 2: Добавить колонку в requiredFiles.py

```python
# DAL/requiredFiles.py

# Если колонка относится к существующей категории:
MEDIA = {
    # ... существующие колонки ...
    'Instagram'  # новая колонка
}

# Если колонка — новая категория:
NEW_CATEGORY = {'NewColumn1', 'NewColumn2'}
```

### Шаг 3: Если новая категория — добавить в FILES_TO_CHECK

```python
# DAL/requiredFiles.py

FILES_TO_CHECK = {
    # ... существующие файлы ...
    'NEW_CATEGORY'  # имя CSV-файла связей
}
```

### Шаг 4: Если новая категория — обработать в fileLib.py

Добавьте обработку в `read_csv()`:

```python
# DAL/fileLib.py

def read_csv():
    # ... существующий код ...
    new_category_list = []

    for row in reader:
        # ... существующая обработка ...
        if key in requiredFiles.NEW_CATEGORY:
            reference_id = new_reference[key]
            new_category_list.append([current_id, reference_id, value])

    # После цикла — батчевая запись
    create_connection_entry_by_list('NewCategoryXMarket', new_category_list)
```

### Шаг 5: Если новая категория — добавить справочник в REF_LIST

```python
# DAL/fileLib.py

REF_LIST = [
    {'MEDIA': requiredFiles.MEDIA},
    {'GROCERY_TYPES': requiredFiles.GROCERY_TYPES},
    {'BANKING_INFO': requiredFiles.BANKING_INFO},
    {'NEW_CATEGORY': requiredFiles.NEW_CATEGORY}  # новый справочник
]
```

### Шаг 6: Если новая категория — обработать в marketList.py

Добавьте резолвинг ID → имена:

```python
# BusinessLogic/marketList.py

def get_all_markets(mode):
    # ... существующий код ...
    new_reference = get_reference_with_uid_as_key('NEW_CATEGORY', 'Common')

    for market_id, market_info in market_base.items():
        # ... существующий резолвинг ...
        if 'new_column' in market_info:
            market_info['new_column'] = new_reference[market_info['new_column']]
```

### Шаг 7: Обновить MARKET_INFO.csv

Если колонка должна попасть в итоговый файл, добавьте в `create_market_base()`:

```python
# DAL/fileLib.py

def create_market_base(market_info):
    field_names = [
        # ... существующие поля ...
        'new_column'  # новое поле
    ]
```

---

## Добавление нового справочника

### Шаг 1: Создать множество в requiredFiles.py

```python
# DAL/requiredFiles.py

NEW_REFERENCE = {'Value1', 'Value2', 'Value3'}
```

### Шаг 2: Добавить в REF_LIST в fileLib.py

```python
# DAL/fileLib.py

REF_LIST = [
    # ... существующие справочники ...
    {'NEW_REFERENCE': requiredFiles.NEW_REFERENCE}
]
```

### Шаг 3: Добавить в FILES_TO_CHECK

```python
# DAL/requiredFiles.py

FILES_TO_CHECK = {
    # ... существующие файлы ...
    'NEW_REFERENCE'
}
```

### Шаг 4: Обновить Reference_Base.csv

Файл создается автоматически через `create_reference_base()` при пересоздании данных.

---

## Добавление нового метода в referenceLib

### Шаг 1: Создать функцию

```python
# DAL/referenceLib.py

def new_method(reference_name, params):
    """
    Описание метода.

    Args:
        reference_name (str): Имя справочника.
        params: Параметры.

    Returns:
        Тип возвращаемого значения.
    """
    # Реализация
```

### Шаг 2: Обновить модульный docstring

Добавьте описание в документацию модуля:

```python
"""
referenceLib — библиотека для управления справочниками и связями.

Основные функции:
- ...
- new_method(): описание нового метода
"""
```

---

## Добавление нового типа сущности (например, отзывы)

### Шаг 1: Создать модуль в DAL/

Создайте файл `DAL/newEntityLib.py` с функциями CRUD:

```python
# DAL/newEntityLib.py

"""
newEntityLib — библиотека для работы с новыми сущностями.

Основные функции:
- create_entity(entity): добавление сущности
- read_entity(id): чтение сущности
- update_entity(entity): обновление сущности
- delete_entity(id): удаление сущности
"""
import csv

def create_entity(entity):
    """Добавляет сущность в CSV-файл."""
    field_names = ['Id', 'field1', 'field2']
    file_path = "files/NEW_ENTITY.csv"
    try:
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writerow(entity)
    except Exception as e:
        print(e)
        print("Error in create_entity")
```

### Шаг 2: Добавить создание CSV-файла в fileLib.py

```python
# DAL/fileLib.py

def create_new_entity_base():
    """Создаёт CSV-файл для новых сущностей."""
    _reference_name = 'NEW_ENTITY'
    field_names = ['Id', 'field1', 'field2']
    try:
        with open(f"files/{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
    except Exception as e:
        print(e)
        print("Error in create_new_entity_base")
```

### Шаг 3: Добавить в requiredFiles.py

```python
# DAL/requiredFiles.py

FILES_TO_CHECK = {
    # ... существующие файлы ...
    'NEW_ENTITY'
}
```

### Шаг 4: Вызвать создание в workflowLib.py

```python
# BusinessLogic/workflowLib.py

def file_creation():
    # ... существующий код ...
    fileLib.create_new_entity_base()
    print('New entity base successfully created...')
```

### Шаг 5: Создать обработчик в commandHandler.py

```python
# BusinessLogic/commandHandler.py

def add_entity(user):
    """
    Добавление новой сущности.

    Args:
        user: Текущий авторизованный пользователь или None.

    Returns:
        (True, user) — после успешного добавления.
    """
    if user is None:
        print('Требуется авторизация.')
        return True, user

    entity = {}
    entity['Id'] = str(uuid.uuid4())
    entity['field1'] = input('Введите field1: ')
    entity['field2'] = input('Введите field2: ')

    from DAL.newEntityLib import create_entity
    create_entity(entity)
    print('Сущность успешно добавлена!')
    return True, user
```

### Шаг 6: Добавить команду в workflowLib.py

```python
# BusinessLogic/workflowLib.py

def proceed_command(command, user):
    # ... существующий код ...
    match command:
        # ... существующие команды ...
        case 'new_entity':
            is_run, user = commandHandler.add_entity(user)
        # ...
```

### Шаг 7: Обновить справку в uiLib.py

```python
# UI/uiLib.py

def print_help():
    # ... существующий код ...
    print('new_entity - описание новой команды')
```

---

## Структура данных

### CSV-файлы справочников (Id, Name)

```
Id,Name
uuid1,Value1
uuid2,Value2
```

### CSV-файлы связей (market_id, reference_id, status)

```
market_id,reference_id,status
fmid1,uuid1,True
fmid2,uuid2,False
```

### MARKET_INFO.csv

```
market_id,marketname,street,city,county,state,zip,season1date,season1time,...
fmid1,Market Name,123 St,City,County,State,12345,2024-01-01,09:00,...
```

---

## Тестирование

### Ручное тестирование

```python
python
>>> import DAL.referenceLib as ref
>>> ref.create_reference('TEST')
>>> ref.create_reference_entry('TEST', 'value')
>>> ref.read_reference_entry('TEST', entry_name='value')
```

### Автоматическое тестирование

```bash
pip install pytest
pytest test_*.py -v
```

---

## Система сессий (авторизация)

Приложение поддерживает отслеживание текущего пользователя через объект `user`:

- `user = None` — пользователь не авторизован
- `user = {...}` — словарь с данными пользователя (Id, user_name, firstname,lastname, location)

### Поток авторизации

1. **Регистрация** (`register`) — создаёт пользователя, возвращает `user`
2. **Вход** (`login`) — проверяет логин/пароль, возвращает `user` или `None`
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
| `KeyError` в marketList | Колонка не добавлена в columns dict | Добавить маппинг номер → имя |
| `FileNotFoundError` | Файл не создан | Проверить FILES_TO_CHECK и REF_LIST |
| `NoneType` в read_csv | Справочник не инициализирован | Вызвать prepare_ref() перед read_csv() |
| Дубли в связях | Повторный вызов read_csv | Очищать файлы перед пересозданием |
| `KeyError` в get_market_by_id | Рынок не найден в MARKET_INFO.csv | Проверить market_id, пересоздать файлы |
| `Error in create_reference_base` | Папка files/ не создана | Вызвать directory_creation() перед file_creation() |
