import Grid
import Life
input_length = 100
input_width = 100
input_step = 20
x = Grid.draw_grid(input_length,input_width,5,input_step)
field = Life.generate_field(input_length,input_width,input_step)
Grid.draw_by_array(input_step,field,x.get('image'))
z = Grid.draw_coordinates(x.get('image'), 20, input_length, input_width, input_step)
Grid.showGrid(z)
Life.imitate_life(10,field,z)

print('s')
