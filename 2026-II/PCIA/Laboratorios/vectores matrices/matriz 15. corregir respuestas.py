# matriz 15: correccion de 10 preguntas de opcion multiple para 5 alumnos

gabarito = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e']
respuestas = []

print("ingrese respuestas de 5 alumnos (10 preguntas por alumno):")
for i in range(5):
    print(f"alumno {i + 1}:")
    fila = []
    for j in range(10):
        fila.append(input(f"pregunta {j + 1}: ").lower())
    respuestas.append(fila)

resultado = []
for i in range(5):
    puntos = 0
    for j in range(10):
        if respuestas[i][j] == gabarito[j]:
            puntos = puntos + 1
    resultado.append(puntos)

for i in range(5):
    print(f"alumno {i + 1}: {resultado[i]} puntos")
