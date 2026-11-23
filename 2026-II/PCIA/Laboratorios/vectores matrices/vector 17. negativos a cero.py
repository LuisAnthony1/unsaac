# vector 17: poner cero a los numeros negativos

vector = []
print("ingrese 10 numeros:")
for i in range(10):
    vector.append(int(input(f"posicion {i}: ")))

for i in range(len(vector)):
    if vector[i] < 0:
        vector[i] = 0

print("vector modificado:")
print(vector)
