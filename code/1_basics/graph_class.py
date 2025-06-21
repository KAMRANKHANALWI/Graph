"""
Graph Class Implementation
==========================
A clean, reusable Graph class that you can use in all your projects.
"""


class Graph:
    """
    A simple Graph class using adjacency list representation.
    Supports both directed and undirected graphs.
    """

    def __init__(self, directed=True):
        """
        Initialize an empty graph.

        Args:
            directed (bool): If True, creates directed graph. If False, undirected.
        """
        self.adjacency_list = {}
        self.directed = directed

    def add_node(self, node):
        """Add a node to the graph."""
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            return True
        return False

    def add_edge(self, from_node, to_node):
        """Add an edge between two nodes."""
        # Ensure both nodes exist
        self.add_node(from_node)
        self.add_node(to_node)

        # Add edge from_node -> to_node
        if to_node not in self.adjacency_list[from_node]:
            self.adjacency_list[from_node].append(to_node)

            # If undirected, add reverse edge too
            if not self.directed:
                self.adjacency_list[to_node].append(from_node)

            return True
        return False

    def remove_edge(self, from_node, to_node):
        """Remove an edge between two nodes."""
        if self.has_edge(from_node, to_node):
            self.adjacency_list[from_node].remove(to_node)

            # If undirected, remove reverse edge too
            if not self.directed and self.has_edge(to_node, from_node):
                self.adjacency_list[to_node].remove(from_node)

            return True
        return False

    def remove_node(self, node):
        """Remove a node and all its connections."""
        if node not in self.adjacency_list:
            return False

        # Remove the node
        del self.adjacency_list[node]

        # Remove all edges pointing to this node
        for other_node in self.adjacency_list:
            if node in self.adjacency_list[other_node]:
                self.adjacency_list[other_node].remove(node)

        return True

    def has_edge(self, from_node, to_node):
        """Check if an edge exists between two nodes."""
        return (
            from_node in self.adjacency_list
            and to_node in self.adjacency_list[from_node]
        )

    def get_neighbors(self, node):
        """Get all neighbors of a node."""
        return self.adjacency_list.get(node, [])

    def get_nodes(self):
        """Get all nodes in the graph."""
        nodes = set(self.adjacency_list.keys())
        # Include nodes that are referenced but not keys
        for neighbors in self.adjacency_list.values():
            nodes.update(neighbors)
        return list(nodes)

    def get_edges(self):
        """Get all edges as a list of tuples."""
        edges = []
        for from_node, neighbors in self.adjacency_list.items():
            for to_node in neighbors:
                edges.append((from_node, to_node))
        return edges

    def get_degree(self, node):
        """Get the degree of a node."""
        if node not in self.get_nodes():
            return 0

        out_degree = len(self.adjacency_list.get(node, []))

        # Count incoming edges
        in_degree = 0
        for other_node, neighbors in self.adjacency_list.items():
            if node in neighbors:
                in_degree += 1

        if self.directed:
            return {"in": in_degree, "out": out_degree, "total": in_degree + out_degree}
        else:
            # For undirected graphs, in_degree = out_degree
            return out_degree

    def is_connected(self):
        """Check if the graph is connected (undirected) or strongly connected (directed)."""
        nodes = self.get_nodes()
        if not nodes:
            return True

        # Use DFS to check connectivity
        visited = set()
        self._dfs(nodes[0], visited)

        return len(visited) == len(nodes)

    def _dfs(self, node, visited):
        """Helper method for DFS traversal."""
        visited.add(node)
        for neighbor in self.get_neighbors(node):
            if neighbor not in visited:
                self._dfs(neighbor, visited)

    def dfs(self, start_node, visited=None):
        """Depth-First Search traversal."""
        if visited is None:
            visited = set()

        result = []
        if start_node not in visited:
            visited.add(start_node)
            result.append(start_node)

            for neighbor in self.get_neighbors(start_node):
                result.extend(self.dfs(neighbor, visited))

        return result

    def bfs(self, start_node):
        """Breadth-First Search traversal."""
        from collections import deque

        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def find_path(self, start, end):
        """Find a path between two nodes using BFS."""
        from collections import deque

        if start == end:
            return [start]

        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            node, path = queue.popleft()

            for neighbor in self.get_neighbors(node):
                if neighbor == end:
                    return path + [neighbor]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None  # No path found

    def __str__(self):
        """String representation of the graph."""
        if not self.adjacency_list:
            return "Empty Graph"

        result = f"{'Directed' if self.directed else 'Undirected'} Graph:\n"
        for node in sorted(self.adjacency_list.keys()):
            neighbors = self.adjacency_list[node]
            if neighbors:
                result += f"  {node} → {sorted(neighbors)}\n"
            else:
                result += f"  {node} → []\n"
        return result.strip()

    def __repr__(self):
        """Representation of the graph."""
        return f"Graph(directed={self.directed}, nodes={len(self.get_nodes())}, edges={len(self.get_edges())})"


def demonstrate_graph_class():
    """Demonstrate the Graph class with examples."""
    print("🚀 DEMONSTRATING GRAPH CLASS")
    print("=" * 40)

    # Create directed graph
    print("--- Creating Directed Graph ---")
    directed_graph = Graph(directed=True)

    # Add nodes and edges
    directed_graph.add_edge(0, 1)
    directed_graph.add_edge(0, 2)
    directed_graph.add_edge(1, 2)
    directed_graph.add_edge(2, 3)

    print(directed_graph)
    print(f"Representation: {repr(directed_graph)}")

    # Graph operations
    print("\n--- Graph Operations ---")
    print(f"Nodes: {directed_graph.get_nodes()}")
    print(f"Edges: {directed_graph.get_edges()}")
    print(f"Neighbors of 0: {directed_graph.get_neighbors(0)}")
    print(f"Degree of node 2: {directed_graph.get_degree(2)}")
    print(f"Has edge 0→1: {directed_graph.has_edge(0, 1)}")
    print(f"Has edge 1→0: {directed_graph.has_edge(1, 0)}")

    # Traversals
    print("\n--- Traversals ---")
    print(f"DFS from 0: {directed_graph.dfs(0)}")
    print(f"BFS from 0: {directed_graph.bfs(0)}")
    print(f"Path from 0 to 3: {directed_graph.find_path(0, 3)}")
    print(f"Path from 3 to 0: {directed_graph.find_path(3, 0)}")

    # Create undirected graph
    print("\n--- Creating Undirected Graph ---")
    undirected_graph = Graph(directed=False)

    # Add same edges - but now they're bidirectional
    undirected_graph.add_edge("A", "B")
    undirected_graph.add_edge("B", "C")
    undirected_graph.add_edge("C", "D")
    undirected_graph.add_edge("A", "D")

    print(undirected_graph)

    # Show bidirectional nature
    print(f"A→B exists: {undirected_graph.has_edge('A', 'B')}")
    print(f"B→A exists: {undirected_graph.has_edge('B', 'A')}")
    print(f"Degree of A: {undirected_graph.get_degree('A')}")

    # Test connectivity
    print(f"Is connected: {undirected_graph.is_connected()}")

    # Path finding in undirected graph
    print(f"Path A to D: {undirected_graph.find_path('A', 'D')}")


def friendship_network_example():
    """Create the friendship network using Graph class."""
    print("\n🤝 FRIENDSHIP NETWORK EXAMPLE")
    print("=" * 40)

    # Create undirected graph for friendships
    friends = Graph(directed=False)

    # Add friendships from your original example
    friendships = [
        ("Kamran", "Asad"),
        ("Kamran", "Shabab"),
        ("Kamran", "Saad"),
        ("Asad", "Shadman"),
        ("Shabab", "Zeeshan"),
        ("Saad", "Zeeshan"),
    ]

    for person1, person2 in friendships:
        friends.add_edge(person1, person2)

    print("Friendship Network:")
    print(friends)

    # Find connections
    print("\n--- Friend Analysis ---")
    print(f"Kamran's friends: {friends.get_neighbors('Kamran')}")
    print(f"Zeeshan's friends: {friends.get_neighbors('Zeeshan')}")
    print(f"Path from Shadman to Zeeshan: {friends.find_path('Shadman', 'Zeeshan')}")

    # Find mutual friends (intersection of friend lists)
    kamran_friends = set(friends.get_neighbors("Kamran"))
    asad_friends = set(friends.get_neighbors("Asad"))
    mutual = kamran_friends.intersection(asad_friends)
    print(f"Mutual friends of Kamran and Asad: {list(mutual)}")


if __name__ == "__main__":
    demonstrate_graph_class()
    friendship_network_example()

    print("\n✅ You now have a complete Graph class!")
    print("🎯 Next: Learn graph traversal algorithms (DFS, BFS)")
    print("💡 You can use this Graph class in all your future projects!")
