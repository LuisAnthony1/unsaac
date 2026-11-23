# vector 20: guardar impares de intervalo 0 a 50

vector1 = []
print("ingrese 10 enteros en el intervalo [0, 50]:")
while len(vector1) < 10:
    n = int(input(f"numero {len(vector1) + 1}: "))
    if 0 <= n <= 50:
        vector1.append(n)
    else:
        print("numero fuera de rango intente de nuevo")

impares = []
for num in vector1:
    if num % 2 != 0:
        impares.append(num)

print("primer vector (2 por linea):")
for i in range(0, len(vector1), 2):
    print(vector1[i:i+2])

print("vector de impares (2 por linea):")
for i in range(0, len(impares), 2):
    print(impares[i:i+2])
