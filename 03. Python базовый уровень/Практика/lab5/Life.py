def generate_field(x,y,step,manual = False):
    from CellInfo import cell_info
    x = int(x/step)
    y = int(y/step)
    game_field = dict()
    for i in range (0,x,1):
        for a in range(0,y,1):
            game_field.update({(i,a):cell_info(False)})
    if(manual):
        game_field.update({(1,1):cell_info(True)})
        game_field.update({(0,4):cell_info(True)})
        game_field.update({(0,3):cell_info(True)})
        game_field.update({(1,3):cell_info(True)})
        game_field.update({(1,4):cell_info(True)})
    return(game_field)
def populate_field(field_to_populate):
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

def check_for_neighbours(field):
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
    import copy
    import CellInfo
    last_item = next(reversed(field.items())) 
    y = last_item[0][1] + 1
    x = last_item[0][0] + 1
    working_field = copy.deepcopy(field)
    for y_coord in range(0,y,1):
        for x_coord in range(0,x, 1):
            if working_field.get((x_coord,y_coord))._alive_neighbours == 3 and  working_field.get((x_coord,y_coord))._status == False:
                new_cell = CellInfo.cell_info(True)
                working_field.update({(x_coord,y_coord):new_cell})
            if working_field.get((x_coord,y_coord))._alive_neighbours > 3 or working_field.get((x_coord,y_coord))._alive_neighbours < 2 and  working_field.get((x_coord,y_coord))._status == True:
                new_cell = CellInfo.cell_info(False)
                working_field.update({(x_coord,y_coord):new_cell})
    return(working_field)
    