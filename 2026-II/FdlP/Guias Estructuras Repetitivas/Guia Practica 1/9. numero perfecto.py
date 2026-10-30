# Un número entero positivo es perfecto si es igual a la suma de sus divisores
# propios. Escribir un algoritmo que determine si un número es o no perfecto.
# Como extensión, muestre todos los números perfectos menores que 10000.

# Leer numero
num = int(input("Ingrese numero: "))

# calcular los divisores
k=1
suma=0
while num>k:
    if num%k==0:
        suma=suma+k
    k=k+1

#mostrar si es perfecto
if suma==num:
    print("Es perfecto",suma)
else:
    print("No es perfecto",suma)

# mostrar todos los perfectos <10000
print("Los numeros perfectos menores a 10 000 son:")
i=1
while i<10000:
    suma=0
    aux=i
    j=1
    while aux>j:
        if aux%j==0:
            suma=suma+j
        j+=1
    if i==suma:
        print(i,end=" ")
    i+=1
