# vector 10: media de notas de 15 alumnos

notas = []
print("ingrese las notas de 15 alumnos:")
for i in range(15):
    notas.append(float(input(f"nota alumno {i + 1}: ")))

suma = 0
for n in notas:
    suma = suma + n

media = suma / len(notas)
print("la media general de notas es:", media)
