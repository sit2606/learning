
from Grid import field,draw_by_array,draw_coordinates,showGrid
import Life
input_length = 100
input_width = 100
input_step = 20


game_field = field(input_length, input_width ,  input_step).draw_grid()
field = Life.generate_field(input_length,input_width,input_step)
draw_by_array(input_step,field,game_field._image)
z = draw_coordinates(game_field._image, 20, input_length, input_width, input_step)
showGrid(z)
Life.imitate_life(10,field,z)

print('s')