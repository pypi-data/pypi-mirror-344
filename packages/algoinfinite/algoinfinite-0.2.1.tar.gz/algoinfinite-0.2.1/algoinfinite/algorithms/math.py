"""
Mathematical algorithms implementation for AlgoInfinite.

This module provides various mathematical algorithms including prime number operations,
number theory functions, combinatorial algorithms, and numerical methods.
"""

import math

def is_prime(n):
    """
    Check if a number is prime.
    
    Time Complexity: O(sqrt(n))
    Space Complexity: O(1)
    
    Args:
        n (int): The number to check
        
    Returns:
        bool: True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True

def sieve_of_eratosthenes(n):
    """
    Generate all prime numbers up to n using the Sieve of Eratosthenes algorithm.
    
    Time Complexity: O(n log log n)
    Space Complexity: O(n)
    
    Args:
        n (int): Upper limit for prime generation
        
    Returns:
        list: List of prime numbers less than or equal to n
    """
    if n < 2:
        return []
    
    # Initialize sieve array
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    
    # Mark non-primes using Sieve algorithm
    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            # Mark all multiples of i as non-prime
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    
    # Collect primes
    return [i for i in range(2, n + 1) if sieve[i]]

def gcd(a, b):
    """
    Calculate the Greatest Common Divisor (GCD) of two numbers using Euclidean algorithm.
    
    Time Complexity: O(log(min(a, b)))
    Space Complexity: O(log(min(a, b))) due to recursion
    
    Args:
        a (int): First number
        b (int): Second number
        
    Returns:
        int: The GCD of a and b
    """
    if b == 0:
        return abs(a)
    return gcd(b, a % b)

def lcm(a, b):
    """
    Calculate the Least Common Multiple (LCM) of two numbers.
    
    Time Complexity: O(log(min(a, b)))
    Space Complexity: O(log(min(a, b))) due to recursion in GCD
    
    Args:
        a (int): First number
        b (int): Second number
        
    Returns:
        int: The LCM of a and b
    """
    return abs(a * b) // gcd(a, b) if a and b else 0

def factorial(n):
    """
    Calculate the factorial of a non-negative integer.
    
    Time Complexity: O(n)
    Space Complexity: O(1) [O(n) if considering the size of the result]
    
    Args:
        n (int): Non-negative integer
        
    Returns:
        int: The factorial of n
    """
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result

def fibonacci(n):
    """
    Calculate the nth Fibonacci number using dynamic programming.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed)
        
    Returns:
        int: The nth Fibonacci number
    """
    if n < 0:
        raise ValueError("Fibonacci not defined for negative indices")
    
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b

def binomial_coefficient(n, k):
    """
    Calculate the binomial coefficient C(n, k), also known as "n choose k".
    
    Time Complexity: O(k)
    Space Complexity: O(1)
    
    Args:
        n (int): Total number of items
        k (int): Number of items to choose
        
    Returns:
        int: The binomial coefficient C(n, k)
    """
    if k < 0 or k > n:
        return 0
    
    if k > n - k:
        k = n - k  # Optimization: C(n, k) = C(n, n-k)
    
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    
    return result

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm to find coefficients x, y such that ax + by = gcd(a, b).
    
    Time Complexity: O(log(min(a, b)))
    Space Complexity: O(log(min(a, b))) due to recursion
    
    Args:
        a (int): First number
        b (int): Second number
        
    Returns:
        tuple: (gcd, x, y) where ax + by = gcd
    """
    if a == 0:
        return (b, 0, 1)
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return (gcd, x, y)

def modular_inverse(a, m):
    """
    Find the modular multiplicative inverse of 'a' under modulo 'm'.
    
    Time Complexity: O(log m)
    Space Complexity: O(log m) due to recursion in extended_gcd
    
    Args:
        a (int): Number to find inverse for
        m (int): Modulo
        
    Returns:
        int: The modular inverse of a under modulo m, or -1 if it doesn't exist
    """
    g, x, y = extended_gcd(a, m)
    
    if g != 1:
        # Modular inverse doesn't exist
        return -1
    else:
        # Make sure the result is positive
        return (x % m + m) % m

def is_perfect_square(n):
    """
    Check if a number is a perfect square.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        n (int): Number to check
        
    Returns:
        bool: True if n is a perfect square, False otherwise
    """
    if n < 0:
        return False
    
    sqrt_n = int(math.sqrt(n))
    return sqrt_n * sqrt_n == n

def prime_factorization(n):
    """
    Find the prime factorization of a number.
    
    Time Complexity: O(sqrt(n))
    Space Complexity: O(log n) for the result
    
    Args:
        n (int): Number to factorize
        
    Returns:
        dict: Dictionary mapping prime factors to their exponents
    """
    if n <= 1:
        return {}
    
    factors = {}
    
    # Check 2 separately to optimize loop
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    
    # Check odd numbers up to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
    
    # If n is a prime greater than 2
    if n > 2:
        factors[n] = factors.get(n, 0) + 1
    
    return factors

def euler_totient(n):
    """
    Calculate Euler's totient function φ(n), which counts numbers up to n
    that are relatively prime to n.
    
    Time Complexity: O(sqrt(n))
    Space Complexity: O(1)
    
    Args:
        n (int): Positive integer
        
    Returns:
        int: Value of φ(n)
    """
    if n <= 0:
        raise ValueError("Totient function defined only for positive integers")
    
    result = n  # Initialize result as n
    
    # Consider all prime factors of n and subtract their multiples
    p = 2
    while p * p <= n:
        # Check if p is a prime factor
        if n % p == 0:
            # If yes, then update n and result
            while n % p == 0:
                n //= p
            
            result -= result // p
        
        p += 1
    
    # If n has a prime factor greater than sqrt(n)
    if n > 1:
        result -= result // n
    
    return result

def matrix_multiply(A, B):
    """
    Multiply two matrices A and B.
    
    Time Complexity: O(n^3) where n is the matrix dimension
    Space Complexity: O(n^2) for the result matrix
    
    Args:
        A (list): Matrix represented as list of lists
        B (list): Matrix represented as list of lists
        
    Returns:
        list: The product matrix of A and B
    """
    if not A or not B or not A[0] or not B[0]:
        raise ValueError("Input matrices cannot be empty")
    
    n_rows_A, n_cols_A = len(A), len(A[0])
    n_rows_B, n_cols_B = len(B), len(B[0])
    
    if n_cols_A != n_rows_B:
        raise ValueError(f"Matrix dimensions don't match for multiplication: {n_cols_A} != {n_rows_B}")
    
    # Initialize result matrix with zeros
    result = [[0 for _ in range(n_cols_B)] for _ in range(n_rows_A)]
    
    # Perform multiplication
    for i in range(n_rows_A):
        for j in range(n_cols_B):
            for k in range(n_cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def matrix_power(A, n):
    """
    Raise matrix A to the power of n using exponentiation by squaring.
    
    Time Complexity: O(m^3 * log n) where m is the matrix dimension
    Space Complexity: O(m^2) for intermediate matrices
    
    Args:
        A (list): Square matrix represented as list of lists
        n (int): Power to raise the matrix to
        
    Returns:
        list: Matrix A raised to power n
    """
    if not A or not A[0]:
        raise ValueError("Input matrix cannot be empty")
    
    if len(A) != len(A[0]):
        raise ValueError("Matrix must be square for power operation")
    
    if n < 0:
        raise ValueError("Negative powers not implemented")
    
    if n == 0:
        # Return identity matrix
        size = len(A)
        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    
    if n == 1:
        # Return a copy of A
        return [row[:] for row in A]
    
    # Exponentiation by squaring
    if n % 2 == 0:
        half_power = matrix_power(A, n // 2)
        return matrix_multiply(half_power, half_power)
    else:
        half_power = matrix_power(A, (n - 1) // 2)
        return matrix_multiply(matrix_multiply(half_power, half_power), A)

# List of available mathematical algorithms
__all__ = [
    'is_prime',
    'sieve_of_eratosthenes',
    'gcd',
    'lcm',
    'factorial',
    'fibonacci',
    'binomial_coefficient',
    'extended_gcd',
    'modular_inverse',
    'is_perfect_square',
    'prime_factorization',
    'euler_totient',
    'matrix_multiply',
    'matrix_power'
]