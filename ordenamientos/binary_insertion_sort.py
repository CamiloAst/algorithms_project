def binary_insertion_sort(data):
    def binary_search(arr, val, start, end):
        while start < end:
            mid = (start + end) // 2
            if (arr[mid][1], arr[mid][0]) < (val[1], val[0]):
                start = mid + 1
            else:
                end = mid
        return start
    for i in range(1, len(data)):
        val = data[i]
        j = binary_search(data, val, 0, i)
        data = data[:j] + [val] + data[j:i] + data[i+1:]
    return data
