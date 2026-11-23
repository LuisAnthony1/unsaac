# ejercicio 14: carro con menor kilometraje

carros = ["toyota", "nissan", "isuzu", "mazda", "volvo"]
kilometrajes = [932, 651, 780, 200, 120]

def carro_mas_nuevo(nombres, km):
    menor_km = km[0]
    pos = 0
    for i in range(1, len(km)):
        if km[i] < menor_km:
            menor_km = km[i]
            pos = i
    return nombres[pos], menor_km

nombre, menor = carro_mas_nuevo(carros, kilometrajes)
print(f"el carro mas nuevo es {nombre} con {menor} km")
