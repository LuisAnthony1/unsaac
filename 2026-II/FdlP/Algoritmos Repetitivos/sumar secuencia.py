# Luis Anthony Mamani Mescco
# sumar secuencia 1**2 - 2**2 + 3**2 ... -100**2
#sumar impares
Si = 0
K = -1
while K<99:
    K+=2
    Si = Si + K**2

#sumar pares
Sp = 0
K = 0
while K<100:
    K+=2
    Sp = Sp + K**2

suma= Si-Sp

#mostrar suma
print("La suma de la secuencia es:", suma)
