# ejercicio 7: consumo de 8 alimentadores durante 24 horas

def calcular_totales(matriz):
    totales = []
    promedios = []
    for i in range(8):
        suma = 0
        for j in range(24):
            suma = suma + matriz[i][j]
        totales.append(suma)
        promedios.append(suma / 24)
    return totales, promedios

def alimentador_maximo(totales):
    mayor = totales[0]
    pos = 0
    for i in range(1, len(totales)):
        if totales[i] > mayor:
            mayor = totales[i]
            pos = i
    return pos + 1, mayor

def demanda_extrema(matriz):
    por_hora = []
    for j in range(24):
        suma_hora = 0
        for i in range(8):
            suma_hora = suma_hora + matriz[i][j]
        por_hora.append(suma_hora)
    max_d = max(por_hora)
    min_d = min(por_hora)
    return por_hora.index(max_d), max_d, por_hora.index(min_d), min_d

matriz = []
print("ingrese datos de consumo 8x24:")
for i in range(8):
    print(f"alimentador {i + 1}:")
    fila = []
    for j in range(24):
        fila.append(float(input(f"hora {j}: ")))
    matriz.append(fila)

totales, promedios = calcular_totales(matriz)
for i in range(8):
    print(f"alimentador {i + 1} - total: {totales[i]} - promedio: {promedios[i]}")

alim, mayor = alimentador_maximo(totales)
print(f"mayor consumo diario: alimentador {alim} con {mayor} kw")

h_max, d_max, h_min, d_min = demanda_extrema(matriz)
print(f"demanda maxima en hora {h_max} con {d_max} kw")
print(f"demanda minima en hora {h_min} con {d_min} kw")
