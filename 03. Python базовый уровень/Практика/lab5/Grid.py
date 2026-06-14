from PIL import Image, ImageDraw,ImageOps, ImageFont

class grid:
    """
    Класс, представляющий сетку.
    
    Атрибуты:
        _width: Ширина сетки.
        _length: Длина сетки.
        _step: Шаг сетки.
        _image: Объект изображения (PIL.Image), связанный с сеткой.
    """
    def __init__(self, width, length, gridStep, image):
        """
        Инициализирует объект сетки заданными параметрами.
        """
        self._width = width
        self._length = length
        self._step = gridStep
        self._image = image
class field:    
    """
    Класс, представляющий поле для отрисовки сетки.
    
    Атрибуты:
        _input_length: Входная длина поля.
        _input_width: Входная ширина поля.
        _input_step: Входной шаг сетки.
    """
    def __init__(self,input_length,input_width,input_step):
        """
        Инициализирует объект поля заданными параметрами.
        """
        self._input_length = input_length
        self._input_width = input_width
        self._input_step = input_step
        pass
    def draw_grid(self):
        """
        Отрисовывает сетку на новом изображении.
        
        Проверяет, делятся ли длина и ширина нацело на шаг сетки. 
        Если нет, выводит сообщение об ошибке и возвращает None.
        В противном случае создает новое изображение, рисует линии сетки, 
        добавляет черную рамку и возвращает объект класса grid.
        
        Возвращает:
            grid: Объект сетки с отрисованным изображением, или None в случае ошибки.
        """
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
    """
    Добавляет координатные метки к изображению сетки.
    
    Аргументы:
        im: Исходное изображение.
        border_width: Ширина границы для размещения текста.
        input_length: Длина поля.
        input_width: Ширина поля.
        input_step: Шаг сетки для расчета координат.
        
    Возвращает:
        Изображение с добавленными координатными метками.
    """
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
def draw_by_dictionary(input_step,field,image_to_draw):
    """
    Отрисовывает элементы на изображении на основе словаря состояний.
    
    Аргументы:
        input_step: Шаг сетки.
        field: Словарь, где ключи - кортежи координат (x, y), 
               а значения - объекты с атрибутом _status.
        image_to_draw: Изображение, на котором производится отрисовка.
    """
    last_item = next(reversed(field.items())) 
    y = last_item[0][1]
    x = last_item[0][0]
    for y_coord in range(0,y+1,1):
        for x_coord in range(0,x+1, 1):
            if field.get((int(x_coord),int(y_coord)))._status == True: 
                draw_by_index(x_coord, y_coord, image_to_draw, input_step)
def draw_by_index(first_index,second_index,image,step):
    """
    Отрисовывает зеленый прямоугольник по заданным индексам сетки.
    
    Аргументы:
        first_index: Индекс по оси X.
        second_index: Индекс по оси Y.
        image: Изображение для отрисовки.
        step: Шаг сетки.
        
    Возвращает:
        None, если индексы выходят за пределы сетки.
    """
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
    """
    Отображает изображение на экране.
    
    Аргументы:
        im: Объект изображения для отображения.
    """
    if im != None:
        im.show()