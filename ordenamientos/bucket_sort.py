def bucket_sort(data):
    max_val = max(data, key=lambda x: x[1])[1]
    size = max_val // 10 + 1
    buckets = [[] for _ in range(size)]
    for item in data:
        buckets[item[1] // 10].append(item)
    result = []
    for b in reversed(buckets):
        result.extend(sorted(b, key=lambda x: (-x[1], x[0])))
    return result
