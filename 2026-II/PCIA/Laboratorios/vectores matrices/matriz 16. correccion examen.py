# matriz 16: calcular notas y porcentaje de aprobacion de 3 alumnos

gabarito = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e']
matriculas = []
notas = []

for i in range(3):
    mat = int(input(f"matricula alumno {i + 1}: "))
    matriculas.append(mat)
    nota = 0
    for j in range(10):
        resp = input(f"pregunta {j + 1}: ").lower()
        if resp == gabarito[j]:
            nota = nota + 1
    notas.append(nota)

aprobados = 0
for i in range(3):
    print(f"matricula: {matriculas[i]} - nota: {notas[i]}")
    if notas[i] >= 7.0:
        aprobados = aprobados + 1

porcentaje = (aprobados / 3) * 100
print(f"porcentaje de aprobacion: {porcentaje:.2f}%")
