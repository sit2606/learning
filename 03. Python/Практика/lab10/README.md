# Морской Бой

Десктопная игра "Морской Бой" с графическим интерфейсом. Игрок против компьютера.

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
python -m view.main
```

## Тесты

```bash
python run_tests.py
```

## Структура проекта

```
lab10/
├── controller/
│   └── AppController.py          # Контроллер (связывает Model и View)
├── model/
│   ├── AI.py                     # ИИ компьютера
│   ├── GameResult.py             # Сохранение/загрузка результатов
│   └── entities/
│       ├── Cell.py               # Клетка поля
│       ├── Ship.py               # Корабль
│       ├── Board.py              # Игровое поле
│       ├── Player.py             # Игрок
│       ├── Config.py             # Конфигурация (settings.json)
│       ├── Game.py               # Фасад игровой логики
│       └── helpers/
│           ├── statuses.py       # CellState, ShipState, GameState
│           ├── default_settings.py
│           └── exceptions.py     # ShipPlacementError и наследники
├── view/
│   ├── App.py                    # Точка входа GUI
│   ├── main.py                   # Запуск приложения
│   ├── components/
│   │   ├── MainWindow.py         # Главное меню
│   │   ├── GameWindow.py         # Окно игры
│   │   ├── BoardWidget.py        # Отрисовка поля (QPainter)
│   │   ├── SettingsWindow.py     # Окно настроек
│   │   └── LeaderboardWindow.py  # Таблица результатов
│   └── src/
│       ├── MainWindow_ui.py      # Сгенерировано из Qt Designer
│       ├── GameWindow_ui.py
│       └── SettingsWindow_ui.py
├── tests/                        # Юнит-тесты
├── settings.json                 # Настройки игры
├── game_results.json             # Результаты игр
├── requirements.txt
└── run_tests.py
```

## Архитектура

Проект построен по паттерну **MVC** (Model-View-Controller):

- **Model** — игровая логика (Game, Board, Ship, Cell, Config, AI, GameResult)
- **View** — графический интерфейс (PyQt6): главное меню, окно игры, настройки, таблица лидеров
- **Controller** — связывает Model и View, обрабатывает действия пользователя

View не знает о Model напрямую. Controller получает данные из View через сигналы и передаёт их в Model.

## Настройки

Файл `settings.json` создаётся автоматически при первом запуске. Параметры:

| Параметр        | Описание                         | По умолчанию           |
|-----------------|----------------------------------|------------------------|
| `size`          | Размер поля                      | `"10x10"`              |
| `AI_difficulty` | Сложность ИИ (0/1/2)            | `0`                    |
| `player`        | Имя игрока                       | `"Player"`             |
| `ship_sizes`    | Размеры и количество кораблей    | `{1:4, 2:3, 3:2, 4:1}`|

