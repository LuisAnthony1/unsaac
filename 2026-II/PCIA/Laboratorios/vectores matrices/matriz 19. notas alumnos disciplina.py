# matriz 19: notas de alumnos (5 filas x 4 columnas)

matriz = []
print("ingrese datos para 5 alumnos:")
for i in range(5):
    print(f"alumno {i + 1}:")
    matricula = int(input("matricula: "))
    media_pruebas = int(input("media de pruebas: "))
    media_trabajos = int(input("media de trabajos: "))
    nota_final = media_pruebas + media_trabajos
    matriz.append([matricula, media_pruebas, media_trabajos, nota_final])

mayor_nota = matriz[0][3]
mat_mayor = matriz[0][0]
suma_finales = 0

for fila in matriz:
    suma_finales = suma_finales + fila[3]
    if fila[3] > mayor_nota:
        mayor_nota = fila[3]
        mat_mayor = fila[0]

print(f"alumno con mayor nota final: matricula {mat_mayor} con nota {mayor_nota}")
print("media de las notas finales:", suma_finales / len(matriz))
