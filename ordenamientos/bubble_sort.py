def bubble_sort(data):
    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            if (data[j][1], data[j][0]) < (data[j + 1][1], data[j + 1][0]):
                data[j], data[j + 1] = data[j + 1], data[j]
    return data
