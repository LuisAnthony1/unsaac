# Luis Anthony Mamani Mescco
# sumar secuencia 1**2 - 2**2 + 3**2 ... -100**2
n=0
suma=0
while n<100:
    n+=1
    suma=suma+n**2
    n+=1
    suma=suma-n**2

# mostrar suma
print("La suma de la secuencia es:",suma)

