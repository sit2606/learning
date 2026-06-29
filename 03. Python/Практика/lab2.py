import math


def get_values():

    d1 = float(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => \n"))
    d2 = float(input("Введите кратчайшее расстояние между утопающего до берега, d2 (футы) => \n")) 
    h = float(input("Введите боковое смещение между спасателем и утопающим, h (ярды) => \n")) 
    v_sand = float(input("Введите  скорость двежения спасателя по песку, v_sand (мили в час) => \n")) 
    n = float(input("Введите  коэффициент замедления спасателя при движении в воде, n  => \n")) 
    theta1 = float(input("Введите  направление движения спасателя по песку, theta1 (градусы)  => \n")) 
    return(d1,d2,h,v_sand,n,theta1)

def convert(d1,h,v_sand,theta1):
    """
    Приводит единицы измерения  к 
    - Футам (для расстояний), 
    - Футам в секунду (для скоростей)
    - радианам (для углов)
    
    >>> # Тест 1: Типичные значения (угол 30 градусов)
    >>> # d1=5 ярдов, h=10 ярдов, v_sand=6 мил/ч, theta1=30
    >>> convert(5, 10, 6, 30) # doctest: +ELLIPSIS
    (15, 30, 8.8, 0.523598...)
    
    >>> # Тест 2: Типичные значения (угол 45)
    >>> # d1=10 ярдов, h=10 ярдов, v_sand=3 мил/ч, theta1=45
    >>> convert(10, 10, 3, 45) # doctest: +ELLIPSIS
    (30, 30, 4.4, 0.78539...)

    >>> # Тест 3: Граничные значения (нулевые расстояния, угол 180 градусов)
    >>> # d1=0 ярдов, h=00 ярдов, v_sand=1.5 мил/ч, theta1=180
    >>> convert(0, 0, 1.5, 180) # doctest: +ELLIPSIS
    (0, 0, 2.2, 3.141592...)
    """
    d1 = d1 * 3
    h = h * 3
    v_sand = v_sand*5280 /3600 
    theta1 = math.radians(theta1)
    return(d1,h,v_sand,theta1)

def calculate(d1,theta1_rad,h,d2,v_sand,n):
    """
    Рассчитывает время достижения утопающего в секундах.
    На вход должны поступать расстояния в футах
    Скорость в футах в секунду
    Градусы в радианах
    
    >>> # Тест 1: Угол 30 градусов 
    >>> # d1=15 футов, h=30 футов, d2=15 футов, v_sand=8.8 фут/с, n=1.5
    >>> calculate(15, 0.5235987755982988, 30, 15, 8.8, 1.5) # doctest: +ELLIPSIS
    6.41440...
    >>> # Тест 2: Угол 45 градусов 
    >>> # d1=30 футов, h=60 футов, d2=10 футов, v_sand=4.4 фут/с, n=2.0
    >>> calculate(30, 0.7853981633974483, 60, 10, 4.4, 2.0) # doctest: +ELLIPSIS
    24.01635...
    """
    x = d1 * math.tan(theta1_rad)
    L1 = math.sqrt(math.pow(x,2) + math.pow(d1,2))

    L2 = math.sqrt(math.pow((h-x),2) + math.pow(d2,2))
    t = 1/v_sand * (L1 + n * L2)
    return(t)
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    
    # d1, d2, h, v_sand, n, theta1 = get_values()
    # d1_ft, h_ft, v_sand, theta1_rad = convert(d1, h, v_sand, theta1)
    # result = calculate(d1_ft, theta1_rad, h_ft, d2, v_sand, n)
    # print(f"Если спасатель начнёт движение под углом theta1, равным {int(round(theta1))} градусам, он достигнет утопающего через {result:.1f} секунды")
