# ejercicio 5: buscar numero en matriz nxn

def buscar(matriz, x):
    encontrados = []
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == x:
                encontrados.append((i, j))
    return encontrados

n = int(input("ingrese orden n de la matriz: "))
matriz = []
print("ingrese elementos de la matriz:")
for i in range(n):
    fila = []
    for j in range(n):
        fila.append(int(input(f"posicion [{i}][{j}]: ")))
    matriz.append(fila)

numero = int(input("numero a buscar: "))
posiciones = buscar(matriz, numero)

if len(posiciones) > 0:
    print("el numero existe en la matriz")
    for p in posiciones:
        print(f"encontrado en fila {p[0]} y columna {p[1]}")
else:
    print("el numero no existe en la matriz")
