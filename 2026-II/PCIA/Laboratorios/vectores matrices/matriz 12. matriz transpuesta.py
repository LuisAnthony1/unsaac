# matriz 12: transpuesta de matriz 3x3

print("ingrese datos de la matriz 3x3:")
matriz = [[int(input(f"[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

transpuesta = []
for j in range(3):
    fila = []
    for i in range(3):
        fila.append(matriz[i][j])
    transpuesta.append(fila)

print("matriz transpuesta:")
for f in transpuesta:
    print(f)
