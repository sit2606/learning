def openConfig():
    """
    Считывает параметры конфигурации и начальные координаты живых клеток из файла 'input.txt'.
    
    Возвращает:
        tuple: Кортеж, содержащий:
            - INPUT_LENGTH (int): Длина поля.
            - INPUT_WIDTH (int): Ширина поля.
            - GENERATION_COUNT (int): Количество поколений для симуляции.
            - STARTING_FIELD (list): Список кортежей с координатами начальных живых клеток.
    """
    file = open('input.txt')
    for line in file:
        if line == '- Length\n':
            INPUT_LENGTH = int(file.readline())
        if line == '- Width\n':
            INPUT_WIDTH = int(file.readline())
        if line == '- Generation count\n':
            GENERATION_COUNT = int(file.readline())
        if line == '- Start Field Config (Please, provide a coordinates of alive cells)\n':
            STARTING_FIELD = file.readlines()
    STARTING_FIELD = [eval(item) for item in STARTING_FIELD]
    file.close() 
    return(INPUT_LENGTH,INPUT_WIDTH,GENERATION_COUNT, STARTING_FIELD)
def putConfigToFile(sim_result,INPUT_LENGTH, INPUT_WIDTH, GENERATION_COUNT):
    """
    Сохраняет итоговое состояние симуляции и параметры конфигурации в текстовый файл 'sim_results.txt'.
    
    Аргументы:
        sim_result (dict): Итоговое состояние игрового поля, где ключи - кортежи координат, 
                           а значения - объекты клеток с атрибутом _status.
        INPUT_LENGTH (int): Длина поля.
        INPUT_WIDTH (int): Ширина поля.
        GENERATION_COUNT (int): Количество симулированных поколений.
    """
    ENDING_FIELD = []
    for key,item in sim_result.items():
        if item._status == True:
            ENDING_FIELD.append(str(key) + '\n')
    file = open('sim_results.txt','w')
    file.write('-- Field Options\n')
    file.write('- Length\n')
    file.write(str(INPUT_LENGTH) + '\n')
    file.write('- Width\n')
    file.write(str(INPUT_WIDTH) + '\n')
    file.write('- Generation count\n')
    file.write(str(GENERATION_COUNT) + '\n')
    file.write('- Start Field Config (Please, provide a coordinates of alive cells)\n')
    file.writelines(ENDING_FIELD)
    file.close()

