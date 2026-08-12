"""
column_helper — словари для перевода названий колонок и описания типов.

Модуль содержит:
- COLUMNS: словарь {англ_название: русское_название} для отображения шапки таблицы
- COLUMNS_INFO: словарь {номер: {name, type}} для валидации и сортировки колонок
- COLUMNS_INFO_REVERSED: словарь {имя_колонки: номер} — обратный маппинг
- COLUMN_TO_SHOW: список имён колонок для отображения в таблице

Поддерживаемые колонки:
1 — number (номер), 2 — market_id (ID), 3 — city (город),
4 — county (графство), 5 — state (штат), 6 — marketname (название рынка),
7 — zip (п. индекс), 8 — score (ср. оценка), 9 — distance (расстояние в км)

Использование:
    from view.column_helper import COLUMNS, COLUMNS_INFO, COLUMN_TO_SHOW
"""
COLUMNS = {
    'number' : 'Номер',
    'market_id' : 'ID',
    'city' : 'город',
    'county' : 'графство',
    'state': 'штат',
    'marketname' : 'название рынка',
    'zip': 'п. индекс',
    'score' : 'ср. оценка',
    'distance': 'расстояние'
}

COLUMNS_INFO = {1: {'name': 'number',
                    'type': 'numeric'},
                   2: {'name':'market_id',
                       'type': 'numeric'},
                   3: {'name':'city',
                       'type': 'text'},
                   4: {'name':'county',
                       'type':'text'},
                   5: {'name': 'state',
                       'type': 'text'},
                   6: {'name':'marketname',
                       'type': 'text'},
                   7: {'name':'zip',
                       'type': 'numeric'},
                   8: {'name':'score',
                       'type': 'numeric'},
                   9:{'name': 'distance',
                      'type': 'numeric'},
                   }
COLUMNS_INFO_REVERSED = {'name': 1, 'market_id': 2, 'city': 3, 'county': 4, 'state': 5,
                         'marketname': 6, 'zip': 7, 'score': 8, 'distance': 9}
COLUMN_TO_SHOW = ['market_id', 'city', 'county', 'state',
                         'marketname', 'zip', 'score', 'distance']