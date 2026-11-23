# recursividad

def producto(A,B):
    if B==0:
        return 0
    else:
        return A + producto(A,B-1)

def potencia(base,E):
    if E==0:
        return 1
    return base*potencia(base,E-1)

def mcd(A,B):
    if B==0:
        return A
    return mcd(B,A%B)

def sumaDivisoresPropios(n, divisor=1, suma=0):
    if n <= 1:
        return 0
    if divisor >= n:
        return suma
    if n % divisor == 0:
        suma += divisor
    return sumaDivisoresPropios(n, divisor + 1, suma)

def suma(n):
    if n == 1:
        return 1
    else:
        return n + suma(n - 1)

def contarDigito(n, d):
    if n == 0:
        return 0
    else:
        ultimo = n % 10

        if ultimo == d:
            return 1 + contarDigito(n // 10, d)
        else:
            return contarDigito(n // 10, d)

def decimalBinario(n):
    if n < 2:
        return str(n)
    else:
        return decimalBinario(n // 2) + str(n % 2)



print(producto(2,3))
print(potencia(2,3))
print(mcd(24,36))
print(sumaDivisoresPropios(20))