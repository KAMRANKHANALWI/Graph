"""
Complete Guide to Graph Representations
=======================================
Learn all three ways to represent graphs with examples and conversions.
"""


def edge_list_example():
    """
    Edge List: Simple list of connections
    Each [a, b] represents an edge from node a to node b
    """
    print("=== EDGE LIST REPRESENTATION ===")
    edges = [
        [0, 1],  # Node 0 connects to Node 1
        [0, 3],  # Node 0 connects to Node 3
        [1, 2],  # Node 1 connects to Node 2
        [3, 4],  # Node 3 connects to Node 4
    ]

    print(f"Edges: {edges}")
    print("\nVisualization:")
    print("    0 ——————→ 1")
    print("    |         |")
    print("    |         ↓")
    print("    ↓         2")
    print("    3 ——————→ 4")
    print("\nHow to read:")
    for edge in edges:
        print(f"  {edge} means: Node {edge[0]} connects to Node {edge[1]}")

    return edges


def adjacency_matrix_example():
    """
    Adjacency Matrix: 2D array where matrix[i][j] = 1 if edge exists
    """
    print("\n=== ADJACENCY MATRIX REPRESENTATION ===")

    # For nodes 0, 1, 2, 3, 4
    matrix = [
        [0, 1, 0, 1, 0],  # Node 0 connects to 1,3
        [0, 0, 1, 0, 0],  # Node 1 connects to 2
        [0, 0, 0, 0, 0],  # Node 2 connects to nothing
        [0, 0, 0, 0, 1],  # Node 3 connects to 4
        [0, 0, 0, 0, 0],  # Node 4 connects to nothing
    ]

    print("Matrix (1=connected, 0=not connected):")
    print("     To→  0  1  2  3  4")
    for i, row in enumerate(matrix):
        print(f"From {i}  {row}")

    print("\nHow to read:")
    print("  matrix[0][1] = 1 means: Node 0 connects to Node 1")
    print("  matrix[2][0] = 0 means: Node 2 does NOT connect to Node 0")

    return matrix


def adjacency_list_example():
    """
    Adjacency List: Dictionary where key=node, value=list of neighbors
    Most popular representation!
    """
    print("\n=== ADJACENCY LIST REPRESENTATION ===")

    graph = {
        0: [1, 3],  # Node 0 connects to 1,3
        1: [2],  # Node 1 connects to 2
        2: [],  # Node 2 connects to nothing
        3: [4],  # Node 3 connects to 4
        4: [],  # Node 4 connects to nothing
    }

    print("Graph as dictionary:")
    for node, neighbors in graph.items():
        if neighbors:
            connections = " → ".join(map(str, neighbors))
            print(f"  {node}: {neighbors}  (goes to: {connections})")
        else:
            print(f"  {node}: {neighbors}  (no outgoing connections)")

    return graph


def convert_representations():
    """
    Show how to convert between different representations
    """
    print("\n=== CONVERTING BETWEEN REPRESENTATIONS ===")

    # Start with edge list
    edges = [[0, 1], [0, 3], [1, 2], [3, 4]]
    print(f"Original edge list: {edges}")

    # Convert to adjacency list
    from collections import defaultdict

    adj_list = defaultdict(list)
    for u, v in edges:
        adj_list[u].append(v)
    adj_list = dict(adj_list)

    print(f"Converted to adjacency list: {adj_list}")

    # Convert adjacency list back to edge list
    new_edges = []
    for node, neighbors in adj_list.items():
        for neighbor in neighbors:
            new_edges.append([node, neighbor])

    print(f"Back to edge list: {new_edges}")


def practical_operations():
    """
    Common operations you'll do with graphs
    """
    print("\n=== PRACTICAL OPERATIONS ===")

    graph = {0: [1, 3], 1: [2], 2: [], 3: [4], 4: []}

    print(f"Graph: {graph}")

    # Check if edge exists
    def has_edge(graph, from_node, to_node):
        return to_node in graph.get(from_node, [])

    print(f"\nEdge 0→1 exists? {has_edge(graph, 0, 1)}")
    print(f"Edge 1→0 exists? {has_edge(graph, 1, 0)}")

    # Get all neighbors
    def get_neighbors(graph, node):
        return graph.get(node, [])

    print(f"\nNeighbors of node 0: {get_neighbors(graph, 0)}")
    print(f"Neighbors of node 2: {get_neighbors(graph, 2)}")

    # Count total edges
    total_edges = sum(len(neighbors) for neighbors in graph.values())
    print(f"\nTotal edges in graph: {total_edges}")

    # Find nodes with no outgoing edges (sinks)
    sinks = [node for node, neighbors in graph.items() if not neighbors]
    print(f"Sink nodes (no outgoing edges): {sinks}")


def comparison_table():
    """
    When to use each representation
    """
    print("\n=== WHEN TO USE EACH REPRESENTATION ===")
    print("┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐")
    print("│ Representation  │ Space Complexity│ Edge Check      │ Best For        │")
    print("├─────────────────┼─────────────────┼─────────────────┼─────────────────┤")
    print("│ Edge List       │ O(E)            │ O(E)            │ Simple input    │")
    print("│ Adjacency Matrix│ O(V²)           │ O(1)            │ Dense graphs    │")
    print("│ Adjacency List  │ O(V + E)        │ O(degree)       │ Most algorithms │")
    print("└─────────────────┴─────────────────┴─────────────────┴─────────────────┘")
    print("\nV = number of vertices/nodes, E = number of edges")


if __name__ == "__main__":
    print("🚀 COMPLETE GUIDE TO GRAPH REPRESENTATIONS")
    print("=" * 50)

    # Show all three representations
    edges = edge_list_example()
    matrix = adjacency_matrix_example()
    adj_list = adjacency_list_example()

    # Show conversions
    convert_representations()

    # Show practical operations
    practical_operations()

    # Show comparison
    comparison_table()

    print("\n✅ You now understand all graph representations!")
    print("🎯 Next: Learn graph traversal algorithms (DFS, BFS)")
