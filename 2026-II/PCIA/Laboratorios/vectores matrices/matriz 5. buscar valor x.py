# matriz 5: buscar valor x en matriz 5x5

matriz = []
print("ingrese datos para matriz 5x5:")
for i in range(5):
    fila = []
    for j in range(5):
        fila.append(int(input(f"posicion [{i}][{j}]: ")))
    matriz.append(fila)

x = int(input("ingrese valor x a buscar: "))
encontrado = False

for i in range(5):
    for j in range(5):
        if matriz[i][j] == x:
            print(f"elemento encontrado en fila {i} y columna {j}")
            encontrado = True

if not encontrado:
    print("elemento no encontrado")
