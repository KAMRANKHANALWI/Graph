"""
Basic Graph Operations
======================
Essential operations you'll need for any graph algorithm.
"""


def create_empty_graph():
    """Create an empty graph using adjacency list"""
    return {}


def add_node(graph, node):
    """Add a node to the graph"""
    if node not in graph:
        graph[node] = []
        print(f"✓ Added node {node}")
    else:
        print(f"⚠ Node {node} already exists")


def add_edge(graph, from_node, to_node):
    """Add an edge from from_node to to_node"""
    # Ensure both nodes exist
    add_node(graph, from_node)
    add_node(graph, to_node)

    # Add edge
    if to_node not in graph[from_node]:
        graph[from_node].append(to_node)
        print(f"✓ Added edge {from_node} → {to_node}")
    else:
        print(f"⚠ Edge {from_node} → {to_node} already exists")


def remove_edge(graph, from_node, to_node):
    """Remove an edge between two nodes"""
    if from_node in graph and to_node in graph[from_node]:
        graph[from_node].remove(to_node)
        print(f"✓ Removed edge {from_node} → {to_node}")
    else:
        print(f"⚠ Edge {from_node} → {to_node} does not exist")


def remove_node(graph, node):
    """Remove a node and all its connections"""
    if node not in graph:
        print(f"⚠ Node {node} does not exist")
        return

    # Remove the node
    del graph[node]

    # Remove all edges pointing to this node
    for other_node in graph:
        if node in graph[other_node]:
            graph[other_node].remove(node)

    print(f"✓ Removed node {node} and all its connections")


def has_edge(graph, from_node, to_node):
    """Check if an edge exists between two nodes"""
    return from_node in graph and to_node in graph[from_node]


def get_neighbors(graph, node):
    """Get all neighbors (outgoing connections) of a node"""
    return graph.get(node, [])


def get_incoming_neighbors(graph, node):
    """Get all nodes that point TO this node"""
    incoming = []
    for other_node, neighbors in graph.items():
        if node in neighbors:
            incoming.append(other_node)
    return incoming


def get_node_degree(graph, node):
    """Get degree of a node (number of connections)"""
    outgoing = len(graph.get(node, []))
    incoming = len(get_incoming_neighbors(graph, node))
    return {
        "out_degree": outgoing,
        "in_degree": incoming,
        "total_degree": outgoing + incoming,
    }


def get_all_nodes(graph):
    """Get all nodes in the graph"""
    nodes = set(graph.keys())
    # Also include nodes that are referenced but not keys
    for neighbors in graph.values():
        nodes.update(neighbors)
    return list(nodes)


def get_all_edges(graph):
    """Get all edges as a list of [from, to] pairs"""
    edges = []
    for from_node, neighbors in graph.items():
        for to_node in neighbors:
            edges.append([from_node, to_node])
    return edges


def graph_statistics(graph):
    """Get basic statistics about the graph"""
    nodes = get_all_nodes(graph)
    edges = get_all_edges(graph)

    stats = {
        "num_nodes": len(nodes),
        "num_edges": len(edges),
        "nodes": sorted(nodes),
        "edges": edges,
    }

    # Find isolated nodes (no connections)
    isolated = []
    for node in nodes:
        if not graph.get(node, []) and not get_incoming_neighbors(graph, node):
            isolated.append(node)
    stats["isolated_nodes"] = isolated

    # Find sink nodes (no outgoing edges)
    sinks = [node for node in nodes if not graph.get(node, [])]
    stats["sink_nodes"] = sinks

    # Find source nodes (no incoming edges)
    sources = [node for node in nodes if not get_incoming_neighbors(graph, node)]
    stats["source_nodes"] = sources

    return stats


def print_graph(graph, title="Graph"):
    """Pretty print the graph"""
    print(f"\n=== {title} ===")
    if not graph:
        print("  (empty graph)")
        return

    for node in sorted(graph.keys()):
        neighbors = graph[node]
        if neighbors:
            connections = " → ".join(map(str, sorted(neighbors)))
            print(f"  {node}: {neighbors}")
            print(f"      {node} → {connections}")
        else:
            print(f"  {node}: [] (no outgoing connections)")


def demonstrate_operations():
    """Demonstrate all basic operations"""
    print("🚀 DEMONSTRATING BASIC GRAPH OPERATIONS")
    print("=" * 50)

    # Create empty graph
    graph = create_empty_graph()
    print("Created empty graph")

    # Add nodes and edges
    print("\n--- Adding nodes and edges ---")
    add_node(graph, 0)
    add_node(graph, 1)
    add_node(graph, 2)

    add_edge(graph, 0, 1)
    add_edge(graph, 0, 2)
    add_edge(graph, 1, 2)

    print_graph(graph, "After adding nodes and edges")

    # Check connections
    print("\n--- Checking connections ---")
    print(f"Edge 0→1 exists? {has_edge(graph, 0, 1)}")
    print(f"Edge 1→0 exists? {has_edge(graph, 1, 0)}")
    print(f"Neighbors of 0: {get_neighbors(graph, 0)}")
    print(f"Nodes pointing to 2: {get_incoming_neighbors(graph, 2)}")

    # Node degrees
    print("\n--- Node degrees ---")
    for node in get_all_nodes(graph):
        degree_info = get_node_degree(graph, node)
        print(f"Node {node}: {degree_info}")

    # Graph statistics
    print("\n--- Graph statistics ---")
    stats = graph_statistics(graph)
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Remove operations
    print("\n--- Removing edges and nodes ---")
    remove_edge(graph, 0, 1)
    print_graph(graph, "After removing edge 0→1")

    remove_node(graph, 1)
    print_graph(graph, "After removing node 1")

    # Final statistics
    print("\n--- Final statistics ---")
    final_stats = graph_statistics(graph)
    for key, value in final_stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    demonstrate_operations()

    print("\n✅ You now know all basic graph operations!")
    print("🎯 Next: Learn about the Graph class for better organization")
