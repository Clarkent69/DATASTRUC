def selectionSort(arr):
    nItems = len(arr)
    for current in range(nItems):
        min_index = current
        for search in range(current + 1, nItems):
            if arr[search] < arr[min_index]:
                min_index = search
        arr[current], arr[min_index] = arr[min_index], arr[current]
    return arr

sample_array = [64, 34, 25, 12, 22, 11, 90]
print(f"Original array: {sample_array}")
sorted_array = selectionSort(sample_array.copy())
print(f"Selection Sort result: {sorted_array}")