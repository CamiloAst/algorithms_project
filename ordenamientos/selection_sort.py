def selection_sort(data):
    for i in range(len(data)):
        max_idx = i
        for j in range(i + 1, len(data)):
            if (data[j][1], data[j][0]) > (data[max_idx][1], data[max_idx][0]):
                max_idx = j
        data[i], data[max_idx] = data[max_idx], data[i]
    return data
