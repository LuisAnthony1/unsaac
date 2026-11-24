# ejercicio 2: control de ventas de una tienda mediante recursividad

def contar_ventas(n, m):
    if n < 10:
        if n >= m:
            return 1
        else:
            return 0
    else:
        ultimo = n % 10
        if ultimo >= m:
            return 1 + contar_ventas(n // 10, m)
        else:
            return contar_ventas(n // 10, m)

n = int(input("registro de ventas: "))
m = int(input("cantidad minima: "))

total = contar_ventas(n, m)
print("periodos que cumplen la condicion:", total)
