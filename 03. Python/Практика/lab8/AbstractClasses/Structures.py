class RatNum:
    """
    Неизменяемое рациональное число.
    Поля представления:
        _num (int): числитель
        _den (int): знаменатель
    Инвариант:
        - _den >= 0
        - дробь сокращена (gcd(|_num|, _den) == 1)
        - если NaN: _num == 0 и _den == 0
    Функция абстракции:
        AF(self) = _num / _den, если _den != 0; иначе NaN
    """
    def __init__(self, numerator, denominator):

        self._num = numerator
        self._den = denominator
    def is_nan(self):
        """Проверяет, является ли число NaN.
               @requires: —
               @modifies: —
               @effects: —
               @throws: —
               @returns: True, если число NaN, иначе False.
        """
        pass
    def is_negative(self):
        """Проверяет, является ли число отрицательным
               @requires: RatNum.is_nan() == False
               @modifies: —
               @effects: —
               @throws: —
               @returns: True, если число <0, иначе False.
        """
        pass
    def is_positive(self):
        """Проверяет, является ли число положительным
               @requires: RatNum.is_nan() == False
               @modifies: —
               @effects: —
               @throws: —
               @returns: True, если число <0, иначе False.
        """
        pass
    def compare_to(self, other):
        """Сравнивает два числа
               @requires: -
               @modifies: —
               @effects: —
               @throws: —
               @returns: 1, если self > other, 0 есть self == other, -1 если self < other,
               Если self == Nan, то - NaN == NaN → 0
                                    - NaN > любое число → 1
                                    - любое число < NaN → -1
        """
        pass
    def float_value(self):
        """Приводит дробь к десятичной записи
               @requires: -
               @modifies: —
               @effects: —
               @throws: —
               @returns: 1, если self > other, 0 есть self == other, -1 если self < other,
               Если self == Nan, то - NaN == NaN → 0
                                    - NaN > любое число → 1
                                    - любое число < NaN → -1
        """
        pass
    def int_value(self):
        """Выделяет целую часть из рациональной дроби
               @requires: RatNum.is_nan() == False
               @modifies: —
               @effects: —
               @throws: —
               @returns: -
        """
        pass
    def __neg__(self):
        """Делает значение дроби отрицательной
               @requires: RatNum.is_nan() == False
               @modifies: —
               @effects: —
               @throws: —
               @returns: 1, если self > other, 0 есть self == other, -1 если self < other,
               Если self == Nan, то - NaN == NaN → 0
                                    - NaN > любое число → 1
                                    - любое число < NaN → -1
        """
        pass
    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        pass
    def __truediv__(self, other):
        pass
    def gcd(self):
        pass
    def __str__(self):
        pass
    def __hash__(self):
        pass
    def __eq__(self):
        pass
