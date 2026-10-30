# Un numero de tres digitos es de Arsmtrong si es igual a la suma de los cubos
# de sus digitos. Escribir un algoritmo que muestre todos los numeros de
# Arsmtrong comprendidos entre 100 y 999
# ejemplo 153 = 1**3 + 5**3 + 3**3 = 1 + 125 + 27 = 153

# buscar numeros de arsmtrong
k=100
while k<1000:
    suma=0
    aux=k
    while aux>0:
        dig = aux%10
        suma=suma+dig**3
        aux=aux//10
        
    if suma==k:
        print(k,end=" ")
    k=k+1
