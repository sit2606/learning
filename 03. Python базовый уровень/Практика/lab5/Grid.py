from PIL import Image, ImageDraw,ImageOps, ImageFont
from GridElement import grid_element

class grid:
    def __init__(self, width, length, gridStep, image):
        self._width = width
        self._length = length
        self._step = gridStep
        self._image = image
class field:
    def __init__(self,input_length,input_width,input_step):
        self._input_length = input_length
        self._input_width = input_width
        self._input_step = input_step
        pass
    def draw_grid(self):
        _grid_step = self._input_step
        x = self._input_length
        y = self._input_width
        b = 5
        if (y%_grid_step != 0) or (x%_grid_step!= 0) :
            print('Невозможно разбить сетку по этому шагу')
            print('Укажите шаг, который нацело делится и на ')
            print('длину и на ширину ')
            return(None)
        im = Image.new('RGBA', (x, y), color="White") 
        draw = ImageDraw.Draw(im)
        for z in range(0, x + b, _grid_step):
            draw.line((0,z , x+b*2, z), width= 1, fill="Black")
            draw.line((z,0 , z, y+b*2), width= 1, fill="Black")
        new_img = ImageOps.expand(im, border=b, fill="black")
        result = grid(x,y,_grid_step,new_img)
        return(result)



def draw_coordinates(im, border_width,input_length, input_width, input_step):

    new_img = ImageOps.expand(im, border=border_width, fill="white")
    try:
        font = ImageFont.truetype("arial.ttf", size=border_width)
    except IOError:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(new_img)
    for x in range (0,input_length, input_step):
        draw.text((x + 27,0), str(int(x/input_step)), fill="black", font=font)
    for y in range (0,input_width, input_step):
        draw.text((0,y + 25), str(int(y/input_step)), fill="black", font=font)
    return(new_img)
def draw_by_array(input_step,field,image_to_draw):
    import Grid
    y = len(field)
    x = len(field[0])
    for y_coord in range(0,y,1):
        for x_coord in range(0,x, 1):
            if field[int(y_coord)][int(x_coord)]._status == True:
                Grid.draw_by_index(x_coord, y_coord, image_to_draw, input_step)
def draw_by_index(first_index,second_index,image,step):
    draw = ImageDraw.Draw(image)
    width,height = image.size
    _n1 = first_index
    _n2 = second_index
    _step = step
    if (width - _n1*_step)<0 or (height-_n2*_step)<0:
        print('Таких индексов нет в сетке')
        return(None)
    draw.rectangle((0+5+_step*_n1,0+5+_step*_n2, _n1*_step+_step+5,_step+5+_step*_n2), fill="Green")
def showGrid(im):
    if im != None:
        im.show()