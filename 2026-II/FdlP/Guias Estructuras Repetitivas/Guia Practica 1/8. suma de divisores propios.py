# Los divisores propios de un número N son todos sus divisores menores que N.
# Escribir un algoritmo que calcule la suma de los divisores propios de un
# número entero positivo. Observe que basta probar los posibles divisores desde
# 1 hasta N/2.

# Leer numero
num = int(input("Ingrese numero: "))

# calcular los divisores
k=1
suma=0
while num>k:
    if num%k==0:
        suma=suma+k
    k=k+1

# mostrar cantidad
print("suma de todos los divisores =",suma)
