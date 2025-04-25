def Insertion_Sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def main():
    A = [55, 26, 9, 1, 5, 678, 0, 2, 3]
    print("Original array:", A)
    sorted_array = Insertion_Sort(A.copy())
    print("Insertion array:", sorted_array)

if __name__ == "__main__":
    main()