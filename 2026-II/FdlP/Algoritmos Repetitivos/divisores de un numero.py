# LUIS ANTHONY MAMANI MESCCO
# calcular los divisores de un numero
# Leer
n = int(input("N: "))

# procesar cantidad de divisores
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
