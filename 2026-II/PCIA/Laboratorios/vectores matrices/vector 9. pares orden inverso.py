# vector 9: leer 6 enteros pares y mostrar inverso

vector = []
while len(vector) < 6:
    num = int(input("ingrese un numero par: "))
    if num % 2 == 0:
        vector.append(num)
    else:
        print("no es par intente nuevamente")

print("pares en orden inverso:")
for i in range(len(vector) - 1, -1, -1):
    print(vector[i])
