import math

d1 = float(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => \n"))
d2 = float(input("Введите кратчайшее расстояние между утопающего до берега, d2 (футы) => \n")) 
h = float(input("Введите боковое смещение между спасателем и утопающим, h (ярды) => \n")) 
v_sand = float(input("Введите  скорость двежения спасателя по песку, v_sand (мили в час) => \n")) 
n = float(input("Введите  коэффициент замедления спасателя при движении в воде, n  => \n")) 
theta1 = float(input("Введите  направление движения спасателя по песку, theta1 (градусы)  => \n")) 



def convert(d1,h,v_sand,theta1):
    d1 = d1 * 3
    h = h * 3
    v_sand = v_sand*5280 /3600 
    theta1 = math.radians(theta1)
    return(d1,h,v_sand,theta1)

d1,h,v_sand,theta1_rad = convert(d1,h,v_sand,theta1)
x = d1 * math.tan(theta1_rad)
L1 = math.sqrt(math.pow(x,2) + math.pow(d1,2))

L2 = math.sqrt(math.pow((h-x),2) + math.pow(d2,2))
t = 1/v_sand * (L1 + n * L2)

print(f"Если спасатель начнёт движение под углом theta1, равным {int(round(theta1))} градусам, он достигнет утопающего через {t:.1f} секунды")