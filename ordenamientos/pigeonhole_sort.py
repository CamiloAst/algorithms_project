def pigeonhole_sort(data):
    min_val = min(data, key=lambda x: x[1])[1]
    max_val = max(data, key=lambda x: x[1])[1]
    size = max_val - min_val + 1
    holes = [[] for _ in range(size)]
    for item in data:
        holes[item[1] - min_val].append(item)
    result = []
    for freq in reversed(holes):
        result.extend(sorted(freq, key=lambda x: x[0]))
    return result
