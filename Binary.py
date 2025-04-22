def binary_search(lyst, target):
    lo = 0
    hi = len(lyst) - 1
    while lo <= hi:
        mid = lo + hi // 2
        mid_value = lyst[mid]
        if lyst[mid] == target:
            return mid
        if lyst[mid] > target:
            hi = mid - 1
        else:
            lo = mid + 1
    return -1