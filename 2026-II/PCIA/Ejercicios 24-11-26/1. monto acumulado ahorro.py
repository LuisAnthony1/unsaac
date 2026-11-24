# ejercicio 1: calculo del monto acumulado de un ahorro

def monto_acumulado(c, t, n):
    if n <= 0:
        return c
    else:
        anterior = monto_acumulado(c, t, n - 1)
        return anterior + anterior * (t / 100)

c = float(input("capital inicial: "))
t = float(input("tasa de interes anual: "))
n = int(input("tiempo en anios: "))

resultado = monto_acumulado(c, t, n)
print("el monto acumulado sera:", round(resultado, 2))
