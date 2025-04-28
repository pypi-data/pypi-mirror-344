"""
Searching algorithms implementation for AlgoInfinite.

This module provides various searching algorithms with different time and
space complexities for different use cases.
"""

import math

def linear_search(arr, target):
    """
    Linear Search algorithm implementation.
    
    Sequentially checks each element of the list until a match is found.
    
    Time Complexity:
        - Best: O(1) when the target is at the beginning
        - Average: O(n)
        - Worst: O(n) when the target is at the end or not present
    Space Complexity: O(1)
    
    Args:
        arr (list): The input array to search in
        target: The value to search for
        
    Returns:
        int: Index of the target if found, -1 otherwise
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr, target):
    """
    Binary Search algorithm implementation.
    
    Requires a sorted array. Repeatedly divides the search interval in half.
    
    Time Complexity:
        - Best: O(1) when the target is in the middle
        - Average: O(log n)
        - Worst: O(log n)
    Space Complexity: 
        - Iterative: O(1)
    
    Args:
        arr (list): The sorted input array to search in
        target: The value to search for
        
    Returns:
        int: Index of the target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        # Check if target is at the middle
        if arr[mid] == target:
            return mid
        
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        
        # If target is smaller, ignore right half
        else:
            right = mid - 1
    
    # Target is not present in the array
    return -1

def binary_search_recursive(arr, target):
    """
    Recursive Binary Search algorithm implementation.
    
    Requires a sorted array. Repeatedly divides the search interval in half.
    
    Time Complexity:
        - Best: O(1) when the target is in the middle
        - Average: O(log n)
        - Worst: O(log n)
    Space Complexity: 
        - Recursive: O(log n) due to recursion stack
    
    Args:
        arr (list): The sorted input array to search in
        target: The value to search for
        
    Returns:
        int: Index of the target if found, -1 otherwise
    """
    def _binary_search(arr, left, right, target):
        if right >= left:
            mid = left + (right - left) // 2
            
            # Check if target is at the middle
            if arr[mid] == target:
                return mid
            
            # If target is smaller, search in left subarray
            elif arr[mid] > target:
                return _binary_search(arr, left, mid - 1, target)
            
            # If target is larger, search in right subarray
            else:
                return _binary_search(arr, mid + 1, right, target)
        else:
            # Target is not present in the array
            return -1
    
    return _binary_search(arr, 0, len(arr) - 1, target)

def interpolation_search(arr, target):
    """
    Interpolation Search algorithm implementation.
    
    Requires a sorted array. Improves on binary search by using position formula.
    Works best on uniformly distributed data.
    
    Time Complexity:
        - Best: O(1)
        - Average: O(log log n) for uniformly distributed data
        - Worst: O(n) when data is not uniformly distributed
    Space Complexity: O(1)
    
    Args:
        arr (list): The sorted input array to search in
        target: The value to search for
        
    Returns:
        int: Index of the target if found, -1 otherwise
    """
    low, high = 0, len(arr) - 1
    
    while low <= high and target >= arr[low] and target <= arr[high]:
        # Check for division by zero
        if arr[high] == arr[low]:
            if arr[low] == target:
                return low
            return -1
        
        # Calculate probe position using interpolation formula
        pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])
        
        # Target found
        if arr[pos] == target:
            return pos
        
        # If target is larger, search in right subarray
        elif arr[pos] < target:
            low = pos + 1
        
        # If target is smaller, search in left subarray
        else:
            high = pos - 1
    
    # Target is not present in the array
    return -1

def jump_search(arr, target):
    """
    Jump Search algorithm implementation.
    
    Requires a sorted array. Jumps ahead by fixed steps and then
    uses linear search to find the element.
    
    Time Complexity:
        - Best: O(1) when target is at the beginning
        - Average: O(√n)
        - Worst: O(√n)
    Space Complexity: O(1)
    
    Args:
        arr (list): The sorted input array to search in
        target: The value to search for
        
    Returns:
        int: Index of the target if found, -1 otherwise
    """
    n = len(arr)
    
    # Finding optimal jump step size
    step = int(math.sqrt(n))
    
    # Finding the block where the target may be present
    prev = 0
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    
    # Linear search in the identified block
    while arr[prev] < target:
        prev += 1
        
        # If we reach next block or end of array, target not present
        if prev == min(step, n):
            return -1
    
    # If target is found
    if arr[prev] == target:
        return prev
    
    # Target not found
    return -1

def exponential_search(arr, target):
    """
    Exponential Search algorithm implementation.
    
    Requires a sorted array. Searches for range where target may be present,
    then uses binary search in that range.
    
    Time Complexity:
        - Best: O(1) when target is at the beginning
        - Average: O(log n)
        - Worst: O(log n)
    Space Complexity: O(1)
    
    Args:
        arr (list): The sorted input array to search in
        target: The value to search for
        
    Returns:
        int: Index of the target if found, -1 otherwise
    """
    n = len(arr)
    
    # If target is at first position
    if arr[0] == target:
        return 0
    
    # Find range for binary search by doubling
    i = 1
    while i < n and arr[i] <= target:
        i = i * 2
    
    # Call binary search for the found range
    def _binary_search(arr, left, right, target):
        if right >= left:
            mid = left + (right - left) // 2
            
            # Check if target is at the middle
            if arr[mid] == target:
                return mid
            
            # If target is smaller, search in left subarray
            elif arr[mid] > target:
                return _binary_search(arr, left, mid - 1, target)
            
            # If target is larger, search in right subarray
            else:
                return _binary_search(arr, mid + 1, right, target)
        else:
            # Target is not present in the array
            return -1
    
    # Perform binary search for selected range
    return _binary_search(arr, i // 2, min(i, n - 1), target)

# List of available searching algorithms
__all__ = [
    'linear_search',
    'binary_search',
    'binary_search_recursive',
    'interpolation_search',
    'jump_search',
    'exponential_search'
]