def insertion_sort(arr):
    nItems = len(arr)
    for i in range(1, nItems):
        j= i
        while j > 0 and arr[j-1] > arr[j]:
            arr[j], arr[j-1] = arr[j-1], arr[j]
            j -= 1
        return arr

def get_median(arr):
    sorted_arr = sorted(arr)
    nItems = len(sorted_arr)
    if nItems % 2 == 0:
        med = sorted_arr[nItems // 2]
    else:
        med = (sorted_arr[nItems // 2] + sorted_arr[nItems // 2 - 1]) / 2
    return med