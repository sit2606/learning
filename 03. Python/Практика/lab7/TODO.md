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
- **market.py**: добавлен `Market.from_db(market_id)` — загрузка из БД со всеми справочниками
- **market.py**: добавлен `Market.update()` — сохранение в БД
- **market.py**: добавлен `Market.calculate_score()` — пересчёт оценки из отзывов
- **market.py**: добавлен `Market.get_reviews()` — получение отзывов
- **market.py**: добавлен `Market.delete()` — удаление рынка
- **datalib2.py**: `update_market()` переделан с dict на Market
- **datalib2.py**: добавлен `delete_market()`
- **market_queries.py**: `get_market_by_id()` исправлен — вызывает `Market.from_db()`
- **market_queries.py**: `get_all_markets_filtered_by_column()` перенесён из marketList
- **market_queries.py**: исправлена сортировка с None-значениями (score)
- **review.py**: полная реализация — `__init__`, `set_text`, `set_score`, `save_to_db`, `from_dict`, `get_as_dict`
- **user.py**: `__init__` принимает dict (убран отдельный id-параметр)
- **user.py**: `from_db()` поддерживает поиск по user_id и username
- **user.py**: добавлен `get_as_dict()`

## Сделано (27.07)
- Удалены старые CSV-модули: marketList.py, dataLib.py, fileLib.py, referenceLib.py, reviewLib.py, userLib.py
- commandHandler.py переведён на OOP-модули (Review, User, market_queries)
- workflowLib.py переведён на OOP (User.from_db вместо dict)
- reviewlib2.py: `get_review_by_market_id()` возвращает `list[Review]`
- reviewlib2.py: добавлен `delete_reviews_by_market_id()`
- config.py: DEFAULT_USER содержит 'id'

## Сделано (10.08)
- **Рефакторинг MVC**: `workflowLib.py` и `commandHandler.py` перемещены из `BusinessLogic/` в `controller/`
- **UI реструктуризация**: `UI/` переименован в `view/` с подпапками `components/`, `helpers/`, `qtsrc/`
- **GUI**: добавлен `view/ui.py` (запуск PyQt5), `view/components/table_view.py` (главное окно)
- **Qt Designer**: `view/qtsrc/table_ui.py` — сгенерированный UI-код из `table_view.ui`
- **PyQt5**: установка `pyqt5` и `pyqt5-tools`, работа Qt Designer на Python 3.14
- **commandHandler.py**: часть `input()` вынесена в `uiLib` (`request_start_and_step`, `request_continue`, `request_column_and_order`)

## Исправленные баги
- **datalib2.py**: пропущен пробел перед `WHERE` в UPDATE-запросе
- **datalib2.py**: SQL injection через f-string → параметризованный запрос
- **datalib2.py**: неправильные тексты ошибок в get_market/get_all_markets
- **market_queries.py**: TypeError при сортировке с None (score) → разделение на with/without values
- **workflow.py**: `return com = ...` — неверный синтаксис, разбито на две строки

## Не сделано
- MARKETS таблица: street, city хранятся как TEXT, а должны быть INTEGER (FK на справочники)
- distance — расчёт расстояния (geoLib.get_distance) не интегрирован в market_queries
- `userlib2.delete_user()` — нет docstring
- Тесты (tests.py)
- commandHandler: оставшиеся `input()` в `command_show`, `register_user`, `login_user`, `add_review`, `delete_market`, `command_zip`
- table_view.py: данные захардкожены, нужен вызов `load_data()` из controller
