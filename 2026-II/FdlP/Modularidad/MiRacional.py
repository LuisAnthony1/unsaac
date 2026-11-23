# Universidad Nacional de San Antonio Abad del Cusco
# Departamento Academico de Informatica
# Fundamentos de Programacion
# Luis Anthony Mamani Mescco
# --------------------------------------------------
# Libreria: MiRacional.py

import MiLibreria

# Modulo Maximo Comun Divisor de dos enteros con while
def MCD(A, B):
    A = abs(A)
    B = abs(B)
    while B != 0:
        A, B = B, A % B
    return A

# Modulo Minimo Comun Multiplo reutilizando MCD
def MCM(A, B):
    if A == 0 or B == 0:
        return 0
    return abs(A * B) // MCD(A, B)

# Modulo Verificar si un racional es indeterminado
def EsIndeterminado(R):
    return R[1] == 0 or R == (0, 0)

# Modulo Simplificar y normalizar racional con MCD
def Simplificar(R):
    N, D = R
    if D == 0:
        return (0, 0)
    if N == 0:
        return (0, 1)
    if D < 0:
        N = -N
        D = -D
    g = MCD(N, D)
    return (N // g, D // g)

# Modulo Sumar dos racionales
def Sumar(R1, R2):
    if EsIndeterminado(R1) or EsIndeterminado(R2):
        return (0, 0)
    N = R1[0] * R2[1] + R2[0] * R1[1]
    D = R1[1] * R2[1]
    return Simplificar((N, D))

# Modulo Restar dos racionales reutilizando Sumar
def Restar(R1, R2):
    if EsIndeterminado(R1) or EsIndeterminado(R2):
        return (0, 0)
    return Sumar(R1, (-R2[0], R2[1]))

# Modulo Multiplicar dos racionales
def Multiplicar(R1, R2):
    if EsIndeterminado(R1) or EsIndeterminado(R2):
        return (0, 0)
    N = R1[0] * R2[0]
    D = R1[1] * R2[1]
    return Simplificar((N, D))

# Modulo Dividir dos racionales
def Dividir(R1, R2):
    if EsIndeterminado(R1) or EsIndeterminado(R2):
        return (0, 0)
    if R2[0] == 0:
        return (0, 0)
    N = R1[0] * R2[1]
    D = R1[1] * R2[0]
    return Simplificar((N, D))

# Modulo Comparar si dos racionales son iguales
def Iguales(R1, R2):
    if EsIndeterminado(R1) and EsIndeterminado(R2):
        return True
    if EsIndeterminado(R1) or EsIndeterminado(R2):
        return False
    return Simplificar(R1) == Simplificar(R2)

# Modulo Convertir racional a texto
def ATexto(R):
    if EsIndeterminado(R):
        return "Indeterminado"
    N, D = Simplificar(R)
    if D == 1:
        return str(N)
    return f"{N}/{D}"

# Modulo Leer racional por teclado
def LeerRacional(Texto):
    print(Texto)
    N = MiLibreria.LeerEntero(-1000, 1000, "  Numerador  : ")
    D = MiLibreria.LeerEntero(-1000, 1000, "  Denominador: ")
    return Simplificar((N, D))
