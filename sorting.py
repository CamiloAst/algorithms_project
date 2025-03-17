import bisect


def tim_sort(arr):
    return sorted(arr)


def comb_sort(arr):
    gap = len(arr)
    shrink = 1.3
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        while i + gap < len(arr):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
            i += 1
    return arr


def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def tree_sort(arr):
    class Node:
        def __init__(self, key):
            self.left = self.right = None
            self.val = key

    def insert(root, key):
        if root is None:
            return Node(key)
        if key < root.val:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
        return root

    def inorder(root, sorted_list):
        if root:
            inorder(root.left, sorted_list)
            sorted_list.append(root.val)
            inorder(root.right, sorted_list)

    if not arr:
        return arr
    root = None
    for num in arr:
        root = insert(root, num)
    sorted_list = []
    inorder(root, sorted_list)
    return sorted_list


def pigeonhole_sort(arr):
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    holes = [[] for _ in range(size)]
    for x in arr:
        holes[x - min_val].append(x)
    i = 0
    for bucket in holes:
        for x in bucket:
            arr[i] = x
            i += 1
    return arr


def bucket_sort(arr):
    max_value = max(arr)
    size = max_value // len(arr)
    buckets = [[] for _ in range(len(arr))]
    for i in arr:
        j = i // size
        if j != len(arr):
            buckets[j].append(i)
        else:
            buckets[len(arr) - 1].append(i)
    for bucket in buckets:
        bucket.sort()
    return [x for bucket in buckets for x in bucket]


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr):
    import heapq
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]


def bitonic_sort(arr):
    def comp_and_swap(a, i, j, direction):
        if (direction == 1 and a[i] > a[j]) or (direction == 0 and a[i] < a[j]):
            a[i], a[j] = a[j], a[i]

    def bitonic_merge(a, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                comp_and_swap(a, i, i + k, direction)
            bitonic_merge(a, low, k, direction)
            bitonic_merge(a, low + k, k, direction)

    def bitonic_sort_helper(a, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            bitonic_sort_helper(a, low, k, 1)
            bitonic_sort_helper(a, low + k, k, 0)
            bitonic_merge(a, low, cnt, direction)

    n = len(arr)
    bitonic_sort_helper(arr, 0, n, 1)
    return arr


def gnome_sort(arr):
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr


def binary_insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        pos = bisect.bisect_left(arr[:i], key)
        arr = arr[:pos] + [key] + arr[pos:i] + arr[i + 1:]
    return arr


def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr


def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    for i in range(n):
        arr[i] = output[i]
    return arr
