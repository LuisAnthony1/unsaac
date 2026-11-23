# vector 24: alumno mas alto y mas bajo entre 10

alumnos = []
alturas = []

for i in range(10):
    num = int(input(f"numero del alumno {i + 1}: "))
    alt = float(input(f"altura en metros del alumno {i + 1}: "))
    alumnos.append(num)
    alturas.append(alt)

mas_alto = 0
mas_bajo = 0

for i in range(1, 10):
    if alturas[i] > alturas[mas_alto]:
        mas_alto = i
    if alturas[i] < alturas[mas_bajo]:
        mas_bajo = i

print(f"alumno mas alto: numero {alumnos[mas_alto]} con {alturas[mas_alto]} m")
print(f"alumno mas bajo: numero {alumnos[mas_bajo]} con {alturas[mas_bajo]} m")
