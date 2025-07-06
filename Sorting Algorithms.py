# Extremely inefficient. moves an index right and sorts everything to th eleft of that index n times.
# Time complexity: O(n²) Space Complexity O(1)
def insertion_sort(arr):
    for i in range (1, len(arr)):
        key = arr[i]
        j - i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr
# --------------------------------------------------------------------------------------

# Select the smallest element in the array and place it in the first unsorted index. Repeat this process until the entire array is sorted.
# Time Complexity: O(n²) Space COmplexity: O(1)
def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        # Assume the current position holds the min element
        min_ndx = i
        
        # Iterate through the unsorted array to find the actual min element.
        for j in range(i + 1, n):
            if arr[j] < arr[i]:
                min_ndx = j
        # Move the min element to it's correct position.
        arr[i], arr[min_ndx] = arr[min_ndx], arr[i]
    return arr
# --------------------------------------------------------------------------------------

# Repeatedly swaps adjacent elements until the entire array is sorted. 
# Time Complexity: O(n²) Space COmplexity: O(1)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        
        for j in range(0, n-i-1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if swapped == False:
            break
    return arr
# --------------------------------------------------------------------------------------

# Recursively splits an array in half then sorts all halves in the form of a binary tree before merging and returning the result.
# Time Complexity: O(nlogn) Space complexity: O(n)
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1      
    result.extend(left[i:])
    result.extend(right[j:])
    return result
# --------------------------------------------------------------------------------------

# Rearrange array elements so that they form a Max Heap. 
# Once this is complete - swap the root element of the Max Heap with the last unsorted element of the array. repeat until completion.
# Time Complexity O(nlogn)2-3x slower than quick_sort  Space Complexity O(nlogn)
def heapify(arr, n, i):
    largest = i
    left = 2*i+1
    right = 2*i+2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
        
def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr,n,i)
    
    # One-by-one extract elements from the heap, move them to the end of the array, and call heapify on the reduced heap.
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr
# --------------------------------------------------------------------------------------

# Selects a pivot point, and partitions the array based on this. greater elements go right, smaller to the left. Recursively apply to completion.
# Time complexity O(nlogn) space complexity O(nlogn)
def quick_sort(arr):
    if (len(arr)) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]     
    return quick_sort(left) + middle + quick_sort(right)
# --------------------------------------------------------------------------------------

# distributes elements of an array into several groups and sorts those groups using either a different algorithm or this one recursively.
# time complexity O(n). Space Complexity O(n+k) k = # of buckets
def bucket_sort(arr):
    if not arr:
        return
    
    max_val, min_val = max(arr), min(arr)
    
    # create buckets
    bucket_range = (max_val - min_val) / len(arr)
    buckets = [[] for _ in range(len(arr) + 1)]
    
    # distribute array elements into buckets
    for i in arr:
        if i == max_val:
            bucket_ndx = len(arr) - 1
            
        else:
            bucket_ndx = int((i - min_val) / bucket_range)
        buckets[bucket_ndx].append(i)
        
    # sort individual buckets
    for bucket in buckets:
        bucket = quick_sort(bucket)
        
    result = []
    for b in buckets:
        result.extend(b)
        
    return result
# --------------------------------------------------------------------------------------

