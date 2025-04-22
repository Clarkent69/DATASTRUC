def binary_search(lyst, target):
    comp_count = 0
    lo = 0
    hi = len(lyst) - 1
    while lo <= hi:
        comp_count = comp_count + 1
        mid = lo + hi // 2
        mid_value = lyst[mid]
        if lyst[mid] == target:
            print(f"Binary Search Comparison count {comp_count}")
            return mid
        if lyst[mid] > target:
            hi = mid - 1
        else:
            lo = mid + 1
    print(f"Binary Search Comparison count {comp_count}")
    return -1

sample_lyst = [i for i in range(1, 101)]
search_item = 100
print("\n Using Binary Search: ")
print(f"item to find: {search_item}")
print(f"List {sample_lyst}")
position2 = binary_search(sample_lyst, search_item)
if position2 != -1:
    print(f"Item is located at index {position2}")
else:
    print("item is not in the list")