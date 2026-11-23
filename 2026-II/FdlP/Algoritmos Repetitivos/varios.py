# LUIS ANTHONY MAMANI MESCCO
# calcular los divisores de un numero
# Leer
n = int(input("N: "))

# procesar cantidad de divisores
k = 0
contador = 0
while k < n:
    k+=1
    if n%k==0:
        contador+=1
        print(k, end=" ")
print()

# indicar si es perfecto o no
k = 0
suma = 0
while k < n-1:
    k += 1
    if n%k == 0:
        suma += k
        
if suma == n:
    print("SI es perfecto")
else:
    print("NO es perfecto")
        
# indicar si es primo o no
if contador == 2:
    print("Es primo")
else:
    print("No es primo")

# tabla de multiplicar de "N"
print()
k = 0
while k < 12:
    k+=1
    print(f"{n} x {k} = {n*k}")
print()

# convertir a bits n
k=0
while n > 0:
    b = n % 2
    n = n // 2
    print(b, end="")
