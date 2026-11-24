# ejercicio 3: control de inventario mediante codigos de productos

def contar_codigo(a, n, x):
    if n == 0:
        return 0
    else:
        if a[n - 1] == x:
            return 1 + contar_codigo(a, n - 1, x)
        else:
            return contar_codigo(a, n - 1, x)

n = int(input("cantidad de elementos: "))
a = []
for i in range(n):
    codigo = int(input("ingrese codigo: "))
    a.append(codigo)

x = int(input("codigo buscado: "))

veces = contar_codigo(a, n, x)
print("el codigo", x, "aparece", veces, "veces")
