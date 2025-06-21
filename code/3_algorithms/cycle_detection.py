"""
Cycle Detection in Graphs
=========================
Complete guide to detecting cycles in directed and undirected graphs.
"""


def detect_cycle_undirected_dfs(graph):
    """
    Detect cycle in undirected graph using DFS
    A cycle exists if we visit a node that's already visited (except parent)
    """
    print("🔄 CYCLE DETECTION IN UNDIRECTED GRAPH (DFS)")
    print("=" * 50)

    visited = set()

    def dfs_has_cycle(node, parent):
        visited.add(node)
        print(f"  Visiting: {node} (parent: {parent})")

        for neighbor in graph.get(node, []):
            print(f"    Checking neighbor: {neighbor}")

            if neighbor not in visited:
                print(f"      {neighbor} not visited, going deeper...")
                if dfs_has_cycle(neighbor, node):
                    return True
            elif neighbor != parent:
                print(
                    f"      🚨 CYCLE FOUND! {neighbor} already visited and not parent"
                )
                print(f"      Cycle involves: {parent} → {node} → {neighbor}")
                return True
            else:
                print(f"      {neighbor} is parent, skipping")

        print(f"  Finished exploring {node}")
        return False

    # Check all components (graph might be disconnected)
    for node in graph:
        if node not in visited:
            print(f"\nStarting DFS from {node}")
            if dfs_has_cycle(node, None):
                return True

    return False


def detect_cycle_directed_dfs(graph):
    """
    Detect cycle in directed graph using DFS with colors
    Uses 3-color approach: WHITE (unvisited), GRAY (visiting), BLACK (visited)
    """
    print("🔄 CYCLE DETECTION IN DIRECTED GRAPH (DFS)")
    print("=" * 50)

    WHITE, GRAY, BLACK = 0, 1, 2
    colors = {node: WHITE for node in graph}

    def dfs_has_cycle(node):
        colors[node] = GRAY  # Mark as currently being processed
        print(f"  Visiting: {node} (marked GRAY)")

        for neighbor in graph.get(node, []):
            print(
                f"    Checking neighbor: {neighbor} (color: {['WHITE', 'GRAY', 'BLACK'][colors[neighbor]]})"
            )

            if colors[neighbor] == GRAY:
                print(f"      🚨 BACK EDGE FOUND! Cycle detected: {node} → {neighbor}")
                return True
            elif colors[neighbor] == WHITE and dfs_has_cycle(neighbor):
                return True

        colors[node] = BLACK  # Mark as completely processed
        print(f"  Finished: {node} (marked BLACK)")
        return False

    # Check all nodes (might have multiple components)
    for node in graph:
        if colors[node] == WHITE:
            print(f"\nStarting DFS from {node}")
            if dfs_has_cycle(node):
                return True

    return False


def find_cycle_path_directed(graph):
    """
    Not only detect cycle but also return the actual cycle path
    """
    print("🎯 FINDING ACTUAL CYCLE PATH (Directed Graph)")
    print("=" * 45)

    WHITE, GRAY, BLACK = 0, 1, 2
    colors = {node: WHITE for node in graph}
    parent = {}

    def dfs_find_cycle(node, path):
        colors[node] = GRAY
        path.append(node)
        print(f"  Current path: {' → '.join(map(str, path))}")

        for neighbor in graph.get(node, []):
            if colors[neighbor] == GRAY:
                # Found back edge - extract cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                print(f"  🎉 CYCLE FOUND: {' → '.join(map(str, cycle))}")
                return cycle
            elif colors[neighbor] == WHITE:
                result = dfs_find_cycle(neighbor, path)
                if result:
                    return result

        colors[node] = BLACK
        path.pop()
        return None

    for node in graph:
        if colors[node] == WHITE:
            print(f"\nTrying from {node}:")
            cycle = dfs_find_cycle(node, [])
            if cycle:
                return cycle

    return None


def detect_cycle_using_topology(graph):
    """
    Detect cycle using Topological Sort (Kahn's Algorithm)
    If we can't sort all nodes topologically, there's a cycle
    """
    print("🔄 CYCLE DETECTION USING TOPOLOGICAL SORT")
    print("=" * 45)

    from collections import deque, defaultdict

    # Calculate in-degrees
    in_degree = defaultdict(int)
    for node in graph:
        in_degree[node] = 0

    for node in graph:
        for neighbor in graph.get(node, []):
            in_degree[neighbor] += 1

    print("In-degrees:", dict(in_degree))

    # Find nodes with no incoming edges
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    processed = 0

    print(f"Starting with nodes having in-degree 0: {list(queue)}")

    while queue:
        node = queue.popleft()
        processed += 1
        print(f"  Processing: {node} (total processed: {processed})")

        # Remove this node and update in-degrees
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            print(f"    Reduced in-degree of {neighbor} to {in_degree[neighbor]}")
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                print(f"    Added {neighbor} to queue")

    total_nodes = len(graph)
    has_cycle = processed != total_nodes

    print(f"\nResult: Processed {processed} out of {total_nodes} nodes")
    print(f"Has cycle: {has_cycle}")

    if has_cycle:
        unprocessed = [node for node in graph if in_degree[node] > 0]
        print(f"Nodes in cycle(s): {unprocessed}")

    return has_cycle


def practical_cycle_examples():
    """
    Show practical examples where cycle detection is important
    """
    print("💼 PRACTICAL CYCLE DETECTION EXAMPLES")
    print("=" * 40)

    # Example 1: Dependency Resolution
    print("Example 1: Package Dependency Cycles")
    print("-" * 35)

    dependencies = {
        "app": ["database", "auth"],
        "database": ["config"],
        "auth": ["database", "crypto"],
        "config": ["logger"],
        "crypto": ["config"],
        "logger": [],
    }

    print("Dependencies:")
    for package, deps in dependencies.items():
        if deps:
            print(f"  {package} depends on: {deps}")
        else:
            print(f"  {package} has no dependencies")

    has_cycle = detect_cycle_directed_dfs(dependencies)
    print(f"✅ Dependency cycle detected: {has_cycle}")

    if not has_cycle:
        print("✅ Dependencies can be resolved in order!")
    else:
        print("❌ Circular dependency! Cannot resolve.")

    # Example 2: Deadlock Detection
    print(f"\nExample 2: Deadlock Detection in Resource Allocation")
    print("-" * 55)

    # Process → Resource allocation graph
    resource_allocation = {
        "Process1": ["Resource2"],  # P1 wants R2
        "Process2": ["Resource1"],  # P2 wants R1
        "Resource1": ["Process1"],  # R1 allocated to P1
        "Resource2": ["Process2"],  # R2 allocated to P2
    }

    print("Resource allocation:")
    for entity, allocations in resource_allocation.items():
        print(f"  {entity} → {allocations}")

    print("\nThis represents:")
    print("  Process1 holds Resource1, wants Resource2")
    print("  Process2 holds Resource2, wants Resource1")

    has_deadlock = detect_cycle_directed_dfs(resource_allocation)
    print(f"🔒 Deadlock detected: {has_deadlock}")

    # Example 3: Social Network Loops
    print(f"\nExample 3: Social Network Recommendation Loops")
    print("-" * 50)

    friendships = {
        "Alice": ["Bob"],
        "Bob": ["Charlie"],
        "Charlie": ["David"],
        "David": ["Alice"],  # This creates a cycle!
    }

    print("Friend recommendations chain:")
    for person, recommends in friendships.items():
        print(f"  {person} → {recommends}")

    cycle_path = find_cycle_path_directed(friendships)
    if cycle_path:
        print(f"🔄 Recommendation loop: {' → '.join(cycle_path)}")
    else:
        print("✅ No recommendation loops found")


def performance_comparison():
    """
    Compare performance of different cycle detection methods
    """
    print("\n⚡ PERFORMANCE COMPARISON")
    print("=" * 30)

    print(
        """
METHOD COMPARISON:
━━━━━━━━━━━━━━━━━━

1. 🔍 DFS with Colors (Directed)
   Time: O(V + E)
   Space: O(V)
   ✅ Most intuitive
   ✅ Finds actual cycle
   ✅ Works for directed graphs

2. 🔍 DFS with Parent (Undirected)  
   Time: O(V + E)
   Space: O(V)
   ✅ Simple to understand
   ✅ Perfect for undirected graphs
   ❌ Only works for undirected

3. 📊 Topological Sort (Directed)
   Time: O(V + E)  
   Space: O(V)
   ✅ Detects any cycle
   ✅ Can order nodes if no cycle
   ❌ Doesn't find actual cycle path
   ❌ Only works for directed graphs

4. 🔗 Union-Find (Undirected)
   Time: O(E α(V)) where α is inverse Ackermann
   Space: O(V)
   ✅ Very efficient for sparse graphs
   ❌ Complex to implement
   ❌ Only works for undirected graphs

WHEN TO USE EACH:
━━━━━━━━━━━━━━━━━

• Need cycle path? → DFS with colors
• Undirected graph? → DFS with parent  
• Also need topological order? → Topological sort
• Very large sparse graph? → Union-Find
"""
    )


def advanced_cycle_detection():
    """
    Advanced cycle detection techniques
    """
    print("\n🚀 ADVANCED CYCLE DETECTION")
    print("=" * 35)

    print(
        """
ADVANCED TECHNIQUES:
━━━━━━━━━━━━━━━━━━━━

1. 🔍 STRONGLY CONNECTED COMPONENTS
   - Find all cycles in directed graph
   - Use Tarjan's or Kosaraju's algorithm
   - Identifies cycle groups

2. 🎯 CYCLE LENGTH DETECTION
   - Find shortest cycle
   - Find longest cycle
   - Count total cycles

3. 🌐 NEGATIVE CYCLE DETECTION
   - Use Bellman-Ford algorithm
   - Important for shortest path algorithms
   - Detects negative weight cycles

4. 🔄 CYCLE BASIS
   - Find fundamental cycles
   - Minimum cycle basis
   - Used in network analysis

5. 🎨 CYCLE COLORING
   - 3-coloring for planar graphs
   - Detect odd/even cycles
   - Graph bipartiteness testing
"""
    )

    def find_shortest_cycle(graph):
        """Find the shortest cycle in the graph"""
        shortest_cycle = None
        min_length = float("inf")

        for start_node in graph:
            # Try to find cycle starting from each node
            visited = {start_node}
            queue = [(start_node, [start_node])]

            while queue:
                node, path = queue.pop(0)

                for neighbor in graph.get(node, []):
                    if neighbor == start_node and len(path) > 2:
                        # Found cycle back to start
                        cycle_length = len(path)
                        if cycle_length < min_length:
                            min_length = cycle_length
                            shortest_cycle = path + [start_node]
                    elif neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

        return shortest_cycle, min_length if shortest_cycle else None

    # Example usage
    cycle_graph = {0: [1], 1: [2], 2: [0, 3], 3: [4], 4: [3]}
    shortest, length = find_shortest_cycle(cycle_graph)
    if shortest:
        print(f"Example: Shortest cycle in {cycle_graph}")
        print(f"Shortest cycle: {' → '.join(map(str, shortest))} (length: {length})")


def cycle_detection_cheatsheet():
    """
    Quick reference for cycle detection
    """
    print("\n📋 CYCLE DETECTION CHEATSHEET")
    print("=" * 35)

    print(
        """
QUICK DECISION TREE:
━━━━━━━━━━━━━━━━━━━━

Graph Type?
├─ Undirected → Use DFS with parent tracking
└─ Directed → Choose below:

Need cycle path?
├─ Yes → Use DFS with 3-colors  
└─ No → Use topological sort

Graph Size?
├─ Small/Medium → Any method works
└─ Very Large → Consider Union-Find (undirected)

IMPLEMENTATION TEMPLATES:
━━━━━━━━━━━━━━━━━━━━━━━━━

# Undirected Graph:
def has_cycle_undirected(graph):
    visited = set()
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node): return True
            elif neighbor != parent:
                return True
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node, None): return True
    return False

# Directed Graph:  
def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    colors = {node: WHITE for node in graph}
    
    def dfs(node):
        colors[node] = GRAY
        for neighbor in graph[node]:
            if colors[neighbor] == GRAY: return True
            if colors[neighbor] == WHITE and dfs(neighbor): return True
        colors[node] = BLACK
        return False
    
    for node in graph:
        if colors[node] == WHITE:
            if dfs(node): return True
    return False
"""
    )


if __name__ == "__main__":
    # Test undirected graph cycle detection
    print("TESTING UNDIRECTED GRAPH")
    print("=" * 30)

    undirected_no_cycle = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    undirected_with_cycle = {0: [1, 2], 1: [0, 2], 2: [0, 1]}

    print("Graph without cycle:")
    result1 = detect_cycle_undirected_dfs(undirected_no_cycle)
    print(f"Has cycle: {result1}\n")

    print("Graph with cycle:")
    result2 = detect_cycle_undirected_dfs(undirected_with_cycle)
    print(f"Has cycle: {result2}")

    print("\n" + "=" * 60)

    # Test directed graph cycle detection
    print("TESTING DIRECTED GRAPH")
    print("=" * 25)

    directed_no_cycle = {0: [1, 2], 1: [3], 2: [3], 3: []}
    directed_with_cycle = {0: [1], 1: [2], 2: [3], 3: [1]}

    print("Directed graph without cycle:")
    result3 = detect_cycle_directed_dfs(directed_no_cycle)
    print(f"Has cycle: {result3}\n")

    print("Directed graph with cycle:")
    result4 = detect_cycle_directed_dfs(directed_with_cycle)
    print(f"Has cycle: {result4}")

    print("\n" + "=" * 60)

    # Find actual cycle path
    cycle_path = find_cycle_path_directed(directed_with_cycle)
    print(f"Actual cycle path: {cycle_path}")

    print("\n" + "=" * 60)

    # Topological sort method
    detect_cycle_using_topology(directed_with_cycle)

    print("\n" + "=" * 60)

    # Practical examples
    practical_cycle_examples()

    # Performance comparison
    performance_comparison()

    # Advanced techniques
    advanced_cycle_detection()

    # Cheatsheet
    cycle_detection_cheatsheet()

    print("\n✅ You now master cycle detection!")
    print("🎯 Next: Learn connected components algorithms")
    print("💡 Key takeaway: Choose method based on graph type and needs!")
