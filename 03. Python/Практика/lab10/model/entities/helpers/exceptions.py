class ShipPlacementError(Exception):
    """Базовое исложение при размещении корабля."""
    pass


class OutOfBoundsError(ShipPlacementError):
    """Корабль выходит за пределы поля."""
    pass


class CellOccupiedError(ShipPlacementError):
    """Клетка уже занята."""
    pass


class NeighborError(ShipPlacementError):
    """Рядом уже есть корабль."""
    pass


class SizeLimitError(ShipPlacementError):
    """Все корабли такого размера уже расставлены."""
    pass
