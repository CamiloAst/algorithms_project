import csv
import time
import numpy as np  # Para calcular el promedio

# 📌 Leer el archivo CSV
def read_csv(filename):
    articles = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            articles.append(row)
    return articles

# 📌 Medir el tiempo de ejecución usando TimSort
def measure_time_timsort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = data.copy()  # Copiar datos para evitar modificar el original
        start_time = time.perf_counter()
        sorted(data_copy, key=lambda x: x["Year"])  # TimSort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

# 📌 Implementación del algoritmo Comb Sort
def comb_sort(arr):
    gap = len(arr)
    shrink = 1.3  # Factor de reducción recomendado
    sorted_flag = False

    while gap > 1 or not sorted_flag:
        gap = max(1, int(gap / shrink))  # Reducir el espacio entre elementos
        sorted_flag = True
        for i in range(len(arr) - gap):
            if arr[i]["Year"] > arr[i + gap]["Year"]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]  # Intercambiar
                sorted_flag = False

# 📌 Medir el tiempo de ejecución usando Comb Sort
def measure_time_combsort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = data.copy()  # Copiar datos para evitar modificar el original
        start_time = time.perf_counter()
        comb_sort(data_copy)  # Aplicar Comb Sort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j]["Year"] < arr[min_idx]["Year"]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # Intercambio
    return arr

# 📌 Medir el tiempo de ejecución usando Selection Sort
def measure_time_selectionsort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = data.copy()  # Copiar datos para evitar modificar el original
        start_time = time.perf_counter()
        selection_sort(data_copy)  # Ejecutar Selection Sort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

class TreeNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

# 📌 Insertar en el BST
def insert(root, key, data):
    if root is None:
        return TreeNode(key, data)
    if key < root.key:
        root.left = insert(root.left, key, data)
    else:
        root.right = insert(root.right, key, data)
    return root

# 📌 Recorrido in-order para obtener los elementos ordenados
def inorder_traversal(root, sorted_list):
    if root:
        inorder_traversal(root.left, sorted_list)
        sorted_list.append(root.data)
        inorder_traversal(root.right, sorted_list)

# 📌 Algoritmo de ordenamiento Tree Sort
def tree_sort(arr):
    if not arr:
        return []
    root = None
    for item in arr:
        root = insert(root, item["Year"], item)
    sorted_list = []
    inorder_traversal(root, sorted_list)
    return sorted_list

# 📌 Medir el tiempo de ejecución usando Tree Sort
def measure_time_treesort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = data.copy()  # Copiar datos para evitar modificar el original
        start_time = time.perf_counter()
        tree_sort(data_copy)  # Ejecutar Tree Sort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

# 📌 Ejecutar el código
if __name__ == "__main__":
    articles = read_csv("articles.csv")
    N = len(articles)  # Cantidad de artículos

    T_timsort = measure_time_timsort(articles)  # Medir tiempo con TimSort

    T_combsort= measure_time_combsort(articles)

    T_selectionSort= measure_time_selectionsort(articles)

    T_treesort = measure_time_treesort(articles)

 
    
    # 📌 Imprimir resultados en formato solicitado
    print(f"N = {N}")
    print(f"Tiempo TimSort = {T_timsort} ms")
    print(f"Tiempo Comb Sort = {T_combsort} ms")
    print(f"Tiempo Selection Sort = {T_selectionSort} ms")
    print(f"Tiempo Tree Sort = {T_treesort} ms")
    