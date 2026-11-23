# Universidad Nacional de San Antonio Abad del Cusco
# Fundamentos de Programacion
# --------------------------------------------------
# MiLibreria
# Luis Anthony Mamani Mescco
# --------------------------------------------------

# Modulo linea decorativa
def line(C,N):
    return C*N

# Modulo presentacion institucional
def presentacion(texto):
    L = len("Universidad Nacional de San Antonio Abad del Cusco")
    print(line("-", L + 4))
    print("| Universidad Nacional de San Antonio Abad del Cusco |")
    print(line("-", L + 4))
    print("| Autor: Luis Anthony Mamani Mescco                  |")
    print(line("-", L + 4))
    print(f"| {texto.ljust(L)} |")
    print(line("-", L + 4))

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

# Modulo Sumar divisores propios
def SumaDivisoresPropios(N):
    return SumaDivisores(N)-N

# Modulo Sumar divisores propios eficiente
def SumaDivisoresPropios1(N):
    Suma=0
    K=0
    while K<N//2:
        K=K+1
        if N%K==0:
            Suma=Suma+K
    return Suma

# Modulo Menor de 2 numeros
def MenorDos(X,Y):
    if X<Y:
        Menor=X
    else:
        Menor=Y
    return Menor

# Modulo Leer un entero dentro del rango [Min, Max]
def LeerEntero(Min,Max,Texto):
    N=int(input(Texto))
    while N<Min or N>Max:
        print("Error, digite un numero entre ",Min," y ",Max)
        N=int(input(Texto))
    return N

# Modulo Leer un real dentro del rango [Min, Max]
def LeerReal(Min,Max,Texto):
    N=float(input(Texto))
    while N<Min or N>Max:
        print("Error, digite un numero entre ",Min," y ",Max)
        N=float(input(Texto))
    return N

# Modulo Contar divisores de N
def ContarDivisores(N):
    NroDivisores=0
    K=0
    while K<N:
        K=K+1
        if N%K==0:
            NroDivisores=NroDivisores+1
    return NroDivisores

# Modulo EsPrimo reutilizando ContarDivisores
def EsPrimo(N):
    if ContarDivisores(N)==2:
        return True
    else:
        return False

# Modulo Factorial de N
def Factorial(N):
    Resultado=1
    K=0
    while K<N:
        K=K+1
        Resultado=Resultado*K
    return Resultado

# Modulo Numero combinatorio C(N,M)
def Combinatorio(N,M):
    return Factorial(N)//(Factorial(M)*Factorial(N-M))

# Modulo Permutacion P(N,M)
def Permutacion(N,M):
    return Factorial(N)//Factorial(N-M)

# Modulo Potencia B elevado a N
def Potencia(B,N):
    Resultado=1
    K=0
    while K<N:
        K=K+1
        Resultado=Resultado*B
    return Resultado

# Modulo fibonacci recursivo
def fibonacci(n):
    if n<2:
        return n
    else:
        return fibonacci(n-1)+fibonacci(n-2)

# Modulo cociente por restas sucesivas
def cociente(A, B):
    if A < B:
        return 0
    else:
        return 1 + cociente(A - B, B)

# Modulo resto de division entera
def resto(A, B):
    if A < B:
        return A
    return resto(A - B, B)

# Modulo contar digitos de N recursivo
def contarDigitos(N):
    if N<10:
        return 1
    else:
        return contarDigitos(N//10)+1

# Modulo sumar digitos de N recursivo
def sumarDigitos(N):
    if N<10:
        return N
    else:
        return sumarDigitos(N//10)+(N%10)
