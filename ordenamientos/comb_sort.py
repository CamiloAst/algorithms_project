def comb_sort(data):
    gap = len(data)
    shrink = 1.3
    sorted_ = False
    while not sorted_:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_ = True
        i = 0
        while i + gap < len(data):
            if (data[i][1], data[i][0]) < (data[i + gap][1], data[i + gap][0]):
                data[i], data[i + gap] = data[i + gap], data[i]
                sorted_ = False
            i += 1
    return data
