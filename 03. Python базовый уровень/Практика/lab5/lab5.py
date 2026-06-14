from Grid import field,draw_by_dictionary,draw_coordinates,showGrid
import Life 
input_length = 100
input_width = 100
input_step = 20
generation_count = 10
manual_mode = True
graphic = field(input_length, input_width ,  input_step).draw_grid()
game_field = Life.generate_field(input_length,input_width,input_step, manual_mode)
if (not manual_mode):
    populated_field = Life.populate_field(game_field)
else:
    populated_field = game_field
draw_by_dictionary(input_step,populated_field,graphic._image)
z2 = draw_coordinates(graphic._image, 20, input_length, input_width, input_step)
showGrid(z2)
for i in range(1,generation_count,1):
    sim_field = Life.check_for_neighbours(populated_field)
    sim_field = Life.apply_rules(sim_field)
    draw_by_dictionary(input_step,sim_field,graphic._image)
    z2 = draw_coordinates(graphic._image, 20, input_length, input_width, input_step)
    showGrid(z2)
print('s')