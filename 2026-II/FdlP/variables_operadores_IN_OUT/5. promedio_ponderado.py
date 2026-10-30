# Pide tres notas y muestra el promedio ponderado con pesos 20%,30%,50%
# Fórmula: promedio = n1·0.20 + n2·0.30 + n3·0.50

# leer 3 notas
nota1 = float(input("Ingrese nota 1: "))
nota2 = float(input("Ingrese nota 2: "))
nota3 = float(input("Ingrese nota 3: "))

#calcular promedio ponderado
promedio = (nota1*0.2 + nota2*0.3 + nota3*0.5)/3

# mostrar promedio
print("El promedio ponderado es:", promedio)
