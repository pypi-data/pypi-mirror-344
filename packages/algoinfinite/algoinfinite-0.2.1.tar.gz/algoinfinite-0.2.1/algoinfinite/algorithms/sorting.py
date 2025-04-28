"""
Sorting algorithms implementation for AlgoInfinite.

This module provides various sorting algorithms with different time and
space complexities for different use cases.
"""

def bubble_sort(arr):
    """
    Bubble Sort algorithm implementation.
    
    Time Complexity:
        - Best: O(n) when array is already sorted
        - Average: O(n²)
        - Worst: O(n²)
    Space Complexity: O(1)
    
    Args:
        arr (list): The input array to be sorted
        
    Returns:
        list: The sorted array
    """
    n = len(arr)
    # Create a copy of the array to avoid modifying the original
    result = arr.copy()
    
    for i in range(n):
        # Flag to optimize if no swaps are made in a pass
        swapped = False
        
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        
        # If no swaps were made in this pass, array is sorted
        if not swapped:
            break
    
    return result

def insertion_sort(arr):
    """
    Insertion Sort algorithm implementation.
    
    Time Complexity:
        - Best: O(n) when array is already sorted
        - Average: O(n²)
        - Worst: O(n²)
    Space Complexity: O(1)
    
    Args:
        arr (list): The input array to be sorted
        
    Returns:
        list: The sorted array
    """
    result = arr.copy()
    
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        
        # Move elements greater than key one position ahead
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        
        result[j + 1] = key
    
    return result

def selection_sort(arr):
    """
    Selection Sort algorithm implementation.
    
    Time Complexity:
        - Best: O(n²)
        - Average: O(n²)
        - Worst: O(n²)
    Space Complexity: O(1)
    
    Args:
        arr (list): The input array to be sorted
        
    Returns:
        list: The sorted array
    """
    result = arr.copy()
    n = len(result)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if result[j] < result[min_idx]:
                min_idx = j
        
        # Swap the minimum element with the first element
        result[i], result[min_idx] = result[min_idx], result[i]
    
    return result

def merge_sort(arr):
    """
    Merge Sort algorithm implementation.
    
    Time Complexity:
        - Best: O(n log n)
        - Average: O(n log n)
        - Worst: O(n log n)
    Space Complexity: O(n)
    
    Args:
        arr (list): The input array to be sorted
        
    Returns:
        list: The sorted array
    """
    if len(arr) <= 1:
        return arr.copy()
    
    def merge(left, right):
        """Merge two sorted arrays."""
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
    
    # Split array into halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    # Merge sorted halves
    return merge(left_half, right_half)

def quicksort(arr):
    """
    QuickSort algorithm implementation.
    
    Time Complexity:
        - Best: O(n log n)
        - Average: O(n log n)
        - Worst: O(n²) when array is already sorted
    Space Complexity: O(log n) due to recursion stack
    
    Args:
        arr (list): The input array to be sorted
        
    Returns:
        list: The sorted array
    """
    # Create a copy of the array to avoid modifying the original
    result = arr.copy()
    
    def _quicksort(arr, low, high):
        if low < high:
            # Partition the array and get pivot position
            pivot_idx = partition(arr, low, high)
            
            # Sort elements before and after partition
            _quicksort(arr, low, pivot_idx - 1)
            _quicksort(arr, pivot_idx + 1, high)
    
    def partition(arr, low, high):
        # Choose rightmost element as pivot
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        # Place pivot in its final position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    if len(result) > 1:
        _quicksort(result, 0, len(result) - 1)
    
    return result

def heap_sort(arr):
    """
    Heap Sort algorithm implementation.
    
    Time Complexity:
        - Best: O(n log n)
        - Average: O(n log n)
        - Worst: O(n log n)
    Space Complexity: O(1)
    
    Args:
        arr (list): The input array to be sorted
        
    Returns:
        list: The sorted array
    """
    result = arr.copy()
    n = len(result)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(result, n, i)
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        result[0], result[i] = result[i], result[0]  # Swap
        heapify(result, i, 0)
    
    return result

def heapify(arr, n, i):
    """
    Helper function to maintain heap property.
    
    Args:
        arr (list): The array being heapified
        n (int): Size of the heap
        i (int): Index of the root of the subtree being heapified
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # Check if right child exists and is greater than root
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # Change root if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

# List of available sorting algorithms
__all__ = [
    'bubble_sort',
    'insertion_sort',
    'selection_sort',
    'merge_sort',
    'quicksort',
    'heap_sort'
]