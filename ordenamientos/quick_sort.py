def quick_sort(data):
    if len(data) <= 1:
        return data
    pivot = data[0]
    left = [x for x in data[1:] if (x[1], x[0]) > (pivot[1], pivot[0])]
    right = [x for x in data[1:] if (x[1], x[0]) <= (pivot[1], pivot[0])]
    return quick_sort(left) + [pivot] + quick_sort(right)
