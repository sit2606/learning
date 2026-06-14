"""
Скрипт для запуска и визуализации симуляции игры «Жизнь» Конвея.

Этот модуль выполняет следующие действия:
1. Инициализирует параметры сетки (размеры и шаг).
2. Создает начальное состояние игрового поля (случайное или заданное вручную).
3. Вычисляет заданное количество поколений, применяя правила игры.
4. Отрисовывает каждое поколение с координатной сеткой.
5. Сохраняет последовательность кадров в анимированный GIF-файл 'out.gif'.

Зависимости:
    - Grid: модуль для отрисовки сетки и координат.
    - Life: модуль, содержащий логику игры «Жизнь» (генерация, правила, соседи).
    - PIL (Pillow): библиотека для работы с изображениями и создания анимации.
"""
from Grid import field,draw_by_dictionary,draw_coordinates,showGrid
import Life 
import copy
from PIL import Image
input_length = 100
input_width = 100
input_step = 20
generation_count = 10
manual_mode = False
graphic = field(input_length, input_width ,  input_step).draw_grid()
game_field = Life.generate_field(input_length,input_width,input_step, manual_mode)
if (not manual_mode):
    populated_field = Life.populate_field(game_field)
else:
    populated_field = game_field
draw_by_dictionary(input_step,populated_field,graphic._image)
z2 = draw_coordinates(graphic._image, 20, input_length, input_width, input_step)
sim_field = Life.check_for_neighbours(populated_field)
sim_results = []
sim_results.append(sim_field)
for i in range(0,generation_count,1):
    sim_field0 = copy.deepcopy(Life.check_for_neighbours(sim_field)) 
    sim_field1 = copy.deepcopy(Life.apply_rules(sim_field0))
    sim_results.append(sim_field1)
    sim_field = copy.deepcopy(sim_field1)
images = []
for i in sim_results:
    graphic = field(input_length, input_width ,  input_step).draw_grid()
    draw_by_dictionary(input_step,i,graphic._image)
    img = draw_coordinates(graphic._image, 20, input_length, input_width, input_step)
    images.append(img)
im1 = Image.new("RGBA", (input_length + 50, input_width + 50), (0, 0, 0))
im1.save("out.gif", save_all=True, append_images=images, duration=100, loop=0)