def bitonic_sort(data):
    def comp_and_swap(a, i, j, dir):
        if (dir == 1 and a[i][1] > a[j][1]) or (dir == 0 and a[i][1] < a[j][1]):
            a[i], a[j] = a[j], a[i]
    def bitonic_merge(a, low, cnt, dir):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                comp_and_swap(a, i, i + k, dir)
            bitonic_merge(a, low, k, dir)
            bitonic_merge(a, low + k, k, dir)
    def bitonic_sort_rec(a, low, cnt, dir):
        if cnt > 1:
            k = cnt // 2
            bitonic_sort_rec(a, low, k, 1)
            bitonic_sort_rec(a, low + k, k, 0)
            bitonic_merge(a, low, cnt, dir)
    a = data[:]
    bitonic_sort_rec(a, 0, len(a), 1)
    return list(reversed(a))
