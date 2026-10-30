# Escribir un algoritmo que muestre todos los divisores de un numero entero
# positivo N y la cantidad de divisores que tiene

# Leer numero
num = int(input("Ingrese numero: "))

# calcular los divisores
k=1
con=0
while num>=k:
    if num%k==0:
        con=con+1
        print(k,end=" ")
    k=k+1

# mostrar cantidad
print("cantidad =",con)
