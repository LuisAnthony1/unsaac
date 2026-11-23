# ejercicio 11: calcular b = a^2 (a multiplicada por a)

def multiplicar_matrices(a, b):
    resultado = []
    for i in range(3):
        fila = []
        for j in range(3):
            suma = 0
            for k in range(3):
                suma = suma + a[i][k] * b[k][j]
            fila.append(suma)
        resultado.append(fila)
    return resultado

print("ingrese matriz a de 3x3:")
a = [[int(input(f"a[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

b = multiplicar_matrices(a, a)
print("matriz b = a^2:")
for fila in b:
    print(fila)
