# vector 4: suma de valores en posiciones x e y

vector = []
print("ingrese 8 numeros:")
for i in range(8):
    vector.append(int(input(f"posicion {i}: ")))

x = int(input("ingrese posicion x (0 a 7): "))
y = int(input("ingrese posicion y (0 a 7): "))

suma = vector[x] + vector[y]
print(f"la suma de los valores en {x} y {y} es:", suma)
