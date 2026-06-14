def generate_field(x,y,step):
    game_field = [[i!=i for i in range(0,x,step)] for _ in range(0,y,step)]
    game_field[0][0] = False
    game_field[0][1] = False
    game_field[0][2] = False
    game_field[0][3] = False
    game_field[0][4] = False
    game_field[1][0] = False
    game_field[1][1] = False
    game_field[1][2] = False
    game_field[1][3] = False
    game_field[1][4] = False
    game_field[2][0] = False
    game_field[2][1] = False
    game_field[2][2] = False
    game_field[2][3] = False
    game_field[2][4] = False
    game_field[3][0] = False
    game_field[3][1] = False
    game_field[3][2] = True
    game_field[3][3] = True
    game_field[3][4] = True
    game_field[4][0] = False
    game_field[4][1] = False
    game_field[4][2] = False
    game_field[4][3] = False
    game_field[4][4] = False
    return(game_field)
def imitate_life(generation_count, field, g):
    import Grid
    x = len(field[0]) - 1
    y = len(field)  - 1
    for i in range (0,generation_count, 1):
        for index2 in range(y,-1,-1):
            for index1 in range(x,-1, -1):
                alive_cels_around = 0
                d1 = x-index1
                d2 = y-index2
                if d1 == 4 and d2 == 3:
                    print('s')
                if field[d1-1][d2-1] == True:
                    alive_cels_around += 1
                #01
                if field[d1-1][d2] == True:
                    alive_cels_around += 1
                #02
                if field[d1-1][d2+1] == True:
                    alive_cels_around += 1
                #10
                if field[d1][d2-1] == True:
                    alive_cels_around += 1
                #12
                if field[d1][d2+1] == True:
                    alive_cels_around += 1
                #20
                if field[d1+1][d2-1] == True:
                    alive_cels_around += 1
                #21
                if field[d1+1][d2] == True:
                    alive_cels_around += 1
                #22
                if field[d1+1][d2+1] == True:
                    alive_cels_around += 1
                if (field[d1][d2] == True and alive_cels_around > 3) or (field[d1][d2] == True and alive_cels_around < 2):
                    field[d1][d2] = False
                if field[d1][d2] == False and alive_cels_around == 3:
                    field[d1][d2] = True
        Grid.draw_by_array(20,field,g)
        Grid.showGrid(g)   
    print('s')
        