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
