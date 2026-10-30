# Escribir un algoritmo que determine el mayor y el menor digito de un numero
# entero positivo, asi como la posicion (contando desde la derecha) en la que
# se encuentra el mayor digito.

# Leer numero
num = int(input("Ingrese numero: "))

# variables inciales
pos = 1
mayor = 0
menor = 9

# calcular el mayor y menor
while num>0:
    dig = num%10
    if dig>mayor:
        mayor=dig
        pos=pos+1
    if dig<menor:
        menor=dig
    num=num//10

# mostrar resultados
print(f"Mayor digito = {mayor} (posicion {pos}), Menor digito = {menor}")
