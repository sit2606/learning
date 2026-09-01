# Контракты классов (Model)

## Перечисления (statuses.py)

```python
class CellState(Enum):
    FILL, EMPTY, HIT, MISS

class ShipState(Enum):
    FULL, WOUNDED, KILLED

class ShotState(Enum):
    MISS, HIT, SUNK

class GameState(Enum):
    SETUP, PLAYER_TURN, COMPUTER_TURN, GAME_OVER
```

---

## Cell

```python
class Cell:
    def __init__(self, x: int, y: int, state: CellState)
    def get_coords(self) -> tuple[int, int]
    def set_state(self, state: CellState)
    def get_state(self) -> CellState
```

---

## Ship

```python
class Ship:
    def __init__(self)
    def set_cells(self, cells: list[Cell])
    def get_cells(self) -> list[Cell]
    def get_length(self) -> int
    def get_state(self) -> ShipState
```

---

## Board

```python
class Board:
    def __init__(self, settings: Config)
    def place_ship(self, ship: Ship)
    def validate_ship_position(self, ship: Ship)
    def shot(self, x: int, y: int) -> ShotState
    def get_ships_state(self)
```

---

## Player

```python
class Player:
    def __init__(self, name: str)
    def win(self)
    def lose(self)
    def get_stats(self) -> tuple[int, int]  # (wins, losses)
```

---

## Config

```python
class Config:
    def __init__(self)
    # Поля: size, ships_count, AI_difficulty
    def read_from_json(self, json_file: str)
    def write_to_json(self, json_file: str)
```

---

## Game

```python
class Game:
    def __init__(self, config: Config)

    # Состояние игры
    def get_state(self) -> GameState
    def switch_turn(self)
    def is_game_over(self) -> bool

    # Расстановка кораблей (SETUP)
    def place_ship(self, ship: Ship) -> bool
    def can_place_ship(self, ship: Ship) -> bool
    def start_game(self)

    # Игровой цикл
    def make_shot(self, x: int, y: int) -> ShotState
    def get_winner(self) -> str
```

---

## GameResult (не реализован)

```python
class GameResult:
    def __init__(self)
    def record(self, winner: Player, loser: Player)
    def get_results(self) -> list
    def save_to_json(self, json_file: str)
    def load_from_json(self, json_file: str)
```
