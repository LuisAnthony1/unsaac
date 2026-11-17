# Universidad Nacional de San Antonio Abad del Cusco
# Fundamentos de Programacion
# --------------------------------------------------
# MiLibreria
# Luis Anthony Mamani Mescco
# --------------------------------------------------

# Modulo el mayor de 2 numeros
def MayorDos(X,Y):
    if X>Y:
        Mayor=X
    else:
        Mayor=Y
    return Mayor

# Modulo Sumar divisores
def SumaDivisores(N):
    Suma=0
    K=0
    while K<N:
        K=K+1
        if N%K==0:
            Suma=Suma+K
    return Suma

def SumaDivisoresPropios(N):
    return SumaDivisores(N)-N

def SumaDivisoresPropios1(N):
    Suma=0
    K=0
    while K<N//2:
        K=K+1
        if N%K==0:
            Suma=Suma+K
    return Suma

# MODULOS NUEVOS

# Menor de 2 numeros (analogo a MayorDos)
def MenorDos(X,Y):
    if X<Y:
        Menor=X
    else:
        Menor=Y
    return Menor

# Leer un entero dentro del rango [Min, Max]
def LeerEntero(Min,Max,Texto):
    N=int(input(Texto))
    while N<Min or N>Max:
        print("Error, digite un numero entre ",Min," y ",Max)
        N=int(input(Texto))
    return N

# Leer un real dentro del rango [Min, Max]
def LeerReal(Min,Max,Texto):
    N=float(input(Texto))
    while N<Min or N>Max:
        print("Error, digite un numero entre ",Min," y ",Max)
        N=float(input(Texto))
    return N

# Contar divisores de N
def ContarDivisores(N):
    NroDivisores=0
    K=0
    while K<N:
        K=K+1
        if N%K==0:
            NroDivisores=NroDivisores+1
    return NroDivisores

# EsPrimo reutilizando ContarDivisores
def EsPrimo(N):
    if ContarDivisores(N)==2:
        return True
    else:
        return False

# Factorial de N (N>=0)
def Factorial(N):
    Resultado=1
    K=0
    while K<N:
        K=K+1
        Resultado=Resultado*K
    return Resultado

# Numero combinatorio C(N,M)
def Combinatorio(N,M):
    return Factorial(N)//(Factorial(M)*Factorial(N-M))

# Permutacion P(N,M) = N!/(N-M)!
def Permutacion(N,M):
    return Factorial(N)//Factorial(N-M)

# Potencia B elevado a N (N>=0)
def Potencia(B,N):
    Resultado=1
    K=0
    while K<N:
        K=K+1
        Resultado=Resultado*B
    return Resultado
