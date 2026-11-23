# vector 35: sumar cifras de dos numeros menores que 10000

a = int(input("ingrese primer numero positivo (< 10000): "))
b = int(input("ingrese segundo numero positivo (< 10000): "))

vector_a = [int(c) for c in str(a)]
vector_b = [int(c) for c in str(b)]

suma = a + b
vector_suma = [int(c) for c in str(suma)]

print("cifras del primer numero:", vector_a)
print("cifras del segundo numero:", vector_b)
print("vector con la suma:", vector_suma)
