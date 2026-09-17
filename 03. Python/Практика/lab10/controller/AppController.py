from model.entities.Cell import Cell
from model.entities.Game import Game
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState, GameState
from view.components.GameWindow import GameWindow


class AppController:
    def __init__(self, game: Game, view):
        self.game = game
        self.view = view
        self.view.new_game_clicked.connect(self.new_game)
        self.game_window = GameWindow()
        self.game_window.cell_clicked.connect(self.on_cell_clicked)
        self.first_click = None
    def new_game(self):
        self.game_window.show()
    def on_cell_clicked(self, row, col):
        match self.game.state:
            case GameState.SETUP:
                self._handle_placement(row, col)
            case GameState.PLAYER_TURN:
                self._handle_shot(row, col)
    def _check_grid(self, row, col):
        game
    def _handle_placement(self, row, col):
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

    def _handle_shot(self, row, col):
        result = self.game.make_shot(col, row)
        if result == CellState.HIT:
            self.game_window.BoardWidget.grid[row][col] = 2
        elif result == CellState.MISS:
            self.game_window.BoardWidget.grid[row][col] = 3
        self.game_window.BoardWidget.update()
