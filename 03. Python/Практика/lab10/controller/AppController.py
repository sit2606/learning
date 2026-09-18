from model.entities.Cell import Cell
from model.entities.Game import Game
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState, GameState
from model.entities.helpers.exceptions import (
    ShipPlacementError, OutOfBoundsError, CellOccupiedError,
    NeighborError, SizeLimitError
)
from model.GameResult import GameResult
from view.components.GameWindow import GameWindow
from PyQt6.QtWidgets import QMessageBox


class AppController:
    """Контроллер приложения.

    Связывает Model (Game) и View (MainWindow, GameWindow).
    Обрабатывает действия пользователя: расстановку кораблей и выстрелы.

    Атрибуты:
        game (Game): игровая логика (Model)
        view (MainWindow): главное меню (View)
        game_window (GameWindow): окно игры (View)
        game_result (GameResult): результаты игр
        first_click (Cell | None): первый клик при расстановке корабля
    """

    def __init__(self, game: Game, view, game_result: GameResult):
        """Инициализирует контроллер и подключает сигналы View.

        Args:
            game: экземпляр Game (Model)
            view: экземпляр MainWindow (View)
            game_result: экземпляр GameResult
        """
        self.game = game
        self.view = view
        self.game_result = game_result
        self.view.new_game_clicked.connect(self.new_game)
        self.game_window = GameWindow()
        self.game_window.player_board_clicked.connect(self.on_player_board_clicked)
        self.game_window.enemy_board_clicked.connect(self.on_enemy_board_clicked)
        self.game_window.switch_mode_clicked.connect(self.dev_switch_mode)
        self.game_window.command_button_clicked.connect(self.on_start_game)
        self.first_click = None

    def new_game(self):
        """Показывает окно игры при нажатии 'New Game'."""
        self.game.ai.populate_board(self.game.board2)
        self._update_information()
        self.game_window.show()

    def on_start_game(self):
        """Начинает игру после расстановки кораблей."""
        self.game.start_game()
        self.game_window.hide_command_button()
        self.game_window.set_status_text("Ваш ход! Стреляйте по полю противника.")
        self.game_window.set_information_text("Игра началась!")

    def on_player_board_clicked(self, row, col):
        """Обрабатывает клик по доске игрока (SETUP — расстановка)."""
        match self.game.state:
            case GameState.SETUP:
                self._handle_placement(row, col)

    def on_enemy_board_clicked(self, row, col):
        """Обрабатывает клик по доске противника (PLAYER_TURN — выстрел)."""
        match self.game.state:
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
            self.game_window.PlayerBoard.grid[row][col] = 4
        else:
            second_click = Cell(col, row, CellState.FILL)
            ship = Ship(self.first_click, second_click)
            try:
                self.game.place_ship(ship)
                self.first_click = None
                for cell in ship.get_cells():
                    self.game_window.PlayerBoard.grid[cell.y][cell.x] = 5
                self._update_information()
            except SizeLimitError as e:
                self.game_window.PlayerBoard.grid[self.first_click.y][self.first_click.x] = 0
                self.first_click = None
                QMessageBox.warning(self.view, "Ошибка", str(e))
            except OutOfBoundsError as e:
                self.game_window.PlayerBoard.grid[self.first_click.y][self.first_click.x] = 0
                self.first_click = None
                QMessageBox.warning(self.view, "Ошибка", str(e))
            except CellOccupiedError as e:
                self.game_window.PlayerBoard.grid[self.first_click.y][self.first_click.x] = 0
                self.first_click = None
                QMessageBox.warning(self.view, "Ошибка", str(e))
            except NeighborError as e:
                self.game_window.PlayerBoard.grid[self.first_click.y][self.first_click.x] = 0
                self.first_click = None
                QMessageBox.warning(self.view, "Ошибка", str(e))
        self.game_window.PlayerBoard.update()


    def _check_player_ship_placed(self):
        return all(v == 0 for v in self.game.board1.get_remaining_ships().values())

    def _update_information(self):
        """Обновляет InformationBrowser с оставшимися кораблями."""
        remaining = self.game.board1.get_remaining_ships()
        lines = ["Осталось расставить:"]
        for size in sorted(remaining.keys(), reverse=True):
            count = remaining[size]
            if count > 0:
                lines.append(f"  {size}-палубных: {count}")
        if all(v == 0 for v in remaining.values()):
            lines.append("  Все расставлены!")
            self.game_window.enable_command_button()
        self.game_window.set_information_text("\n".join(lines))

    def dev_switch_mode(self):
        """Переключает режим SETUP ↔ PLAYER_TURN для отладки."""
        if self.game.state == GameState.SETUP:
            self.game.state = GameState.PLAYER_TURN
            self.game_window.set_status_text("Режим: бой")
        elif self.game.state == GameState.PLAYER_TURN:
            self.game.state = GameState.SETUP
            self.game_window.set_status_text("Режим: расстановка")

    def _handle_shot(self, row, col):
        """Обрабатывает выстрел игрока и ход компьютера.

        Args:
            row: строка выстрела
            col: столбец выстрела
        """
        # Выстрел игрока (current=board1, opponent=board2)
        result = self.game.make_shot(col, row)
        if result == CellState.HIT:
            self.game_window.EnemyBoard.grid[row][col] = 2
        elif result == CellState.MISS:
            self.game_window.EnemyBoard.grid[row][col] = 3
        self.game_window.EnemyBoard.update()

        if self.game.is_game_over():
            self._end_game()
            return

        # Смена хода → current=board2, opponent=board1
        self.game.switch_turn()

        # Ход компьютера (opponent=board1)
        ai_choice = self.game.ai.choose_cell(self.game._get_opponent_board())
        if ai_choice is None:
            return
        ai_x, ai_y = ai_choice
        ai_result = self.game.make_shot(ai_x, ai_y)
        if ai_result == CellState.HIT:
            self.game_window.PlayerBoard.grid[ai_y][ai_x] = 2
        elif ai_result == CellState.MISS:
            self.game_window.PlayerBoard.grid[ai_y][ai_x] = 3
        self.game_window.PlayerBoard.update()

        # Смена хода обратно → current=board1
        self.game.switch_turn()

        if self.game.is_game_over():
            self._end_game()

    def _end_game(self):
        """Показывает результат игры и сохраняет его."""
        winner = self.game.get_winner()
        loser = self.game.player2.name if winner == self.game.player1.name else self.game.player1.name
        self.game.state = GameState.GAME_OVER
        self.game_result.record(winner, loser)
        self.game_result.save_to_json()
        self.game_window.set_status_text(f"Игра окончена! Победитель: {winner}")
        QMessageBox.information(self.view, "Конец игры", f"Победил: {winner}")
