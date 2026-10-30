# Escribir un algoritmo que calcule la suma de todos los divisores
# de un numero entero positivo N, incluido el propio N

# Leer numero
num = int(input("Ingrese numero: "))

# calcular los divisores
k=1
suma=0
while num>=k:
    if num%k==0:
        suma=suma+k
    k=k+1

# mostrar cantidad
print("suma de todos los divisores =",suma)
