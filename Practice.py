#Linear search
#Basic search algorithm

def linear_search(lyst, target):
    for index, value in enumerate(lyst):
        if value == target:
            return index
    return -1

# USING LYST COMPREHENSIONS, GENERATE A LIST THAT CONTAINS THE INTEGERS 1 TO 100
sample_lyst = [i for i in range(1, 101)]
search_item = 100
print(f"item to find: {search_item}")
print(f"List {sample_lyst}")
position = linear_search(sample_lyst, search_item)
if position != -1:
    print(f"Item is located at index {position}")
else:
    print("item is not in the list")