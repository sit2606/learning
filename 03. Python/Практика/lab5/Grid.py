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
        for z in range(0, max(x, y) + b, _grid_step):
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
def draw_by_dictionary(input_step,field,image_to_draw, color='green'):
    """
    Отрисовывает элементы на изображении на основе словаря состояний.

    Аргументы:
        input_step: Шаг сетки.
        field: Словарь, где ключи - кортежи координат (x, y),
               а значения - объекты с атрибутом _status.
        image_to_draw: Изображение, на котором производится отрисовка.
        color: Базовый цвет клеток (red, blue, green).
    """
    last_item = next(reversed(field.items()))
    y = last_item[0][1]
    x = last_item[0][0]
    for y_coord in range(0,y+1,1):
        for x_coord in range(0,x+1, 1):
            if field.get((int(x_coord),int(y_coord)))._status == True:
                cell_obj = field.get((int(x_coord), int(y_coord)))
                draw_by_index(x_coord, y_coord, image_to_draw, input_step, age=cell_obj._age, color=color)
def draw_by_index(first_index,second_index,image,step,age=1,color='green'):
    """
    Отрисовывает прямоугольник по заданным индексам сетки.

    Аргументы:
        first_index: Индекс по оси X.
        second_index: Индекс по оси Y.
        image: Изображение для отрисовки.
        step: Шаг сетки.
        age: Возраст ячейки (определяет оттенок цвета).
        color: Базовый цвет клеток (red, blue, green).

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
    base_colors = {
        'red': (255, 0, 0),
        'blue': (0, 0, 255),
        'green': (0, 255, 0),
    }
    r, g, b = base_colors.get(color, (0, 255, 0))
    factor = max(0, 255 - age * 15) / 255
    cell_color = (int(r * factor), int(g * factor), int(b * factor))
    draw.rectangle((0+5+_step*_n1,0+5+_step*_n2, _n1*_step+_step+5,_step+5+_step*_n2), fill=cell_color)

def draw_generation_count(image, generation_count):
    """
    Добавляет текст с номером текущего поколения к изображению.
    
    Аргументы:
        image: Исходное изображение (PIL.Image), к которому добавляется текст.
        generation_count: Целое число, представляющее номер текущего поколения.
        
    Возвращает:
        PIL.Image: Изображение с добавленной белой рамкой и текстом 'Current generation: {generation_count}' в левом верхнем углу.
    """
    full_text = 'Current generation: ' + str(generation_count)
    short_text1 = 'Current generation:'
    short_text2 = str(generation_count)
    tiny_text1 = 'gen'
    tiny_text2 = str(generation_count)

    temp_draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", size=20)
    except IOError:
        font = ImageFont.load_default()

    def text_width(text):
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]

    line_height = temp_draw.textbbox((0, 0), "A", font=font)[3]

    padding = 10

    if text_width(full_text) <= image.width:
        lines = [full_text]
        text_width_val = text_width(full_text)
    elif text_width(short_text1) <= image.width:
        lines = [short_text1, short_text2]
        text_width_val = max(text_width(short_text1), text_width(short_text2))
    else:
        lines = [tiny_text1, tiny_text2]
        text_width_val = max(text_width(tiny_text1), text_width(tiny_text2))

    new_width = image.width + padding * 2
    new_height = image.height + line_height * len(lines) + padding * 2

    new_image = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 255))
    new_image.paste(image, (padding, line_height * len(lines) + padding * 2))

    draw = ImageDraw.Draw(new_image)
    for i, line in enumerate(lines):
        draw.text((padding, padding + i * line_height), line, fill="black", font=font)

    return new_image
def showGrid(im):
    """
    Отображает изображение на экране.
    
    Аргументы:
        im: Объект изображения для отображения.
    """
    if im != None:
        im.show()