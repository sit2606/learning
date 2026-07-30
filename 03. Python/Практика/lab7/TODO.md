# Прогресс

## Сделано (24.07)
- Разделил models на entities/ и collections/
- Обновил документацию
- Создал market_queries.py с TODO
- начал перенос на ООП подход для marketList

## Сделано (25.07)
- Добавлен change_mode в MarketCollection и Market
- Небольшой рефакторинг filelib2
- Продолжение работы над get_all_markets_ordered_by_column

## Сделано (26.07)
- **market.py**: добавлены dataclass-ы BankInfo, MediaInfo, GroceryInfo
- **market.py**: добавлен `Market.from_db(market_id)` — загрузка из БД со всеми справочниками (локации + связи)
- **market.py**: добавлен `Market.update()` — сохранение в БД через datalib2
- **market.py**: `__init__` теперь инициализирует `ref_mode = 'id'` в начале
- **datalib2.py**: `update_market()` переделан с dict на Market (автоматическая конвертация ref_mode)
- **market_queries.py**: `get_market_by_id()` исправлен — теперь вызывает `Market.from_db()`
- **market_queries.py**: `get_all_markets_filtered_by_column()` перенесён из marketList
- **user.py**: добавлены docstrings ко всем методам
- **review.py**: исправлена синтаксическая ошибка (было `idGhjdthm`)

## Исправленные баги
- **datalib2.py:121**: пропущен пробел перед `WHERE` в UPDATE-запросе
- **datalib2.py:143**: SQL injection через f-string → заменён на параметризованный запрос
- **datalib2.py:150,167**: текст ошибки "Error in create_market" → исправлен на правильные имена функций
- **review.py:3**: синтаксическая ошибка `idGhjdthm` → исправлено

## Обновлена документация
- **market.py**: модульный docstring (добавлены новые dataclass-ы и методы), docstrings для `from_db()`, `update()`
- **datalib2.py**: модульный docstring (добавлены get_market, get_all_markets), docstring для update_market (подпись изменена с dict на Market)
- **market_queries.py**: модульный docstring (отмечены мигрированные функции), docstrings для get_market_by_id, get_all_markets_filtered_by_column
- **user.py**: полные docstrings для модуля, класса и всех методов
- **market_collection.py**: улучшен docstring для from_dict

## Не сделано
- `get_all_markets_ordered_by_column` — сортировка закомментирована, distance не работает
- `MARKETS` таблица: street TEXT, city TEXT → должны быть INTEGER (FK)
- `reviewlib2.calculate_score()` — вызывает старые функции из marketList
- `commandHandler.py` — использует старый marketList, не market_queries
- `user.py` — `from_db` и `update_db` — @staticmethod vs обычный метод (обсуждаем)
- `review.py` — заготовка, нужна полная реализация
- MARKETS table column types: street, city → INTEGER (FK)
- Full OOP rewrite of remaining BusinessLogic functions
