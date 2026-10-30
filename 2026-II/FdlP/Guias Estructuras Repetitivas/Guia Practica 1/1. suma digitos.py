# Escribir un algoritmo que lea un numero entero positivo y calcule la suma de sus digitos.

# Leer el numero
num = int(input("Ingrese un numero: "))

# calcular la suma
suma = 0
while num>0:
    digito = num%10
    suma = suma + digito
    num = num//10

# mostrar el resultado
print("La suma de los digitos es: ",suma)

