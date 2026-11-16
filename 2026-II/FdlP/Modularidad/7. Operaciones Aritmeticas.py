import MiLibreria as ml

def Line(C,N):
    return C*N

def Presentacion():
    L=len("Universidad Nacional de San Antonio Abad del Cusco")
    print(Line("-",L+4))
    print("| Universidad Nacional de San Antonio Abad del Cusco |")
    print(Line("-",L+4))
    print("| Autor: Luis Anthony Mamani Mescco                  |")
    print(Line("-",L+4))
    print("| Programa: Operaciones Aritmeticas                  |")
    print(Line("-",L+4))

Presentacion()

# Leer datos
N=ml.LeerEntero(1,100,"N: ")
M=ml.LeerEntero(1,100,"M: ")

# Operacion
producto=ml.Combinatorio(N,M)

# Mostrar
print(producto)

