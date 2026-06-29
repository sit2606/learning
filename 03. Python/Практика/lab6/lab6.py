import math
import zip_util
import doctest
from converters import km_to_miles, decimal_to_dms


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


def find_by_zip(data: list, zip_code: str):
    """
    Ищет запись по почтовому индексу с помощью линейного поиска.
    
    Args:
        data: Список записей о почтовых индексах.
              Каждая запись - список [zip, lat, lon, city, state, county].
        zip_code: Почтовый индекс для поиска (строка из 5 цифр).
    
    Returns:
        Запись о почтовом индексе, если найдена, иначе None.
    
    Examples:
        >>> data = [['10001', 40.7484, -73.9967, 'New York', 'NY', 'New York']]
        >>> find_by_zip(data, '10001')
        ['10001', 40.7484, -73.9967, 'New York', 'NY', 'New York']
        >>> find_by_zip(data, '99999') is None
        True
        >>> find_by_zip([], '10001') is None
        True
    """
    for row in data:
        if row[0] == zip_code:
            return row
    return None


def find_by_city_state(data: list, city: str, state: str) -> list:
    """
    Ищет все почтовые индексы для заданного города и штата.
    
    Поиск выполняется без учёта регистра символов.
    
    Args:
        data: Список записей о почтовых индексах.
              Каждая запись - список [zip, lat, lon, city, state, county].
        city: Название города для поиска.
        state: Код штата для поиска.
    
    Returns:
        Список почтовых индексов, соответствующих городу и штату.
        Если ничего не найдено, возвращает пустой список.
    
    Examples:
        >>> data = [['12179', 42.7284, -73.6918, 'Troy', 'NY', 'Rensselaer'],
        ...         ['12180', 42.7284, -73.6918, 'Troy', 'NY', 'Rensselaer'],
        ...         ['10001', 40.7484, -73.9967, 'New York', 'NY', 'New York']]
        >>> find_by_city_state(data, 'Troy', 'NY')
        ['12179', '12180']
        >>> find_by_city_state(data, 'troy', 'ny')
        ['12179', '12180']
        >>> find_by_city_state(data, 'TROY', 'NY')
        ['12179', '12180']
        >>> find_by_city_state(data, 'Boston', 'MA')
        []
        >>> find_by_city_state([], 'New York', 'NY')
        []
    """
    result = []
    city_lower = city.lower()
    state_lower = state.lower()
    for row in data:
        if row[3].lower() == city_lower and row[4].lower() == state_lower:
            result.append(row[0])
    return result


def handle_loc(data: list) -> None:
    """
    Обрабатывает команду loc: поиск информации по почтовому индексу.
    
    Запрашивает у пользователя почтовый индекс, ищет его в данных
    и выводит информацию о городе, штате, графстве и координатах.
    Если индекс не найден, выводит сообщение об ошибке.
    
    Args:
        data: Список записей о почтовых индексах.
    
    Note:
        Функция взаимодействует с пользователем через input() и print().
        Для тестирования используйте mock-объекты.
    """
    zip_code = input("Enter a ZIP Code to lookup => ").strip()

    row = find_by_zip(data, zip_code)
    if row:
        lat_dms = decimal_to_dms(row[1], is_lat=True)
        lon_dms = decimal_to_dms(row[2], is_lat=False)
        print(zip_code)
        print(f"ZIP Code {zip_code} is in {row[3]}, {row[4]}, {row[5]} county,")
        print(f"coordinates: ({lat_dms},{lon_dms})")
    else:
        print("Error: invalid or not found zip code")


def handle_zip(data: list) -> None:
    """
    Обрабатывает команду zip: поиск почтовых индексов по городу и штату.
    
    Запрашивает у пользователя название города и штата, ищет соответствующие
    почтовые индексы и выводит их. Если ничего не найдено, выводит сообщение
    об ошибке.
    
    Args:
        data: Список записей о почтовых индексах.
    
    Note:
        Функция взаимодействует с пользователем через input() и print().
        Для тестирования используйте mock-объекты.
    """
    city = input("Enter a city name to lookup => ").strip()
    print(city)
    state = input("Enter the state name to lookup => ").strip()
    print(state)

    zips = find_by_city_state(data, city, state)
    if zips:
        city_formatted = city.capitalize()
        state_formatted = state.upper()
        zips_str = ', '.join(zips)
        print(f"The following ZIP Code(s) found for {city_formatted}, {state_formatted}: {zips_str}")
    else:
        print("Error: city/state not found")


def handle_dist(data: list) -> None:
    """
    Обрабатывает команду dist: вычисление расстояния между двумя почтовыми индексами.
    
    Запрашивает у пользователя два почтовых индекса, находит их координаты
    и вычисляет геодезическое расстояние между ними в милях. 
    Если хотя бы один индекс не найден, выводит сообщение об ошибке.
    
    Args:
        data: Список записей о почтовых индексах.
    
    Note:
        Функция взаимодействует с пользователем через input() и print().
        Для тестирования используйте mock-объекты.
    """
    zip1 = input("Enter the first ZIP Code => ").strip()
    print(zip1)
    zip2 = input("Enter the second ZIP Code => ").strip()
    print(zip2)

    row1 = find_by_zip(data, zip1)
    row2 = find_by_zip(data, zip2)
    
    if row1 and row2:
        lat1, lon1 = row1[1], row1[2]
        lat2, lon2 = row2[1], row2[2]
        distance_km = haversine(lat1, lon1, lat2, lon2)
        distance_miles = km_to_miles(distance_km)
        print(f"The distance between {zip1} and {zip2} is {distance_miles:.2f} miles")
    else:
        print("Error: invalid or not found zip code")


def repl(data: list) -> None:
    """
    Основной цикл взаимодействия с пользователем (REPL).
    
    Читает команды от пользователя и выполняет соответствующие действия:
    - loc: поиск по почтовому индексу
    - zip: поиск по городу и штату
    - dist: вычисление расстояния между двумя индексами
    - end: завершение работы программы
    
    Команды регистронезависимы. Неизвестные команды игнорируются.
    
    Args:
        data: Список записей о почтовых индексах.
    
    Note:
        Функция работает в бесконечном цикле до получения команды 'end'.
        Для тестирования используйте mock-объекты.
    """
    while True:
        command = input("Command ('loc', 'zip', 'dist', 'end') => ").strip().lower()

        if command == 'end':
            print("Done")
            break
        elif command == 'loc':
            handle_loc(data)
        elif command == 'zip':
            handle_zip(data)
        elif command == 'dist':
            handle_dist(data)
        else:
            print("Invalid command, ignoring")


def main():
    """
    Точка входа в программу.
    
    Загружает данные о почтовых индексах из модуля zip_util
    и запускает интерактивный цикл REPL.
    """
    data = zip_util.read_zip_all()
    repl(data)


if __name__ == "__main__":
    # Запуск doctest для проверки примеров в документации
    doctest.testmod(verbose=True)
    # Запуск основной программы
    main()