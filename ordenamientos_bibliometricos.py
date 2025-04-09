# ordenamientos_bibliometricos.py

import os
import re
import time
import matplotlib.pyplot as plt
from collections import Counter
from tabulate import tabulate
import pandas as pd

from ordenamientos.timsort import timsort
from ordenamientos.comb_sort import comb_sort
from ordenamientos.selection_sort import selection_sort
from ordenamientos.pigeonhole_sort import pigeonhole_sort
from ordenamientos.bucket_sort import bucket_sort
from ordenamientos.quick_sort import quick_sort
from ordenamientos.heap_sort import heap_sort
from ordenamientos.bitonic_sort import bitonic_sort
from ordenamientos.gnome_sort import gnome_sort
from ordenamientos.binary_insertion_sort import binary_insertion_sort
from ordenamientos.radix_sort import radix_sort
from ordenamientos.bubble_sort import bubble_sort

# ---------------------- PARTE 1: CARGA DE DATOS ----------------------

def extraer_abstracts_manual(filepath):
    abstracts = []
    with open(filepath, encoding="utf-8") as f:
        contenido = f.read()
        matches = re.findall(r'abstract\s*=\s*[{\"]([^{}\"]+)[}\"]', contenido, re.IGNORECASE)
        abstracts.extend(matches)
    return abstracts

def contar_terminos_manual(abstracts, terminos):
    contador = Counter()
    for abstract in abstracts:
        lower_abstract = abstract.lower()
        for termino in terminos:
            if "-" in termino:
                for sub in termino.lower().split("-"):
                    contador[termino] += lower_abstract.count(sub)
            else:
                contador[termino] += lower_abstract.count(termino.lower())
    return contador

def cargar_frecuencias_desde_bibtex(ruta):
    terminos = [
        "Abstraction", "Motivation", "Algorithm", "Persistence", "Coding", "Block",
        "Creativity", "Mobile application", "Logic", "Programming", "Conditionals",
        "Robotic", "Loops", "Scratch"
    ]
    conteo_global = Counter()
    for archivo in os.listdir(ruta):
        if archivo.endswith(".bib"):
            abstracts = extraer_abstracts_manual(os.path.join(ruta, archivo))
            conteo_global.update(contar_terminos_manual(abstracts, terminos))
    conteo_ordenado = sorted(conteo_global.items(), key=lambda x: (-x[1], x[0]))
    return conteo_ordenado

# ---------------------- PARTE 3: EJECUCIÓN Y VISUALIZACIÓN ----------------------

def aplicar_algoritmos_y_mostrar(ruta):
    datos = cargar_frecuencias_desde_bibtex(ruta)
    algoritmos = {
        "TimSort": timsort,
        "Comb Sort": comb_sort,
        "Selection Sort": selection_sort,
        "Pigeonhole Sort": pigeonhole_sort,
        "Bucket Sort": bucket_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort,
        "Bitonic Sort": bitonic_sort,
        "Gnome Sort": gnome_sort,
        "Binary Insertion Sort": binary_insertion_sort,
        "Radix Sort": radix_sort,
        "Bubble Sort": bubble_sort,
    }

    for nombre, algoritmo in algoritmos.items():
        datos_copia = datos.copy()
        inicio = time.time()
        resultado = algoritmo(datos_copia)
        tiempo = time.time() - inicio

        df = pd.DataFrame(resultado, columns=["Término", "Frecuencia"])
        print(f"\nAlgoritmo: {nombre} - Tiempo: {tiempo:.6f} s")
        print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))

        plt.figure(figsize=(10, 5))
        plt.bar(df["Término"], df["Frecuencia"])
        plt.title(f"{nombre} - Tiempo: {tiempo:.6f} s")
        plt.xlabel("Término")
        plt.ylabel("Frecuencia")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

# ---------------------- EJECUCIÓN PRINCIPAL ----------------------

if __name__ == "__main__":
    ruta_bibtex = "./Articulos"  # cambiar a la ruta de los archivos .bib
    aplicar_algoritmos_y_mostrar(ruta_bibtex)
