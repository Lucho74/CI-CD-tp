import os
import csv

def validar_archivo(path_csv):
    return os.path.exists(path_csv)

def ordenar_burbuja(filas):
    n = len(filas)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            clave_actual = (filas[j][0], filas[j][1])
            clave_siguiente = (filas[j + 1][0], filas[j + 1][1])
            if clave_actual > clave_siguiente:
                filas[j], filas[j + 1] = filas[j + 1], filas[j]
    return filas

def leer_csv(path_csv):
    with open(path_csv, newline='') as csvfile:
        reader = csv.reader(csvfile)
        encabezado = next(reader)
        filas = list(reader)
    return encabezado, filas

def escribir_csv(path_csv, encabezado, filas):
    with open(path_csv, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(encabezado)
        writer.writerows(filas)

def calcular_totales_producto(data, i, current_product):
    total_units_product = 0
    total_price_product = 0
    row = data[i]
    while i < len(data) and current_product == row[1]:
        row = data[i]
        units_product = int(row[4])
        price_product = float(row[5])
        total_units_product += units_product
        total_price_product += price_product * units_product
        i += 1
    return i, total_units_product, total_price_product

def actualizar_max_min(current_product, total_price_product, max_product, max_price_product, min_product, min_price_product):
    if total_price_product > max_price_product:
        max_product = current_product
        max_price_product = total_price_product
    if total_price_product < min_price_product:
        min_product = current_product
        min_price_product = total_price_product
    return max_product, max_price_product, min_product, min_price_product

def procesar_sucursal(data, i, current_branch):
    total_units_branch = 0
    total_price_branch = 0
    max_price_product = 0
    min_price_product = 999999999
    max_product = None
    min_product = None

    while i < len(data) and current_branch == data[i][0]:
        current_product = data[i][1]
        i, total_units_product, total_price_product = calcular_totales_producto(data, i, current_product)
        print(f"Cod. Prod.: {current_product}, Total Uni.: {total_units_product}, Total precio: {total_price_product:.2f}")
        max_product, max_price_product, min_product, min_price_product = actualizar_max_min(
            current_product, total_price_product,
            max_product, max_price_product,
            min_product, min_price_product
        )
        total_units_branch += total_units_product
        total_price_branch += total_price_product

    return i, total_units_branch, total_price_branch, max_product, max_price_product, min_product, min_price_product