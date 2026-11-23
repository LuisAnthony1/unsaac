# matriz 11: suma de elementos de la diagonal secundaria 3x3

print("ingrese datos de la matriz 3x3:")
matriz = [[int(input(f"[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

suma = 0
for i in range(3):
    suma = suma + matriz[i][2 - i]

print("la suma de la diagonal secundaria es:", suma)
