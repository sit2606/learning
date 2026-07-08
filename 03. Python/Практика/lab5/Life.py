def generate_field(x,y,step,manual = False):
    """
    Генерирует игровое поле заданного размера.

    Аргументы:
        x: Ширина поля в пикселях.
        y: Высота поля в пикселях.
        step: Шаг сетки.
        manual: Флаг ручной инициализации (по умолчанию False). Если True, добавляет предустановленный паттерн.

    Возвращает:
        dict: Словарь, представляющий игровое поле, где ключи - кортежи координат, а значения - объекты cell_info.
    """
    from CellInfo import cell_info
    x = int(x/step)
    y = int(y/step)
    game_field = dict()
    for i in range (0,x,1):
        for a in range(0,y,1):
            game_field.update({(i,a):cell_info(False)})
    if(manual):
        game_field.update({(1,3):cell_info(True)})
        game_field.update({(2,3):cell_info(True)})
        game_field.update({(3,3):cell_info(True)})
        game_field.update({(3,2):cell_info(True)})
        game_field.update({(2,1):cell_info(True)})
    return(game_field)

def populate_field(field_to_populate):
    """
    Случайным образом заполняет игровое поле живыми клетками.

    Аргументы:
        field_to_populate: Исходное игровое поле (словарь).
        
    Возвращает:
        dict: Новое игровое поле со случайно добавленными живыми клетками.
    """
    import copy
    from random import randrange
    from CellInfo import cell_info
    _field_to_populate = copy.deepcopy(field_to_populate)
    last_item = next(reversed(_field_to_populate.items())) 
    y = last_item[0][1]
    x = last_item[0][0]
    random_cell_number = randrange(1, x+y)
    for cell in range(0,random_cell_number,1):
        is_place_vacant = True
        while(is_place_vacant):
            x_coord = randrange(0, x)
            y_coord = randrange(0, y)
            if (_field_to_populate.get((x_coord,y_coord))._status == False):
                    _field_to_populate.update({(x_coord,y_coord):cell_info(True)})
                    is_place_vacant = False
    return(_field_to_populate)

def populate_field_by_config(field_to_populate, STARTING_FIELD):
    import copy
    from CellInfo import cell_info
    _field_to_populate = copy.deepcopy(field_to_populate)
    for coord in STARTING_FIELD:
        _field_to_populate.update({coord[0]:cell_info(True, age=coord[1])})
    return(_field_to_populate)
def check_for_neighbours(field):
    """
    Подсчитывает количество живых соседей для каждой клетки на поле.

    Аргументы:
        field: Игровое поле (словарь).
        
    Возвращает:
        dict: Обновленное игровое поле, где у каждой клетки установлен атрибут _alive_neighbours.
    """
    import copy
    last_item = next(reversed(field.items())) 
    y = last_item[0][1] + 1
    x = last_item[0][0] + 1
    working_field = copy.deepcopy(field)
    for y_coord in range(0,y,1):
        for x_coord in range(0,x, 1):
            current_cell = working_field.get((x_coord,y_coord))
            alive_cels_around = 0
            #00
            if working_field.get((x_coord-1,y_coord-1)) != None:
                if working_field.get((x_coord-1,y_coord-1))._status == True:
                    alive_cels_around += 1
            #01
            if working_field.get((x_coord-1,y_coord)) != None:
                if working_field.get((x_coord-1,y_coord))._status == True:
                    alive_cels_around += 1
            #02
            if working_field.get((x_coord-1,y_coord+1)) != None:
                if working_field.get((x_coord-1,y_coord+1))._status == True:
                    alive_cels_around += 1
            #10
            if working_field.get((x_coord,y_coord - 1)) != None:
                if working_field.get((x_coord,y_coord - 1))._status == True:
                    alive_cels_around += 1
            #12
            if working_field.get((x_coord,y_coord + 1)) != None:
                if working_field.get((x_coord,y_coord + 1))._status == True:
                    alive_cels_around += 1
            #20
            if working_field.get((x_coord+1,y_coord-1)) != None:
                if working_field.get((x_coord+1,y_coord-1))._status == True:
                    alive_cels_around += 1
            #21
            if working_field.get((x_coord+1,y_coord)) != None:
                if working_field.get((x_coord+1,y_coord))._status == True:
                    alive_cels_around += 1
            #22
            if working_field.get((x_coord+1,y_coord+1)) != None:
                if  working_field.get((x_coord+1,y_coord+1))._status == True:
                    alive_cels_around += 1
            current_cell._alive_neighbours = alive_cels_around
            working_field.update({(x_coord,y_coord):current_cell})
    return(working_field)
def apply_rules(field):
    """
    Применяет правила игры «Жизнь» Конвея к игровому полю.

    Правила:
    - Мертвая клетка с ровно 3 живыми соседями оживает.
    - Живая клетка с 2 или 3 живыми соседями выживает.
    - В остальных случаях клетка умирает (от одиночества или перенаселения).

    Аргументы:
        field: Игровое поле (словарь) с уже подсчитанными соседями.
        
    Возвращает:
        dict: Новое состояние игрового поля после применения правил.
    """
    import copy
    import CellInfo
    last_item = next(reversed(field.items())) 
    y = last_item[0][1] + 1
    x = last_item[0][0] + 1
    working_field = copy.deepcopy(field)
    for y_coord in range(0,y,1):
        for x_coord in range(0,x, 1):
            if working_field.get((x_coord,y_coord))._alive_neighbours == 3 and  working_field.get((x_coord,y_coord))._status == False:
                new_cell = CellInfo.cell_info(True, age=1)
                working_field.update({(x_coord,y_coord):new_cell})
                continue
            if (working_field.get((x_coord,y_coord))._alive_neighbours > 3 or working_field.get((x_coord,y_coord))._alive_neighbours < 2) and  working_field.get((x_coord,y_coord))._status == True:
                new_cell = CellInfo.cell_info(False)
                working_field.update({(x_coord,y_coord):new_cell})
            elif working_field.get((x_coord,y_coord))._status == True:
                current = working_field.get((x_coord,y_coord))
                current._age += 1
                working_field.update({(x_coord,y_coord):current})
    return(working_field)
    