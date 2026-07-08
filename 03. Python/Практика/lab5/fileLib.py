def openConfig():
    """
    Считывает параметры конфигурации и начальные координаты живых клеток из файла 'input.txt'.

    Возвращает:
        tuple: Кортеж, содержащий:
            - INPUT_LENGTH (int): Длина поля.
            - INPUT_WIDTH (int): Ширина поля.
            - GENERATION_COUNT (int): Количество поколений для симуляции.
            - STARTING_FIELD (list): Список кортежей с координатами начальных живых клеток и их возрастом.
            - COLOR (str): Базовый цвет клеток (red, blue, green).
    """
    file = open('input.txt')
    COLOR = 'green'
    for line in file:
        if line == '- Length\n':
            INPUT_LENGTH = int(file.readline())
        if line == '- Width\n':
            INPUT_WIDTH = int(file.readline())
        if line == '- Generation count\n':
            GENERATION_COUNT = int(file.readline())
        if line == '- Color\n':
            COLOR = file.readline().strip()
        if line == '- Field Config\n':
            STARTING_FIELD = file.readlines()
    result = []
    for item in STARTING_FIELD:
        item = item.strip()
        if 'age=' in item:
            coord_part, age_part = item.split(' age=')
            result.append((eval(coord_part), int(age_part)))
        else:
            result.append((eval(item), 0))
    STARTING_FIELD = result
    file.close()
    return(INPUT_LENGTH,INPUT_WIDTH,GENERATION_COUNT, STARTING_FIELD, COLOR)
def putConfigToFile(sim_result,INPUT_LENGTH, INPUT_WIDTH, GENERATION_COUNT, CURRENT_GENERATION, output_dir='.', color='green'):
    """
    Сохраняет итоговое состояние симуляции и параметры конфигурации в текстовый файл 'sim_results.txt'.

    Аргументы:
        sim_result (dict): Итоговое состояние игрового поля, где ключи - кортежи координат,
                           а значения - объекты клеток с атрибутом _status.
        INPUT_LENGTH (int): Длина поля.
        INPUT_WIDTH (int): Ширина поля.
        GENERATION_COUNT (int): Количество симулированных поколений.
        CURRENT_GENERATION (int): Номер текущего поколения.
        output_dir (str): Директория для сохранения файла.
        color (str): Базовый цвет клеток (red, blue, green).
    """
    ENDING_FIELD = []
    for key,item in sim_result.items():
        if item._status == True:
            ENDING_FIELD.append(str(key) + ' age=' + str(item._age) + '\n')
    import os
    file = open(os.path.join(output_dir, 'sim_results.txt'),'w')
    file.write('-- Field Options\n')
    file.write('- Length\n')
    file.write(str(INPUT_LENGTH) + '\n')
    file.write('- Width\n')
    file.write(str(INPUT_WIDTH) + '\n')
    file.write('- Generation count\n')
    file.write(str(GENERATION_COUNT) + '\n')
    file.write('- Current generation\n')
    file.write(str(CURRENT_GENERATION) + '\n')
    file.write('- Color\n')
    file.write(color + '\n')
    file.write('- Field Config\n')
    file.writelines(ENDING_FIELD)
    file.close()

