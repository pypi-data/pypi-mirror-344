"""
Graph algorithms implementation for AlgoInfinite.

This module provides various graph algorithms for operations like traversal,
shortest path finding, minimum spanning tree, cycle detection, etc.
"""

from collections import defaultdict, deque
import heapq

def breadth_first_search(graph, start):
    """
    Breadth-First Search (BFS) algorithm implementation.
    
    Time Complexity: O(V + E) where V is the number of vertices and E is the number of edges
    Space Complexity: O(V)
    
    Args:
        graph (dict): A dictionary representing an adjacency list of the graph
        start: The starting vertex
        
    Returns:
        list: The BFS traversal order
    """
    if start not in graph:
        return []
    
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result

def depth_first_search(graph, start):
    """
    Depth-First Search (DFS) algorithm implementation.
    
    Time Complexity: O(V + E) where V is the number of vertices and E is the number of edges
    Space Complexity: O(V)
    
    Args:
        graph (dict): A dictionary representing an adjacency list of the graph
        start: The starting vertex
        
    Returns:
        list: The DFS traversal order
    """
    if start not in graph:
        return []
    
    visited = set()
    result = []
    
    def dfs_recursive(vertex):
        visited.add(vertex)
        result.append(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs_recursive(neighbor)
    
    dfs_recursive(start)
    return result

def dijkstra(graph, start):
    """
    Dijkstra's algorithm for finding the shortest paths from a source vertex.
    
    Time Complexity: O((V + E) log V) with a binary heap
    Space Complexity: O(V)
    
    Args:
        graph (dict): A dictionary representing a weighted adjacency list where
                    graph[u] is a list of tuples (v, weight)
        start: The starting vertex
        
    Returns:
        dict: Dictionary of shortest distances from the start vertex to all others
    """
    if start not in graph:
        return {}
    
    # Initialize distances
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    
    # Priority queue for vertices to visit next
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # If we already found a shorter path, skip
        if current_distance > distances[current_vertex]:
            continue
        
        # Check neighbors
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            
            # If we found a shorter path to the neighbor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def bellman_ford(graph, start, vertices):
    """
    Bellman-Ford algorithm for finding shortest paths from a source vertex.
    Can handle negative edge weights and detect negative weight cycles.
    
    Time Complexity: O(V * E) where V is the number of vertices and E is the number of edges
    Space Complexity: O(V)
    
    Args:
        graph (list): A list of edges where each edge is a tuple (u, v, weight)
        start: The starting vertex
        vertices (set): Set of all vertices in the graph
        
    Returns:
        tuple: (distances, bool) - Dictionary of shortest distances and whether a negative cycle exists
    """
    # Initialize distances
    distances = {vertex: float('infinity') for vertex in vertices}
    distances[start] = 0
    
    # Relax edges repeatedly
    for _ in range(len(vertices) - 1):
        for u, v, weight in graph:
            if distances[u] != float('infinity') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
    
    # Check for negative weight cycles
    for u, v, weight in graph:
        if distances[u] != float('infinity') and distances[u] + weight < distances[v]:
            return distances, True  # Negative cycle exists
    
    return distances, False

def kruskal_mst(graph, vertices):
    """
    Kruskal's algorithm for finding the Minimum Spanning Tree (MST) of a graph.
    
    Time Complexity: O(E log E) or O(E log V) where E is the number of edges and V is the number of vertices
    Space Complexity: O(V + E)
    
    Args:
        graph (list): A list of edges where each edge is a tuple (u, v, weight)
        vertices (set): Set of all vertices in the graph
        
    Returns:
        list: The edges in the MST
    """
    # Sort edges by weight
    graph.sort(key=lambda x: x[2])
    
    # Initialize disjoint set
    parent = {vertex: vertex for vertex in vertices}
    rank = {vertex: 0 for vertex in vertices}
    
    def find(vertex):
        """Find operation with path compression."""
        if parent[vertex] != vertex:
            parent[vertex] = find(parent[vertex])
        return parent[vertex]
    
    def union(u, v):
        """Union by rank."""
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            if rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                if rank[root_u] == rank[root_v]:
                    rank[root_u] += 1
    
    mst = []
    
    for u, v, weight in graph:
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, weight))
            
            # If MST is complete
            if len(mst) == len(vertices) - 1:
                break
    
    return mst

def prim_mst(graph, start):
    """
    Prim's algorithm for finding the Minimum Spanning Tree (MST) of a graph.
    
    Time Complexity: O((V + E) log V) with a binary heap
    Space Complexity: O(V + E)
    
    Args:
        graph (dict): A dictionary representing a weighted adjacency list where
                    graph[u] is a list of tuples (v, weight)
        start: The starting vertex
        
    Returns:
        list: The edges in the MST
    """
    if start not in graph:
        return []
    
    # Track visited vertices
    visited = {start}
    
    # Edge heap: (weight, u, v)
    edge_heap = [(weight, start, v) for v, weight in graph[start]]
    heapq.heapify(edge_heap)
    
    mst = []
    
    while edge_heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(edge_heap)
        
        if v not in visited:
            visited.add(v)
            mst.append((u, v, weight))
            
            # Add edges from the newly visited vertex
            for neighbor, w in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(edge_heap, (w, v, neighbor))
    
    return mst

def topological_sort(graph):
    """
    Topological sorting algorithm for directed acyclic graphs (DAG).
    
    Time Complexity: O(V + E) where V is the number of vertices and E is the number of edges
    Space Complexity: O(V)
    
    Args:
        graph (dict): A dictionary representing an adjacency list of the directed graph
        
    Returns:
        list: A topological ordering of vertices, or empty list if a cycle exists
    """
    # Track visited nodes and recursion stack
    visited = set()
    temp = set()
    result = []
    
    def visit(vertex):
        # If vertex is already in recursion stack, cycle exists
        if vertex in temp:
            return False
        
        # If already processed, skip
        if vertex in visited:
            return True
        
        # Mark vertex as part of current recursion
        temp.add(vertex)
        
        # Visit neighbors
        for neighbor in graph.get(vertex, []):
            if not visit(neighbor):
                return False
        
        # Remove from recursion stack and mark as processed
        temp.remove(vertex)
        visited.add(vertex)
        
        # Add to result in reverse order
        result.append(vertex)
        return True
    
    # Visit all vertices
    for vertex in graph:
        if vertex not in visited:
            if not visit(vertex):
                return []  # Cycle detected
    
    # Return reversed result for correct topological order
    return result[::-1]

def detect_cycle_undirected(graph):
    """
    Cycle detection in an undirected graph.
    
    Time Complexity: O(V + E) where V is the number of vertices and E is the number of edges
    Space Complexity: O(V)
    
    Args:
        graph (dict): A dictionary representing an adjacency list of the undirected graph
        
    Returns:
        bool: True if a cycle exists, False otherwise
    """
    visited = set()
    
    def dfs(vertex, parent):
        visited.add(vertex)
        
        for neighbor in graph.get(vertex, []):
            # Skip the parent (we came from there)
            if neighbor == parent:
                continue
            
            # If already visited, we found a cycle
            if neighbor in visited:
                return True
            
            # Recursive DFS
            if dfs(neighbor, vertex):
                return True
        
        return False
    
    # Check all components
    for vertex in graph:
        if vertex not in visited:
            if dfs(vertex, None):
                return True
    
    return False

def detect_cycle_directed(graph):
    """
    Cycle detection in a directed graph.
    
    Time Complexity: O(V + E) where V is the number of vertices and E is the number of edges
    Space Complexity: O(V)
    
    Args:
        graph (dict): A dictionary representing an adjacency list of the directed graph
        
    Returns:
        bool: True if a cycle exists, False otherwise
    """
    # Track visited and recursion stack
    visited = set()
    rec_stack = set()
    
    def dfs(vertex):
        visited.add(vertex)
        rec_stack.add(vertex)
        
        for neighbor in graph.get(vertex, []):
            # If not visited, recurse
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            # If in recursion stack, cycle exists
            elif neighbor in rec_stack:
                return True
        
        # Remove from recursion stack
        rec_stack.remove(vertex)
        return False
    
    # Check all components
    for vertex in graph:
        if vertex not in visited:
            if dfs(vertex):
                return True
    
    return False

def strongly_connected_components(graph):
    """
    Kosaraju's algorithm for finding strongly connected components in a directed graph.
    
    Time Complexity: O(V + E) where V is the number of vertices and E is the number of edges
    Space Complexity: O(V)
    
    Args:
        graph (dict): A dictionary representing an adjacency list of the directed graph
        
    Returns:
        list: List of strongly connected components (each component is a list of vertices)
    """
    # Create reversed graph
    reversed_graph = defaultdict(list)
    for u in graph:
        for v in graph.get(u, []):
            reversed_graph[v].append(u)
    
    # First DFS to get the finish order
    visited = set()
    finish_order = []
    
    def dfs_finish(vertex):
        visited.add(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs_finish(neighbor)
        finish_order.append(vertex)
    
    # Run first DFS
    for vertex in graph:
        if vertex not in visited:
            dfs_finish(vertex)
    
    # Second DFS on reversed graph in finish order
    visited.clear()
    components = []
    
    def dfs_component(vertex, component):
        visited.add(vertex)
        component.append(vertex)
        for neighbor in reversed_graph.get(vertex, []):
            if neighbor not in visited:
                dfs_component(neighbor, component)
    
    # Process vertices in reverse finish order
    for vertex in reversed(finish_order):
        if vertex not in visited:
            component = []
            dfs_component(vertex, component)
            components.append(component)
    
    return components

# List of available graph algorithms
__all__ = [
    'breadth_first_search',
    'depth_first_search',
    'dijkstra',
    'bellman_ford',
    'kruskal_mst',
    'prim_mst',
    'topological_sort',
    'detect_cycle_undirected',
    'detect_cycle_directed',
    'strongly_connected_components'
]