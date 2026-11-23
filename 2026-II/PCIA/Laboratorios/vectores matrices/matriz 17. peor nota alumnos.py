# matriz 17: alumnos con peor nota en cada prueba (10 alumnos x 3 pruebas)

notas = []
print("ingrese notas de 10 alumnos en 3 pruebas:")
for i in range(10):
    print(f"alumno {i + 1}:")
    fila = []
    for j in range(3):
        fila.append(float(input(f"prueba {j + 1}: ")))
    notas.append(fila)

peor_p1 = 0
peor_p2 = 0
peor_p3 = 0

for i in range(10):
    min_nota = min(notas[i])
    if notas[i][0] == min_nota:
        peor_p1 = peor_p1 + 1
    elif notas[i][1] == min_nota:
        peor_p2 = peor_p2 + 1
    else:
        peor_p3 = peor_p3 + 1

print("alumnos con peor nota en prueba 1:", peor_p1)
print("alumnos con peor nota en prueba 2:", peor_p2)
print("alumnos con peor nota en prueba 3:", peor_p3)
