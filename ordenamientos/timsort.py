def timsort(data):
    return sorted(data, key=lambda x: (-x[1], x[0]))
