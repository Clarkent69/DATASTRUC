def bubbleSort(arr):
    nItems = len(arr)
    for last in range(nItems):
        for inner in range(last):
            if arr[inner] > arr[inner + 1]:
                arr[inner], arr[inner + 1] = arr[inner + 1], arr[inner]
    return arr

sample_array = [64, 34, 25, 12, 22, 11, 90]
print(f"Original array: {sample_array}")
sorted_array = bubbleSort(sample_array)
print(f"Bubble Sort result: {sorted_array}")