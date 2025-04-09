def radix_sort(data):
    max_len = len(str(max(data, key=lambda x: x[1])[1]))
    for i in range(max_len):
        buckets = [[] for _ in range(10)]
        for item in data:
            digit = (item[1] // (10 ** i)) % 10
            buckets[digit].append(item)
        data = []
        for bucket in buckets:
            data.extend(bucket)
    return sorted(data, key=lambda x: (-x[1], x[0]))
