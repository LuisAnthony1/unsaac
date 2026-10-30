# Universidad Nacional San Antonio Abad del Cusco
# Alumno: Luis Anthony Mamani Mescco
'''
Ejercicio 1. Suma de sumas
Escribir un algoritmo que calcule:  S = 1 + (1+2) + (1+2+3) + ... + (1+2+3+...+N). Resuélvalo primero con dos bucles anidados y luego con un solo bucle, aprovechando la suma parcial anterior. Compare ambas soluciones: ¿cuántas sumas realiza cada una para un N dado?
Ejemplo:
Entrada: N = 4
Salida: S = 1 + 3 + 6 + 10 = 20
'''

# Leer cantidad de terminos
N=int(input("N : "))

# Calcular suma de sumas
SumaTotal=0
SumaParcial=0
K=0
while K<N:
    K=K+1
    SumaParcial=SumaParcial+K
    SumaTotal=SumaTotal+SumaParcial
    
# Mostrar valor de la suma de sumas
print("El valor de la suma es : ",SumaTotal)
