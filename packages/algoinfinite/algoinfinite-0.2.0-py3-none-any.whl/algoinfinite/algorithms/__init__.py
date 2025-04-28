"""
Algorithm collection for AlgoInfinite.
"""

from .sorting import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    merge_sort,
    quicksort,
    heap_sort
)
from .searching import (
    linear_search,
    binary_search,
    binary_search_recursive,
    interpolation_search,
    jump_search,
    exponential_search
)
from .graph import (
    breadth_first_search,
    depth_first_search,
    dijkstra,
    bellman_ford,
    kruskal_mst,
    prim_mst,
    topological_sort,
    detect_cycle_undirected,
    detect_cycle_directed,
    strongly_connected_components
)
from .math import (
    is_prime,
    sieve_of_eratosthenes,
    gcd,
    lcm,
    factorial,
    fibonacci,
    binomial_coefficient,
    extended_gcd,
    modular_inverse,
    is_perfect_square,
    prime_factorization,
    euler_totient,
    matrix_multiply,
    matrix_power
)

__all__ = [
    # Sorting algorithms
    'bubble_sort',
    'insertion_sort',
    'selection_sort',
    'merge_sort',
    'quicksort',
    'heap_sort',
    
    # Searching algorithms
    'linear_search',
    'binary_search',
    'binary_search_recursive',
    'interpolation_search',
    'jump_search',
    'exponential_search',

    # Graph algorithms
    'breadth_first_search',
    'depth_first_search',
    'dijkstra',
    'bellman_ford',
    'kruskal_mst',
    'prim_mst',
    'topological_sort',
    'detect_cycle_undirected',
    'detect_cycle_directed',
    'strongly_connected_components',

    # Math algorithms
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
    'matrix_power',
]