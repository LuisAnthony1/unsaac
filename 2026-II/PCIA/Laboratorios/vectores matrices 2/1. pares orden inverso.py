# ejercicio 1: leer 6 enteros pares y mostrar en orden inverso

def leer_pares():
    vector = []
    while len(vector) < 6:
        num = int(input("ingrese un numero par: "))
        if num % 2 == 0:
            vector.append(num)
        else:
            print("el numero no es par intente de nuevo")
    return vector

datos = leer_pares()
print("valores en orden inverso:")
for i in range(len(datos) - 1, -1, -1):
    print(datos[i])
