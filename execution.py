import time
import random

A = []
for i in range(1, 10000):
    A.append(random.randint(1, 10000))
    
def insertion_sort(A):
    start = time.time()
    for i in range(1, len(A)):
        key = A[i]
        j = i - 1
        while j >= 0 and key < A[j]:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key
    end = time.time()
    print("Time Elapsed: ", end - start)
insertion_sort(A)