"""
Скрипт для запуска и визуализации симуляции игры «Жизнь» Конвея.

Использование:
    python lab5.py                 — ручной режим, случайное заполнение
    python lab5.py --file          — файловый режим (чтение из input.txt)
    python lab5.py --manual        — ручной режим с предустановленным паттерном

Режимы работы:
    --file    : параметры и начальные координаты считываются из 'input.txt'
    --manual  : предустановленный паттерн (глайдер)
    (без флагов): случайное заполнение поля

Последовательность действий:
1. Инициализирует параметры сетки (размеры и шаг) в зависимости от выбранного режима.
2. Создаёт начальное состояние игрового поля.
3. Вычисляет заданное количество поколений, применяя правила игры «Жизнь».
4. Отрисовывает каждое поколение с координатной сеткой и номером текущего поколения.
5. Сохраняет итоговое состояние симуляции в файл 'sim_results.txt' через fileLib.
6. Сохраняет каждое поколение  как отдельный PNG-файл (формат: "Gen {номер_поколения}.png")
7. Сохраняет последовательность кадров в анимированный GIF-файл 'out.gif'.

Зависимости:
    - Grid: модуль для отрисовки сетки, координат и номеров поколений.
    - Life: модуль, содержащий логику игры «Жизнь» (генерация, правила, подсчёт соседей).
    - fileLib: модуль для чтения конфигурации из файла и записи результатов симуляции.
    - PIL (Pillow): библиотека для работы с изображениями и создания анимации.
"""
from Grid import field,draw_by_dictionary,draw_coordinates, draw_generation_count
import fileLib
import Life
import copy
import sys
import os
from PIL import Image

os.makedirs("sim_result", exist_ok=True)

INPUT_STEP = 20
FILE_MODE = '--file' in sys.argv
MANUAL_MODE = '--manual' in sys.argv

if (FILE_MODE):
    INPUT_LENGTH, INPUT_WIDTH, GENERATION_COUNT,STARTING_FIELD, COLOR = fileLib.openConfig();
else:
    INPUT_LENGTH = 400
    INPUT_WIDTH = 400
    GENERATION_COUNT = 60
    COLOR = 'blue'
graphic = field(INPUT_LENGTH, INPUT_WIDTH ,  INPUT_STEP).draw_grid()
game_field = Life.generate_field(INPUT_LENGTH,INPUT_WIDTH,INPUT_STEP, MANUAL_MODE)
if (not MANUAL_MODE and not FILE_MODE):
    populated_field = Life.populate_field(game_field)
elif (FILE_MODE):
    populated_field = Life.populate_field_by_config(game_field,STARTING_FIELD)
if (MANUAL_MODE):
    populated_field = game_field
draw_by_dictionary(INPUT_STEP,populated_field,graphic._image, COLOR)
z2 = draw_coordinates(graphic._image, 20, INPUT_LENGTH, INPUT_WIDTH, INPUT_STEP)
sim_field = Life.check_for_neighbours(populated_field)
sim_results = []
sim_results.append(sim_field)
for i in range(0,GENERATION_COUNT,1):
    sim_field0 = copy.deepcopy(Life.check_for_neighbours(sim_field)) 
    sim_field1 = copy.deepcopy(Life.apply_rules(sim_field0))
    sim_results.append(sim_field1)
    sim_field = copy.deepcopy(sim_field1)
last_sim_result = next(reversed(sim_results)) 
fileLib.putConfigToFile(last_sim_result,INPUT_LENGTH,INPUT_WIDTH, GENERATION_COUNT, GENERATION_COUNT, "sim_result", COLOR)
images = []
for index,item in enumerate(sim_results):
    graphic = field(INPUT_LENGTH, INPUT_WIDTH , INPUT_STEP).draw_grid()
    draw_by_dictionary(INPUT_STEP,item,graphic._image, COLOR)
    img = draw_coordinates(graphic._image, 20, INPUT_LENGTH, INPUT_WIDTH, INPUT_STEP)
    img = draw_generation_count(img, index)
    images.append(img)
    fileLib.putConfigToFile(item, INPUT_LENGTH, INPUT_WIDTH, GENERATION_COUNT, index, "sim_result", COLOR)
    os.replace(os.path.join("sim_result", "sim_results.txt"), os.path.join("sim_result", f"Gen {index}.txt"))
im1 = Image.new("RGBA", (INPUT_LENGTH + INPUT_STEP*4, INPUT_WIDTH + INPUT_STEP*4), (255, 255, 255))
x = 0
for i in images:
    im_name = "Gen " + str(x)
    i.save(os.path.join("sim_result", f"{im_name}.png"))
    x += 1
im1.save(os.path.join("sim_result", "out.gif"), save_all=True, append_images=images, duration=100, loop=0)