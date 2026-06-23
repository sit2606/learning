import math


def km_to_miles(km: float) -> float:
    """
    Преобразует километры в мили.
    
    Args:
        km: Расстояние в километрах.
    
    Returns:
        Расстояние в милях.
    
    Examples:
        >>> round(km_to_miles(1), 2)
        0.62
        >>> round(km_to_miles(324.0), 2)
        201.32
    """
    return km * 0.621371


def decimal_to_dms(decimal: float, is_lat: bool = True) -> str:
    """
    Преобразует десятичные градусы в формат DMS (градусы, минуты, секунды).
    
    Args:
        decimal: Координата в десятичных градусах.
        is_lat: True для широты, False для долготы.
    
    Returns:
        Строка в формате DD°MM'SS.SS"N/S или DDD°MM'SS.SS"E/W.
    
    Examples:
        >>> decimal_to_dms(42.6737, is_lat=True) == '042°40\\'25.32"N'
        True
        >>> decimal_to_dms(-73.60879166666667, is_lat=False) == '073°36\\'31.65"W'
        True
        >>> decimal_to_dms(0.0, is_lat=True)
        '000°00\\'00.00"N'
        >>> decimal_to_dms(-90.0, is_lat=True)
        '090°00\\'00.00"S'
        >>> decimal_to_dms(180.0, is_lat=False)
        '180°00\\'00.00"E'
    """
    if is_lat:
        direction = 'N' if decimal >= 0 else 'S'
    else:
        direction = 'E' if decimal >= 0 else 'W'
    
    decimal = abs(decimal)
    degrees = int(decimal)
    minutes_decimal = (decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60
    
    return f'{degrees:03d}°{minutes:02d}\'{seconds:05.2f}"{direction}'


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)