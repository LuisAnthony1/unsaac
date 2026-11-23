# Universidad Nacional de San Antonio Abad del Cusco
# Luis Anthony Mamani Mescco

from MiLibreria import *

def PromedioNotas():
    print("--- Problema 1: promedio de 3 notas ---")
    N1 = LeerEntero(0, 20, "Nota 1 : ")
    N2 = LeerEntero(0, 20, "Nota 2 : ")
    N3 = LeerEntero(0, 20, "Nota 3 : ")
    Promedio = (N1 + N2 + N3) / 3
    print("Promedio : ", round(Promedio, 2))

def EvaluarAprobacion():
    N1 = LeerEntero(0, 20, "Nota 1 : ")
    N2 = LeerEntero(0, 20, "Nota 2 : ")
    N3 = LeerEntero(0, 20, "Nota 3 : ")
    Promedio = (N1 + N2 + N3) / 3
    print("Promedio : ", round(Promedio, 2))
    if Promedio >= 10.5:
        print("APROBADO")
    else:
        print("DESAPROBADO")

def PromedioPonderado():
    N1 = LeerReal(0, 20, "Nota 1 (30%) : ")
    N2 = LeerReal(0, 20, "Nota 2 (30%) : ")
    N3 = LeerReal(0, 20, "Nota 3 (40%) : ")
    Promedio = N1 * 0.30 + N2 * 0.30 + N3 * 0.40
    print("Promedio ponderado : ", round(Promedio, 2))

def EliminarMenor():
    N1 = LeerEntero(0, 20, "Nota 1 : ")
    N2 = LeerEntero(0, 20, "Nota 2 : ")
    N3 = LeerEntero(0, 20, "Nota 3 : ")
    N4 = LeerEntero(0, 20, "Nota 4 : ")
    Menor = MenorDos(MenorDos(N1, N2), MenorDos(N3, N4))
    Promedio = (N1 + N2 + N3 + N4 - Menor) / 3
    print("Nota eliminada : ", Menor)
    print("Promedio : ", round(Promedio, 2))

def FormatoFecha():
    D = LeerEntero(1, 31, "Dia (1-31) : ")
    M = LeerEntero(1, 12, "Mes (1-12) : ")
    A = LeerEntero(1900, 2100, "Anio (1900-2100) : ")
    print("Fecha : ", str(D).zfill(2) + "/" + str(M).zfill(2) + "/" + str(A))

def VerificarPrimo():
    N = LeerEntero(1, 1000, "Digite N (1-1000) : ")
    if EsPrimo(N):
        print(N, " es primo")
    else:
        print(N, " NO es primo")

def NumeroPerfecto():
    print("--- Problema 2: numero perfecto ---")
    N = LeerEntero(1, 100000, "Digite N : ")
    if SumaDivisoresPropios(N) == N:
        print(N, " es un numero perfecto")
    else:
        print(N, " NO es un numero perfecto")

def ListarPerfectos():
    print("Perfectos entre 1 y 10000:")
    N = 0
    while N < 10000:
        N = N + 1
        if SumaDivisoresPropios1(N) == N:
            print(N)

def ClasificarNumero():
    N = LeerEntero(1, 100000, "Digite N : ")
    S = SumaDivisoresPropios(N)
    if S == N:
        print(N, " es PERFECTO")
    elif S > N:
        print(N, " es ABUNDANTE")
    else:
        print(N, " es DEFICIENTE")

def NumerosAmigos():
    A = LeerEntero(1, 100000, "Digite A : ")
    B = LeerEntero(1, 100000, "Digite B : ")
    if SumaDivisoresPropios(A) == B and SumaDivisoresPropios(B) == A:
        print(A, " y ", B, " son amigos")
    else:
        print(A, " y ", B, " NO son amigos")

def ListarAmigos():
    print("Pares de amigos menores que 10000:")
    A = 1
    while A < 10000:
        A = A + 1
        B = SumaDivisoresPropios1(A)
        if A < B and B < 10000 and SumaDivisoresPropios1(B) == A:
            print(A, "-", B)

def CasiPerfectos():
    print("Casi perfectos menores que 1000:")
    N = 0
    while N < 999:
        N = N + 1
        if SumaDivisoresPropios(N) == N - 1:
            print(N)

def MasDivisores():
    Max = 0
    Numero = 0
    N = 0
    while N < 1000:
        N = N + 1
        C = ContarDivisores(N)
        if C > Max:      # se guarda el numero asociado al maximo
            Numero = N
        Max = MayorDos(Max, C)
    print("El numero con mas divisores es ", Numero, " con ", Max, " divisores")

def CompararEficiencia():
    N = LeerEntero(1, 100000, "Digite N : ")
    print("SumaDivisoresPropios  : ", SumaDivisoresPropios(N), " (", N, " vueltas)")
    print("SumaDivisoresPropios1 : ", SumaDivisoresPropios1(N), " (", N // 2, " vueltas)")
    print("Dan lo mismo porque ningun divisor propio de N es mayor que N//2;")
    print("los unicos candidatos mayores serian N (que se excluye) y nada entre N//2 y N.")
    print("Hace menos vueltas SumaDivisoresPropios1 (la mitad).")

def CalcularCombinatorio():
    print("--- Problema 3: numero combinatorio ---")
    N = LeerEntero(0, 100, "Elementos del conjunto (n) : ")
    M = LeerEntero(0, N, "Elementos a tomar (m) : ")
    print("C(", N, ",", M, ") = ", Combinatorio(N, M))

def JugadasLoteria():
    print("Jugadas de loteria C(45,6) = ", Combinatorio(45, 6))

def CalcularComisiones():
    print("Comisiones C(30,4) = ", Combinatorio(30, 4))

def ElegirCargos():
    print("Formas de elegir presidente, secretario y tesorero de 10: ", Permutacion(10, 3))

def TrianguloPascal():
    F = LeerEntero(1, 15, "Numero de filas (1-15) : ")
    N = 0
    while N < F:
        M = 0
        while M <= N:
            print(Combinatorio(N, M), end=" ")
            M = M + 1
        print()
        N = N + 1

def VerificarSimetria():
    N = LeerEntero(0, 100, "Digite n : ")
    Cumple = True
    M = 0
    while M <= N:
        if Combinatorio(N, M) != Combinatorio(N, N - M):
            Cumple = False
        M = M + 1
    if Cumple:
        print("Se cumple C(n,m) = C(n,n-m) para todo m")
    else:
        print("NO se cumple la simetria")

def SumaPascal():
    N = LeerEntero(0, 100, "Digite n : ")
    Suma = 0
    M = 0
    while M <= N:
        Suma = Suma + Combinatorio(N, M)
        M = M + 1
    print("Suma de la fila = ", Suma, " ; 2^n = ", Potencia(2, N))
    if Suma == Potencia(2, N):
        print("Se verifica la igualdad")
    else:
        print("NO se verifica")

# MENU
Opciones = {
    "1": PromedioNotas, "1.1": EvaluarAprobacion, "1.2": PromedioPonderado, "1.3": EliminarMenor, "1.4": FormatoFecha, "1.5": VerificarPrimo,
    "2": NumeroPerfecto, "2.1": ListarPerfectos, "2.2": ClasificarNumero, "2.3": NumerosAmigos, "2.4": ListarAmigos, "2.5": CasiPerfectos, "2.6": MasDivisores, "2.7": CompararEficiencia,
    "3": CalcularCombinatorio, "3.1": JugadasLoteria, "3.2": CalcularComisiones, "3.3": ElegirCargos, "3.4": TrianguloPascal, "3.5": VerificarSimetria, "3.6": SumaPascal
}

if __name__ == "__main__":
    print("Problemas: 1, 2, 3 | Ejercicios: 1.1-1.5, 2.1-2.7, 3.1-3.6 | 0 = salir")
    Op = input("Que desea ejecutar? ")
    while Op != "0":
        if Op in Opciones:
            Opciones[Op]()
        else:
            print("Opcion no valida")
        Op = input("\nQue desea ejecutar? ")
