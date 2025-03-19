import csv
import time
import numpy as np  # Para calcular el promedio
import matplotlib.pyplot as plt

# Luego puedes generar la gráfica como lo estabas haciendo.


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

def bucket_sort(arr):
    filtered_arr = [article for article in arr if article["Year"].isdigit()]
    if not filtered_arr:
        return arr  # Si no hay datos válidos, retornar la lista original
    
    min_year = min(int(article["Year"]) for article in filtered_arr)
    max_year = max(int(article["Year"]) for article in filtered_arr)
    bucket_count = max_year - min_year + 1
    buckets = [[] for _ in range(bucket_count)]
    
    for article in filtered_arr:
        year = int(article["Year"])
        buckets[year - min_year].append(article)
    
    sorted_articles = []
    for bucket in buckets:
        sorted_articles.extend(bucket)
    
    return sorted_articles

# 📌 Medir el tiempo de ejecución usando Bucket Sort
def measure_time_bucketsort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = [article for article in data if article["Year"].isdigit()]  # Filtrar valores no numéricos
        start_time = time.perf_counter()
        bucket_sort(data_copy)  # Ejecutar Bucket Sort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

def quicksort(arr):
    filtered_arr = [article for article in arr if article["Year"].isdigit()]
    if len(filtered_arr) <= 1:
        return filtered_arr
    
    pivot = filtered_arr[len(filtered_arr) // 2]
    left = [article for article in filtered_arr if int(article["Year"]) < int(pivot["Year"])]
    middle = [article for article in filtered_arr if int(article["Year"]) == int(pivot["Year"])]
    right = [article for article in filtered_arr if int(article["Year"]) > int(pivot["Year"])]
    
    return quicksort(left) + middle + quicksort(right)

# 📌 Medir el tiempo de ejecución usando QuickSort
def measure_time_quicksort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = [article for article in data if article["Year"].isdigit()]  # Filtrar valores no numéricos
        start_time = time.perf_counter()
        quicksort(data_copy)  # Ejecutar QuickSort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

# 📌 Implementación del algoritmo HeapSort con manejo de errores
def heapify(arr, n, i):
    largest = i  # Inicializar el nodo raíz como el más grande
    left = 2 * i + 1  # Hijo izquierdo
    right = 2 * i + 2  # Hijo derecho
    
    if left < n and int(arr[left]["Year"]) > int(arr[largest]["Year"]):
        largest = left
    
    if right < n and int(arr[right]["Year"]) > int(arr[largest]["Year"]):
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Intercambiar
        heapify(arr, n, largest)

# 📌 Función principal HeapSort
def heapsort(arr):
    filtered_arr = [article for article in arr if article["Year"].isdigit()]
    n = len(filtered_arr)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(filtered_arr, n, i)
    
    for i in range(n - 1, 0, -1):
        filtered_arr[i], filtered_arr[0] = filtered_arr[0], filtered_arr[i]  # Intercambiar
        heapify(filtered_arr, i, 0)
    
    return filtered_arr

# 📌 Medir el tiempo de ejecución usando HeapSort
def measure_time_heapsort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = [article for article in data if article["Year"].isdigit()]  # Filtrar valores no numéricos
        start_time = time.perf_counter()
        heapsort(data_copy)  # Ejecutar HeapSort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

# 📌 Función para comparar e intercambiar elementos en Bitonic Sort
def bitonic_compare(arr, up):
    n = len(arr)
    dist = n // 2
    while dist > 0:
        for i in range(n - dist):
            if (up and int(arr[i]["Year"]) > int(arr[i + dist]["Year"])) or (not up and int(arr[i]["Year"]) < int(arr[i + dist]["Year"])):
                arr[i], arr[i + dist] = arr[i + dist], arr[i]  # Intercambio
        dist //= 2

# 📌 Función principal de Bitonic Sort
def bitonic_sort(arr, up=True):
    filtered_arr = [article for article in arr if article["Year"].isdigit()]
    n = len(filtered_arr)
    
    if n <= 1:
        return filtered_arr
    
    mid = n // 2
    left = bitonic_sort(filtered_arr[:mid], True)
    right = bitonic_sort(filtered_arr[mid:], False)
    
    sorted_arr = left + right
    bitonic_compare(sorted_arr, up)
    return sorted_arr

# 📌 Medir el tiempo de ejecución usando Bitonic Sort
def measure_time_bitonicsort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = [article for article in data if article["Year"].isdigit()]  # Filtrar valores no numéricos
        start_time = time.perf_counter()
        bitonic_sort(data_copy)  # Ejecutar Bitonic Sort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

# 📌 Implementación del algoritmo Gnome Sort con manejo de errores
def gnome_sort(arr):
    filtered_arr = [article for article in arr if article["Year"].isdigit()]
    n = len(filtered_arr)
    index = 0
    
    while index < n:
        if index == 0 or int(filtered_arr[index]["Year"]) >= int(filtered_arr[index - 1]["Year"]):
            index += 1
        else:
            filtered_arr[index], filtered_arr[index - 1] = filtered_arr[index - 1], filtered_arr[index]  # Intercambiar
            index -= 1
    
    return filtered_arr

# 📌 Medir el tiempo de ejecución usando Gnome Sort
def measure_time_gnomesort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = [article for article in data if article["Year"].isdigit()]  # Filtrar valores no numéricos
        start_time = time.perf_counter()
        gnome_sort(data_copy)  # Ejecutar Gnome Sort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

# 📌 Implementación del algoritmo Binary Insertion Sort con manejo de errores
def binary_insertion_sort(arr):
    filtered_arr = [article for article in arr if article["Year"].isdigit()]
    n = len(filtered_arr)
    
    for i in range(1, n):
        key = filtered_arr[i]
        left, right = 0, i - 1
        
        while left <= right:
            mid = (left + right) // 2
            if int(filtered_arr[mid]["Year"]) > int(key["Year"]):
                right = mid - 1
            else:
                left = mid + 1
        
        filtered_arr = filtered_arr[:left] + [key] + filtered_arr[left:i] + filtered_arr[i+1:]
    
    return filtered_arr

# 📌 Medir el tiempo de ejecución usando Binary Insertion Sort
def measure_time_binaryinsertionsort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = [article for article in data if article["Year"].isdigit()]  # Filtrar valores no numéricos
        start_time = time.perf_counter()
        binary_insertion_sort(data_copy)  # Ejecutar Binary Insertion Sort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo

# 📌 Función para encontrar el valor máximo en la lista
def get_max(arr):
    return max(int(article["Year"]) for article in arr if article["Year"].isdigit())

# 📌 Función auxiliar para hacer el conteo por dígitos
def counting_sort(arr, exp):
    n = len(arr)
    output = [None] * n
    count = [0] * 10
    
    for article in arr:
        index = (int(article["Year"]) // exp) % 10
        count[index] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        index = (int(arr[i]["Year"]) // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    for i in range(n):
        arr[i] = output[i]

# 📌 Implementación del algoritmo Radix Sort
def radix_sort(arr):
    filtered_arr = [article for article in arr if article["Year"].isdigit()]
    max_value = get_max(filtered_arr)
    exp = 1
    while max_value // exp > 0:
        counting_sort(filtered_arr, exp)
        exp *= 10
    return filtered_arr

# 📌 Medir el tiempo de ejecución usando Radix Sort
def measure_time_radixsort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = [article for article in data if article["Year"].isdigit()]  # Filtrar valores no numéricos
        start_time = time.perf_counter()
        radix_sort(data_copy)  # Ejecutar Radix Sort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo
# 📌 Implementación del algoritmo Pigeonhole Sort
def pigeonhole_sort(arr):
    filtered_arr = [article for article in arr if article["Year"].isdigit()]
    if not filtered_arr:
        return []
    
    min_year = min(int(article["Year"]) for article in filtered_arr)
    max_year = max(int(article["Year"]) for article in filtered_arr)
    size = max_year - min_year + 1
    
    pigeonholes = [[] for _ in range(size)]
    
    for article in filtered_arr:
        index = int(article["Year"]) - min_year
        pigeonholes[index].append(article)
    
    sorted_arr = []
    for bucket in pigeonholes:
        sorted_arr.extend(bucket)
    
    return sorted_arr

# 📌 Medir el tiempo de ejecución usando Pigeonhole Sort
def measure_time_pigeonholesort(data, runs=100):
    times = []
    for _ in range(runs):
        data_copy = [article for article in data if article["Year"].isdigit()]  # Filtrar valores no numéricos
        start_time = time.perf_counter()
        pigeonhole_sort(data_copy)  # Ejecutar Pigeonhole Sort
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertir a ms
    return round(np.mean(times), 3)  # Promediar tiempo



if __name__ == "__main__":
    articles = read_csv("articles.csv")
    N = len(articles)  # Cantidad de artículos

    tiempos = {
        "TimSort": measure_time_timsort(articles),
        "CombSort": measure_time_combsort(articles),
        "SelectionSort": measure_time_selectionsort(articles),
        "TreeSort": measure_time_treesort(articles),
        "BucketSort": measure_time_bucketsort(articles),
        "QuickSort": measure_time_quicksort(articles),
        "HeapSort": measure_time_heapsort(articles),
        "BitonicSort": measure_time_bitonicsort(articles),
        "GnomeSort": measure_time_gnomesort(articles),
        "BinaryInsertionSort": measure_time_binaryinsertionsort(articles),
        "RadixSort": measure_time_radixsort(articles),
        "PigeonholeSort": measure_time_pigeonholesort(articles)
    }
    
    # 📌 Imprimir resultados
    print(f"N = {N}")
    for key, value in tiempos.items():
        print(f"Tiempo {key} = {value} ms")
    
    # 📌 Generar gráfico
    plt.figure(figsize=(12, 6))
    plt.bar(tiempos.keys(), tiempos.values(), color='skyblue')
    plt.xlabel("Algoritmo de Ordenamiento")
    plt.ylabel("Tiempo de ejecución (ms)")
    plt.title(f"Tiempo de ejecución de algoritmos de ordenamiento para N = {N}")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()
    

 
    