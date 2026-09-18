from model.entities.Cell import Cell
from model.entities.Game import Game
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState, GameState
from view.components.GameWindow import GameWindow


class AppController:
    """Контроллер приложения.

    Связывает Model (Game) и View (MainWindow, GameWindow).
    Обрабатывает действия пользователя: расстановку кораблей и выстрелы.

    Атрибуты:
        game (Game): игровая логика (Model)
        view (MainWindow): главное меню (View)
        game_window (GameWindow): окно игры (View)
        first_click (Cell | None): первый клик при расстановке корабля
    """

    def __init__(self, game: Game, view):
        """Инициализирует контроллер и подключает сигналы View.

        Args:
            game: экземпляр Game (Model)
            view: экземпляр MainWindow (View)
        """
        self.game = game
        self.view = view
        self.view.new_game_clicked.connect(self.new_game)
        self.game_window = GameWindow()
        self.game_window.cell_clicked.connect(self.on_cell_clicked)
        self.first_click = None

    def new_game(self):
        """Показывает окно игры при нажатии 'New Game'."""
        self.game.ai.populate_board(self.game.board2)
        self.game_window.show()

    def on_cell_clicked(self, row, col):
        """Обрабатывает клик по клетке в зависимости от состояния игры.

        Args:
            row: строка (координата y)
            col: столбец (координата x)
        """
        match self.game.state:
            case GameState.SETUP:
                self._handle_placement(row, col)
            case GameState.PLAYER_TURN:
                self._handle_shot(row, col)

    def _handle_placement(self, row, col):
        """Обрабатывает расстановку корабля (два клика).

        Первый клик — запоминает начало корабля (подсветка).
        Второй клик — создаёт корабль, проверяет и размещает.

        Args:
            row: строка клика
            col: столбец клика
        """
        if self.first_click is None:
            self.first_click = Cell(col, row, CellState.FILL)
            self.game_window.BoardWidget.grid[row][col] = 4
        else:
            second_click = Cell(col, row, CellState.FILL)
            ship = Ship(self.first_click, second_click)
            if self.game.place_ship(ship):
                self.first_click = None
                for cell in ship.get_cells():
                    self.game_window.BoardWidget.grid[cell.y][cell.x] = 5
            else:
                from PyQt6.QtWidgets import QMessageBox
                self.first_click = None
                QMessageBox.warning(self.view, "Ошибка", "Нельзя разместить корабль здесь")
        self.game_window.BoardWidget.update()


    def _check_player_ship_placed(self):
        return all(v == 0 for v in self.game.board1.get_remaining_ships().values())

    def _handle_shot(self, row, col):
        """Обрабатывает выстрел игрока.

        Вызывает game.make_shot, обновляет цвет клетки на доске.

        Args:
            row: строка выстрела
            col: столбец выстрела
        """
        result = self.game.make_shot(col, row)
        if result == CellState.HIT:
            self.game_window.BoardWidget.grid[row][col] = 2
        elif result == CellState.MISS:
            self.game_window.BoardWidget.grid[row][col] = 3
        self.game_window.BoardWidget.update()
