import heapq

def heap_sort(data):
    heap = [(-v, k) for k, v in data]
    heapq.heapify(heap)
    return [(k, -v) for v, k in [heapq.heappop(heap) for _ in range(len(heap))]]
