"""
Connected Components in Graphs
==============================
Find all connected components (isolated groups) in graphs.
"""

from collections import deque


def find_connected_components_dfs(graph):
    """
    Find all connected components using DFS
    Returns list of components, each component is a list of nodes
    """
    print("🏝️ FINDING CONNECTED COMPONENTS (DFS)")
    print("=" * 40)

    visited = set()
    components = []

    def dfs_component(node, current_component):
        visited.add(node)
        current_component.append(node)
        print(f"    Added {node} to component")

        # Visit all unvisited neighbors
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs_component(neighbor, current_component)

    # Check each node
    for node in graph:
        if node not in visited:
            print(f"\n  Starting new component from {node}:")
            current_component = []
            dfs_component(node, current_component)
            components.append(sorted(current_component))
            print(f"  Component {len(components)}: {sorted(current_component)}")

    return components


def find_connected_components_bfs(graph):
    """
    Find all connected components using BFS
    Alternative approach - same result, different traversal
    """
    print("🏝️ FINDING CONNECTED COMPONENTS (BFS)")
    print("=" * 40)

    visited = set()
    components = []

    def bfs_component(start_node):
        component = []
        queue = deque([start_node])
        visited.add(start_node)

        while queue:
            node = queue.popleft()
            component.append(node)
            print(f"    Added {node} to component")

            # Add all unvisited neighbors to queue
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return sorted(component)

    # Check each node
    for node in graph:
        if node not in visited:
            print(f"\n  Starting new component from {node}:")
            component = bfs_component(node)
            components.append(component)
            print(f"  Component {len(components)}: {component}")

    return components


def analyze_graph_connectivity(graph):
    """
    Comprehensive analysis of graph connectivity
    """
    print("📊 GRAPH CONNECTIVITY ANALYSIS")
    print("=" * 35)

    components = find_connected_components_dfs(graph)

    print(f"\nAnalysis Results:")
    print(f"  Total nodes: {len(graph)}")
    print(f"  Total components: {len(components)}")
    print(f"  Is connected: {len(components) == 1}")

    if len(components) > 1:
        print(f"  Graph is DISCONNECTED")
        component_sizes = [len(comp) for comp in components]
        print(f"  Component sizes: {component_sizes}")
        print(f"  Largest component: {max(component_sizes)} nodes")
        print(f"  Smallest component: {min(component_sizes)} nodes")

        # Find isolated nodes (components of size 1)
        isolated = [comp[0] for comp in components if len(comp) == 1]
        if isolated:
            print(f"  Isolated nodes: {isolated}")
    else:
        print(f"  Graph is CONNECTED")

    return components


def union_find_components(graph):
    """
    Find connected components using Union-Find (Disjoint Set)
    Efficient for large sparse graphs
    """
    print("🔗 UNION-FIND CONNECTED COMPONENTS")
    print("=" * 38)

    # Union-Find data structure
    class UnionFind:
        def __init__(self, nodes):
            self.parent = {node: node for node in nodes}
            self.rank = {node: 0 for node in nodes}
            self.components = len(nodes)

        def find(self, node):
            if self.parent[node] != node:
                self.parent[node] = self.find(self.parent[node])  # Path compression
            return self.parent[node]

        def union(self, node1, node2):
            root1 = self.find(node1)
            root2 = self.find(node2)

            if root1 != root2:
                # Union by rank
                if self.rank[root1] < self.rank[root2]:
                    self.parent[root1] = root2
                elif self.rank[root1] > self.rank[root2]:
                    self.parent[root2] = root1
                else:
                    self.parent[root2] = root1
                    self.rank[root1] += 1

                self.components -= 1
                return True
            return False

    # Get all nodes
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    uf = UnionFind(all_nodes)

    print(f"Initial: {uf.components} components (each node isolated)")

    # Process all edges
    edges_processed = 0
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if uf.union(node, neighbor):
                edges_processed += 1
                print(f"  Merged components of {node} and {neighbor}")
                print(f"    Components remaining: {uf.components}")

    # Group nodes by their root
    component_map = {}
    for node in all_nodes:
        root = uf.find(node)
        if root not in component_map:
            component_map[root] = []
        component_map[root].append(node)

    components = [sorted(comp) for comp in component_map.values()]

    print(f"\nFinal: {len(components)} connected components")
    for i, comp in enumerate(components, 1):
        print(f"  Component {i}: {comp}")

    return components


def connectivity_metrics(graph):
    """
    Calculate various connectivity metrics
    """
    print("📈 CONNECTIVITY METRICS")
    print("=" * 25)

    components = find_connected_components_dfs(graph)

    # Basic metrics
    total_nodes = len(graph)
    num_components = len(components)
    is_connected = num_components == 1

    # Edge count
    total_edges = sum(len(neighbors) for neighbors in graph.values())
    if not is_directed_graph(graph):
        total_edges //= 2  # Each edge counted twice in undirected graph

    # Component size statistics
    component_sizes = [len(comp) for comp in components]
    largest_component_size = max(component_sizes) if component_sizes else 0

    # Connectivity metrics
    print(f"Basic Metrics:")
    print(f"  Nodes: {total_nodes}")
    print(f"  Edges: {total_edges}")
    print(f"  Components: {num_components}")
    print(f"  Is Connected: {is_connected}")

    print(f"\nComponent Analysis:")
    print(f"  Largest component: {largest_component_size} nodes")
    print(f"  Component sizes: {sorted(component_sizes, reverse=True)}")

    if not is_connected:
        connectivity_ratio = largest_component_size / total_nodes
        print(f"  Connectivity ratio: {connectivity_ratio:.2f}")

        isolated_nodes = len([comp for comp in components if len(comp) == 1])
        print(f"  Isolated nodes: {isolated_nodes}")


def is_directed_graph(graph):
    """Check if graph is directed by looking for asymmetric edges"""
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor in graph and node not in graph[neighbor]:
                return True
    return False


def practical_connectivity_examples():
    """
    Real-world examples of connectivity analysis
    """
    print("🌍 PRACTICAL CONNECTIVITY EXAMPLES")
    print("=" * 40)

    # Example 1: Social Network Groups
    print("Example 1: Social Network Friend Groups")
    print("-" * 40)

    social_network = {
        # Group 1: School friends
        "Alice": ["Bob", "Carol"],
        "Bob": ["Alice", "Carol"],
        "Carol": ["Alice", "Bob"],
        # Group 2: Work colleagues
        "David": ["Eve", "Frank"],
        "Eve": ["David", "Frank"],
        "Frank": ["David", "Eve"],
        # Isolated person
        "Grace": [],
    }

    print("Social network:")
    for person, friends in social_network.items():
        print(f"  {person}: {friends}")

    components = analyze_graph_connectivity(social_network)

    if len(components) == 1:
        print("✅ All people are connected (directly or indirectly)")
    else:
        print("❌ People form separate groups")
        for i, group in enumerate(components, 1):
            print(f"   Group {i}: {group}")

    # Example 2: Website Link Structure
    print(f"\nExample 2: Website Link Structure")
    print("-" * 35)

    website_links = {
        "home": ["about", "products", "contact"],
        "about": ["home", "team"],
        "products": ["home", "product1", "product2"],
        "contact": ["home"],
        "team": ["about"],
        "product1": ["products"],
        "product2": ["products"],
        "blog": ["blog_post1"],  # Isolated blog section
        "blog_post1": ["blog"],
    }

    print("Website structure:")
    for page, links in website_links.items():
        print(f"  {page}: {links}")

    components = analyze_graph_connectivity(website_links)
    print("🌐 Website connectivity analysis:")

    if len(components) > 1:
        main_site = max(components, key=len)
        isolated_sections = [comp for comp in components if comp != main_site]

        print(f"   Main site: {main_site}")
        print(f"   Isolated sections: {isolated_sections}")
        print("   ⚠️ Some pages are unreachable from main navigation!")
    else:
        print("   ✅ All pages are connected through navigation")


def performance_comparison():
    """
    Compare performance of different connected component algorithms
    """
    print("\n⚡ ALGORITHM PERFORMANCE COMPARISON")
    print("=" * 40)

    print(
        """
ALGORITHM COMPARISON:
━━━━━━━━━━━━━━━━━━━━━

1. 🔍 DFS Approach
   Time: O(V + E)
   Space: O(V)
   ✅ Simple to implement
   ✅ Natural recursion
   ✅ Works for directed/undirected
   ❌ Stack overflow risk (deep recursion)

2. 🌊 BFS Approach  
   Time: O(V + E)
   Space: O(V)
   ✅ No recursion depth issues
   ✅ Level-by-level exploration
   ✅ Works for directed/undirected
   ❌ Slightly more memory for queue

3. 🔗 Union-Find
   Time: O(E α(V)) where α is inverse Ackermann
   Space: O(V)
   ✅ Very efficient for sparse graphs
   ✅ Incremental (can add edges dynamically)
   ✅ Path compression optimization
   ❌ More complex to implement
   ❌ Only works for undirected graphs

WHEN TO USE EACH:
━━━━━━━━━━━━━━━━━

• Small/Medium graphs → DFS/BFS (easier)
• Large sparse graphs → Union-Find
• Dynamic edge additions → Union-Find
• Need component traversal → DFS/BFS
• Directed graphs → DFS/BFS only
"""
    )


def connectivity_algorithms_cheatsheet():
    """
    Quick reference for connectivity algorithms
    """
    print("\n📋 CONNECTIVITY ALGORITHMS CHEATSHEET")
    print("=" * 45)

    print(
        """
QUICK IMPLEMENTATIONS:
━━━━━━━━━━━━━━━━━━━━━━

# Find Connected Components (DFS):
def find_components(graph):
    visited, components = set(), []
    
    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)
    
    return components

# Check if Graph is Connected:
def is_connected(graph):
    if not graph: return True
    start = next(iter(graph))
    visited = set()
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
    
    dfs(start)
    return len(visited) == len(graph)

# Union-Find for Dynamic Connectivity:
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True
"""
    )


if __name__ == "__main__":
    # Test with a disconnected graph
    test_graph = {
        # Component 1
        0: [1, 2],
        1: [0, 2],
        2: [0, 1],
        # Component 2
        3: [4],
        4: [3, 5],
        5: [4],
        # Isolated node
        6: [],
        # Component 3
        7: [8],
        8: [7],
    }

    print("🔍 CONNECTED COMPONENTS ANALYSIS")
    print("=" * 40)
    print(f"Test graph: {test_graph}")

    # Analyze connectivity
    analyze_graph_connectivity(test_graph)

    print("\n" + "=" * 60)

    # Compare DFS vs BFS
    print("Comparing DFS vs BFS approaches:")
    dfs_components = find_connected_components_dfs(test_graph)
    print(f"DFS result: {dfs_components}")

    bfs_components = find_connected_components_bfs(test_graph)
    print(f"BFS result: {bfs_components}")
    print(f"Results match: {sorted(dfs_components) == sorted(bfs_components)}")

    print("\n" + "=" * 60)

    # Union-Find approach
    union_find_components(test_graph)

    print("\n" + "=" * 60)

    # Practical examples
    practical_connectivity_examples()

    # Performance comparison
    performance_comparison()

    # Cheatsheet
    connectivity_algorithms_cheatsheet()

    print("\n✅ You now master connected components!")
    print("🎯 Next: Learn shortest path algorithms")
    print(
        "💡 Key takeaway: Use DFS/BFS for most cases, Union-Find for dynamic scenarios!"
    )
