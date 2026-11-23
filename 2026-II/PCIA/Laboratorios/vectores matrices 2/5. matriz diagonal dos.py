# ejercicio 5: matriz 5x5 con 2 en diagonal principal y 0 en resto

def crear_matriz():
    matriz = []
    for i in range(5):
        fila = []
        for j in range(5):
            if i == j:
                fila.append(2)
            else:
                fila.append(0)
        matriz.append(fila)
    return matriz

resultado = crear_matriz()
print("matriz obtenida:")
for fila in resultado:
    print(fila)
