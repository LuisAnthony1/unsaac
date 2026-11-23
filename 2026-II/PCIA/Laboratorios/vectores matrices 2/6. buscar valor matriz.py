# ejercicio 6: buscar valor x en matriz 5x5

def buscar_en_matriz(matriz, x):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == x:
                return i, j
    return None

matriz = []
print("ingrese datos para matriz 5x5:")
for i in range(5):
    fila = []
    for j in range(5):
        fila.append(int(input(f"posicion [{i}][{j}]: ")))
    matriz.append(fila)

x = int(input("ingrese el valor a buscar: "))
pos = buscar_en_matriz(matriz, x)

if pos is not None:
    print(f"elemento encontrado en linea {pos[0]} y columna {pos[1]}")
else:
    print("elemento no encontrado")
