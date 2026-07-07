"""
column_helper — словари для перевода названий колонок и описания типов.

Модуль содержит:
- COLUMNS: словарь {англ_название: русское_название} для отображения шапки таблицы
- COLUMNS_INFO: словарь {номер: {name, type}} для валидации и сортировки колонок

Используется в uiLib.py для отображения шапки таблицы и инструкций
по сортировке/фильтрации.

Использование:
    from UI.column_helper import COLUMNS, COLUMNS_INFO
"""
COLUMNS = {
    'number' : 'Номер',
    'market_id' : 'ID',
    'city' : 'город',
    'county' : 'графство',
    'state': 'штат',
    'marketname' : 'название рынка',
    'zip': 'п. индекс',
    'score' : 'ср. оценка'
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
                   }
COLUMNS_INFO_REVERSED = {'name': 1, 'market_id': 2, 'city': 3, 'county': 4, 'state': 5,
                         'marketname': 6, 'zip': 7, 'score': 8}