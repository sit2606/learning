"""
geoLib — библиотека для работы с геоданными и расчёта дистанций.

Модуль содержит функции для:
- Расчёта дистанции между двумя координатами (формула Хаверсина)
- Фильтрации рынков по расстоянию от пользователя

Зависимости:
- math: стандартная библиотека для тригонометрических функций

Использование:
    from BusinessLogic.geoLib import haversine, get_distance
"""
import math



def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Вычисляет геодезическое расстояние между двумя точками на поверхности Земли.

    Использует формулу гаверсинусов для расчёта расстояния по большой окружности.

    Args:
        lat1: Широта первой точки в градусах.
        lon1: Долгота первой точки в градусах.
        lat2: Широта второй точки в градусах.
        lon2: Долгота второй точки в градусах.

    Returns:
        Расстояние между точками в километрах.

    Examples:
        >>> round(haversine(40.7128, -74.0060, 34.0522, -118.2437), 2)
        3935.75
        >>> round(haversine(51.5074, -0.1278, 48.8566, 2.3522), 2)
        343.56
        >>> haversine(0.0, 0.0, 0.0, 0.0)
        0.0
    """
    R = 6371.0

    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2
         + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2)

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
def get_distance(coords, market_base):
    """
    Рассчитывает расстояние от пользователя до каждого рынка.

    Добавляет поле 'distance' (км) в каждый словарь рынка.

    Args:
        user: Словарь пользователя с полями latitude, longitude.
        market_base: Словарь рынков {id: {атрибуты, latitude, longitude}}.

    Returns:
        dict: market_base с добавленным полем 'distance' для каждого рынка,
              или None при ошибке.
    """
    user_loc = dict()
    user_loc['latitude'] = float(coords['latitude'])
    user_loc['longitude'] = float(coords['longitude'])
    try:
        for key,market in market_base.items():

            distance = haversine(user_loc['latitude'],user_loc['longitude'],float(market['latitude']),
                             float(market['longitude']))
            market_base[key].update({'distance':distance})
        return market_base
    except Exception as e:
            print(e)
def get_zip_coords(postalcode):
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="my-app/1.0")
    location = geolocator.geocode({"postalcode": postalcode, "country": "US"})
    if location:
        return location.latitude, location.longitude
    else:
        return None
