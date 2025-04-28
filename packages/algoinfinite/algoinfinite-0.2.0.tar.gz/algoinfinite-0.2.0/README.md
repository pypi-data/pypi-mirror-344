# AlgoInfinite

[![PyPI version](https://img.shields.io/pypi/v/algoinfinite.svg)](https://pypi.org/project/algoinfinite/)
[![Python Versions](https://img.shields.io/pypi/pyversions/algoinfinite.svg)](https://pypi.org/project/algoinfinite/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive collection of algorithms and data structures implemented in Python. AlgoInfinite provides efficient implementations of common algorithms and data structures for educational purposes and practical applications.

## Features

- **Data Structures**: LinkedList, Stack, Queue, Binary Trees, and more
- **Sorting Algorithms**: QuickSort, MergeSort, BubbleSort, etc.
- **Search Algorithms**: Binary Search, Linear Search, etc.
- **Graph Algorithms**: Shortest Path, Minimum Spanning Tree, etc.
- **Mathematical Algorithms**: Prime Number generation, GCD calculation, etc.

## Installation

Install the latest version of AlgoInfinite from PyPI:

```bash
pip install algoinfinite
```

### Usage
Basic Import
```python
# Import specific components
from algoinfinite.data_structures import LinkedList, Stack
from algoinfinite.algorithms.sorting import quicksort, mergesort

# Or import everything (not recommended for production code)
from algoinfinite import *
```
Data Structure Exaxmple
```python
from algoinfinite.data_structures import LinkedList

# Create a linked list
my_list = LinkedList()
my_list.append(1)
my_list.append(2)
my_list.append(3)

# Display the list
print(my_list.display())  # Output: [1, 2, 3]
```
Algorithms Example
```python
from algoinfinite.algorithms.sorting import quicksort

# Sort an array
unsorted_array = [3, 1, 4, 1, 5, 9, 2, 6, 5]
sorted_array = quicksort(unsorted_array)

print(sorted_array)  # Output: [1, 1, 2, 3, 4, 5, 5, 6, 9]
```
### Command Line Interface (CLI)
AlgoInfinite also provides a command line interface for quick access to algorithms and data structures. You can run the following command to see the available options:

```bash
# Display a greeting message
madan-hello

# More tools will be added soon
```
## Documentation

Comprehensive documentation will be available soon at [https://algoinfinite.readthedocs.io](https://algoinfinite.readthedocs.io)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Madan Mohan Behera - [GitHub](https://github.com/Madan1500) - [Email](mailto:madanmohan14072002@gmail.com)

---

Made with ❤️ by Madan Mohan Behera
