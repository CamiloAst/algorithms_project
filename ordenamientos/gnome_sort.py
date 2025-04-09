def gnome_sort(data):
    index = 0
    while index < len(data):
        if index == 0 or data[index][1] <= data[index - 1][1]:
            index += 1
        else:
            data[index], data[index - 1] = data[index - 1], data[index]
            index -= 1
    return sorted(data, key=lambda x: (-x[1], x[0]))
