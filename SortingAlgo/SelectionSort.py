def selectionSort(arr):
    nItems = len(arr)
    for outer in range(nItems):
        min = outer
        for inner in range(outer + 1, nItems):
            if arr[inner] < arr[min]:
                min = inner
                
        arr[outer], arr[min] = arr[min], arr[outer]
    return arr

sample_array = [64, 34, 25, 12, 22, 11, 90]
print(f"Original array: {sample_array}")
sorted_array = selectionSort(sample_array)
print(f"Selection Sort result: {sorted_array}")