def insertion_sort(arr):
    nItems = len(arr)
    for i in range(1, nItems):
        j = i
        while j > 0 and arr[j - 1] > arr[j]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1
    return arr

def get_median(arr):
    sorted_arr = sorted(arr)
    nItems = len(sorted_arr)
    if nItems % 2 == 0:
        mid1 = sorted_arr[nItems // 2 - 1]
        mid2 = sorted_arr[nItems // 2]
        med = (mid1 + mid2) / 2
    else:
        med = sorted_arr[nItems // 2]
    return med

sample_array = [64, 56, 25, 12, 22, 11, 90]
print(f"Original array: {sample_array}")
sorted_insertion = insertion_sort(sample_array)
print(f"Insertion Sorted: {sorted_insertion}")
med = get_median(sample_array)
print(f"Median: {med}")