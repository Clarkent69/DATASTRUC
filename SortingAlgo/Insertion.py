def get_median(arr):
    sorted_arr = sorted(arr)
    nItems = len(sorted_arr)
    if nItems % 2 == 0:
        med = sorted_arr[nItems // 2]
    else:
        med = (sorted_arr[nItems // 2] + sorted_arr[nItems // 2 - 1]) / 2
    return med