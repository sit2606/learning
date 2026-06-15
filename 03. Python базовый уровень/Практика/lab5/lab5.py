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
from Grid import field,draw_by_dictionary,draw_coordinates, draw_generation_count
import Life 
import copy
from PIL import Image
INPUT_LENGTH = 200
INPUT_WIDTH = 100
INPUT_STEP = 20
GENERATION_COUNT = 30
MANUAL_MODE = False

graphic = field(INPUT_LENGTH, INPUT_WIDTH ,  INPUT_STEP).draw_grid()
game_field = Life.generate_field(INPUT_LENGTH,INPUT_WIDTH,INPUT_STEP, MANUAL_MODE)
if (not MANUAL_MODE):
    populated_field = Life.populate_field(game_field)
else:
    populated_field = game_field
draw_by_dictionary(INPUT_STEP,populated_field,graphic._image)
z2 = draw_coordinates(graphic._image, 20, INPUT_LENGTH, INPUT_WIDTH, INPUT_STEP)
sim_field = Life.check_for_neighbours(populated_field)
sim_results = []
sim_results.append(sim_field)
for i in range(0,GENERATION_COUNT,1):
    sim_field0 = copy.deepcopy(Life.check_for_neighbours(sim_field)) 
    sim_field1 = copy.deepcopy(Life.apply_rules(sim_field0))
    sim_results.append(sim_field1)
    sim_field = copy.deepcopy(sim_field1)
images = []
for index,item in enumerate(sim_results):
    graphic = field(INPUT_LENGTH, INPUT_WIDTH , INPUT_STEP).draw_grid()
    draw_by_dictionary(INPUT_STEP,item,graphic._image)
    img = draw_coordinates(graphic._image, 20, INPUT_LENGTH, INPUT_WIDTH, INPUT_STEP)
    img = draw_generation_count(img, index)
    images.append(img)
im1 = Image.new("RGBA", (INPUT_LENGTH + INPUT_STEP*4, INPUT_WIDTH + INPUT_STEP*4), (0, 0, 0))
im1.save("out.gif", save_all=True, append_images=images, duration=100, loop=0)