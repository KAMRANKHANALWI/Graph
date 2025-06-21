"""
Graph Path Finding Algorithms
=============================
Complete guide to finding paths between nodes using different strategies.
"""

from collections import deque


def dfs_find_any_path(graph, start, target, path=None):
    """
    Find ANY path using DFS (not necessarily shortest)
    Uses recursion and backtracking
    """
    if path is None:
        path = []

    path = path + [start]

    # Found the target!
    if start == target:
        return path

    # Try each neighbor
    for neighbor in graph.get(start, []):
        if neighbor not in path:  # Avoid cycles
            new_path = dfs_find_any_path(graph, neighbor, target, path)
            if new_path:  # Found a path through this neighbor
                return new_path

    # No path found through any neighbor
    return None


def dfs_find_all_paths(graph, start, target, path=None, all_paths=None):
    """
    Find ALL possible paths using DFS
    """
    if path is None:
        path = []
        all_paths = []

    path = path + [start]

    if start == target:
        all_paths.append(path)
        return all_paths

    for neighbor in graph.get(start, []):
        if neighbor not in path:  # Avoid cycles
            dfs_find_all_paths(graph, neighbor, target, path, all_paths)

    return all_paths


def bfs_find_shortest_path(graph, start, target):
    """
    Find SHORTEST path using BFS (minimum number of edges)
    BFS guarantees shortest path in unweighted graphs
    """
    if start == target:
        return [start]

    visited = set([start])
    queue = deque([(start, [start])])  # (current_node, path_to_node)

    while queue:
        current_node, path = queue.popleft()

        # Check each neighbor
        for neighbor in graph.get(current_node, []):
            if neighbor == target:
                return path + [neighbor]  # Found shortest path!

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # No path exists


def find_path_with_visualization(graph, start, target, algorithm="BFS"):
    """
    Find path with step-by-step visualization
    """
    print(f"🎯 FINDING PATH: {start} → {target} using {algorithm}")
    print("=" * 50)
    print(f"Graph: {graph}")

    if algorithm == "BFS":
        print("\nBFS Strategy: Find SHORTEST path (level by level)")
        print("Uses Queue (FIFO) - explores closest nodes first")

        if start == target:
            print(f"✅ Start = Target. Path: [{start}]")
            return [start]

        visited = set([start])
        queue = deque([(start, [start])])
        step = 1

        print(f"\nInitial: queue = [{start}], visited = {{{start}}}")

        while queue:
            print(f"\n--- Step {step} ---")
            current_node, path = queue.popleft()
            print(
                f"Processing: {current_node} (path so far: {' → '.join(map(str, path))})"
            )

            neighbors = graph.get(current_node, [])
            print(f"Neighbors of {current_node}: {neighbors}")

            for neighbor in neighbors:
                if neighbor == target:
                    final_path = path + [neighbor]
                    print(
                        f"🎉 FOUND TARGET! Final path: {' → '.join(map(str, final_path))}"
                    )
                    return final_path

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
                    print(
                        f"  Added {neighbor} to queue (path: {' → '.join(map(str, path + [neighbor]))})"
                    )
                else:
                    print(f"  {neighbor} already visited, skipping")

            print(
                "Queue now:", [f"{node}({'->'.join(map(str, p))})" for node, p in queue]
            )
            print(f"Visited: {sorted(visited)}")
            step += 1

        print("❌ No path found!")
        return None

    elif algorithm == "DFS":
        print("\nDFS Strategy: Find ANY path (go deep first)")
        print("Uses recursion and backtracking")

        def dfs_with_steps(current, target, path, step_counter):
            step_counter[0] += 1
            print(f"\n--- Step {step_counter[0]} ---")
            print(f"Exploring: {current}")
            print(f"Current path: {' → '.join(map(str, path))}")

            if current == target:
                print(f"🎉 FOUND TARGET! Final path: {' → '.join(map(str, path))}")
                return path

            neighbors = graph.get(current, [])
            print(f"Neighbors of {current}: {neighbors}")

            for neighbor in neighbors:
                if neighbor not in path:  # Avoid cycles
                    print(f"  Trying neighbor: {neighbor}")
                    result = dfs_with_steps(
                        neighbor, target, path + [neighbor], step_counter
                    )
                    if result:
                        return result
                else:
                    print(f"  {neighbor} already in path, skipping (avoid cycle)")

            print(f"🔙 Backtracking from {current}")
            return None

        step_counter = [0]
        result = dfs_with_steps(start, target, [start], step_counter)
        if not result:
            print("❌ No path found!")
        return result


def compare_path_finding_algorithms():
    """
    Compare different pathfinding approaches
    """
    print("🔍 PATH FINDING ALGORITHMS COMPARISON")
    print("=" * 45)

    # Test graph with multiple paths
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["E", "F"],
        "D": ["G"],
        "E": ["G", "H"],
        "F": ["H"],
        "G": ["I"],
        "H": ["I"],
        "I": [],
    }

    print(f"Graph: {graph}")
    print(
        """
Visual Network:
    A
   / \\
  B   C
 /|   |\\
D E   E F
| |   | |
G G   H H
 \\ \\ / /
   I←→I
"""
    )

    start, target = "A", "I"
    print(f"Finding paths from {start} to {target}:")

    # 1. DFS - Any path
    print("\n1️⃣ DFS - Find ANY path:")
    dfs_path = dfs_find_any_path(graph, start, target)
    print(f"   Result: {' → '.join(dfs_path) if dfs_path else 'No path'}")
    print(f"   Length: {len(dfs_path) - 1 if dfs_path else 0} edges")

    # 2. BFS - Shortest path
    print("\n2️⃣ BFS - Find SHORTEST path:")
    bfs_path = bfs_find_shortest_path(graph, start, target)
    print(f"   Result: {' → '.join(bfs_path) if bfs_path else 'No path'}")
    print(f"   Length: {len(bfs_path) - 1 if bfs_path else 0} edges")

    # 3. DFS - All paths
    print("\n3️⃣ DFS - Find ALL paths:")
    all_paths = dfs_find_all_paths(graph, start, target)
    print(f"   Found {len(all_paths)} paths:")
    for i, path in enumerate(all_paths, 1):
        print(f"     Path {i}: {' → '.join(path)} (length: {len(path) - 1})")

    # Analysis
    print("\n📊 Analysis:")
    if all_paths:
        lengths = [len(path) - 1 for path in all_paths]
        print(f"   Shortest path length: {min(lengths)}")
        print(f"   Longest path length: {max(lengths)}")
        print(f"   Average path length: {sum(lengths) / len(lengths):.1f}")

        if bfs_path:
            bfs_length = len(bfs_path) - 1
            shortest_length = min(lengths)
            print(f"   BFS found optimal path: {bfs_length == shortest_length}")


def practical_pathfinding_scenarios():
    """
    Real-world pathfinding scenarios
    """
    print("\n🌍 PRACTICAL PATHFINDING SCENARIOS")
    print("=" * 40)

    # Scenario 1: City Navigation
    print("Scenario 1: City Navigation System")
    print("-" * 35)

    city_map = {
        "Home": ["Main_St", "Park_Ave"],
        "Main_St": ["Home", "Downtown", "Mall"],
        "Park_Ave": ["Home", "School", "Hospital"],
        "Downtown": ["Main_St", "Office", "Mall"],
        "Mall": ["Main_St", "Downtown", "Movies"],
        "School": ["Park_Ave", "Library"],
        "Hospital": ["Park_Ave", "Pharmacy"],
        "Office": ["Downtown"],
        "Movies": ["Mall"],
        "Library": ["School"],
        "Pharmacy": ["Hospital"],
    }

    print("Task: Navigate from Home to Library")

    # Find shortest route
    shortest = bfs_find_shortest_path(city_map, "Home", "Library")
    print(f"Shortest route: {' → '.join(shortest)} ({len(shortest) - 1} blocks)")

    # Find alternative routes
    all_routes = dfs_find_all_paths(city_map, "Home", "Library")
    print(f"All possible routes ({len(all_routes)} total):")
    for i, route in enumerate(sorted(all_routes, key=len), 1):
        print(f"  Route {i}: {' → '.join(route)} ({len(route) - 1} blocks)")

    print("✅ Use BFS for GPS navigation (shortest route)")
    print("✅ Use DFS to find alternative routes")

    # Scenario 2: Social Network
    print(f"\nScenario 2: Social Network Connections")
    print("-" * 40)

    social_network = {
        "Alice": ["Bob", "Carol"],
        "Bob": ["Alice", "David", "Eve"],
        "Carol": ["Alice", "Frank"],
        "David": ["Bob", "George"],
        "Eve": ["Bob", "Frank", "Helen"],
        "Frank": ["Carol", "Eve", "Ivan"],
        "George": ["David"],
        "Helen": ["Eve"],
        "Ivan": ["Frank"],
    }

    print("Task: Find connection between Alice and Ivan")

    connection_path = bfs_find_shortest_path(social_network, "Alice", "Ivan")
    degrees_of_separation = len(connection_path) - 1

    print(f"Connection path: {' → '.join(connection_path)}")
    print(f"Degrees of separation: {degrees_of_separation}")
    print("✅ Use BFS for shortest social connections")


def advanced_pathfinding_techniques():
    """
    Advanced pathfinding concepts
    """
    print("\n🚀 ADVANCED PATHFINDING TECHNIQUES")
    print("=" * 40)

    print(
        """
1. 🎯 PATH WITH CONSTRAINTS
   - Avoid certain nodes
   - Maximum path length
   - Must visit specific nodes
   
2. 🔄 CYCLE DETECTION IN PATHS  
   - Detect infinite loops
   - Find shortest cycle
   - Break cycles intelligently
   
3. 📊 WEIGHTED GRAPHS
   - Dijkstra's algorithm
   - A* search with heuristics
   - Shortest path by cost, not edges
   
4. 🌐 MULTIPLE TARGETS
   - Find nearest of several targets
   - Visit all targets (TSP variant)
   - Multi-destination routing
   
5. 🧠 HEURISTIC SEARCH
   - Greedy best-first search
   - A* with manhattan distance
   - Bidirectional search

Example: Path with constraints
"""
    )

    def find_path_avoiding_nodes(graph, start, target, avoid_nodes):
        """Find path while avoiding certain nodes"""
        if start in avoid_nodes or target in avoid_nodes:
            return None

        visited = set([start])
        queue = deque([(start, [start])])

        while queue:
            current, path = queue.popleft()

            for neighbor in graph.get(current, []):
                if neighbor == target:
                    return path + [neighbor]

                if neighbor not in visited and neighbor not in avoid_nodes:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    # Example usage
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": ["E"], "E": []}
    normal_path = bfs_find_shortest_path(graph, "A", "E")
    avoiding_path = find_path_avoiding_nodes(graph, "A", "E", ["B"])

    print(f"Normal path A→E: {' → '.join(normal_path) if normal_path else 'None'}")
    print(f"Avoiding node B: {' → '.join(avoiding_path) if avoiding_path else 'None'}")


def pathfinding_best_practices():
    """
    Best practices for pathfinding
    """
    print("\n💡 PATHFINDING BEST PRACTICES")
    print("=" * 35)

    print(
        """
🎯 ALGORITHM SELECTION:
━━━━━━━━━━━━━━━━━━━━━━━

• Need shortest path? → BFS
• Any path is fine? → DFS  
• Weighted edges? → Dijkstra
• Have good heuristic? → A*
• Very large graph? → Bidirectional search

⚡ PERFORMANCE OPTIMIZATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Early termination when target found
• Bidirectional search for long paths
• Memoization for repeated queries
• Use appropriate data structures

🛡️ ROBUSTNESS:
━━━━━━━━━━━━━━━

• Check for cycles to avoid infinite loops
• Handle disconnected components
• Validate input (start/target exist)
• Set maximum path length limits

📊 MEMORY MANAGEMENT:
━━━━━━━━━━━━━━━━━━━━━━━

• DFS: O(depth) - good for deep graphs
• BFS: O(width) - good for shallow graphs
• Consider iterative DFS for very deep graphs
• Clear visited sets when appropriate

🔧 PRACTICAL TIPS:
━━━━━━━━━━━━━━━━━━

• Use BFS for unweighted shortest paths
• Use DFS for existence checks
• Cache results for repeated queries
• Consider approximate algorithms for huge graphs
"""
    )


if __name__ == "__main__":
    # Basic pathfinding examples
    test_graph = {0: [1, 2], 1: [3, 4], 2: [5], 3: [6], 4: [6], 5: [6], 6: []}

    print("🎯 BASIC PATHFINDING EXAMPLES")
    print("=" * 40)
    print(f"Test Graph: {test_graph}")
    print(f"Finding paths from 0 to 6:")
    print()

    # Test all basic algorithms
    dfs_path = dfs_find_any_path(test_graph, 0, 6)
    bfs_path = bfs_find_shortest_path(test_graph, 0, 6)
    all_paths = dfs_find_all_paths(test_graph, 0, 6)

    print(f"DFS (any path): {dfs_path}")
    print(f"BFS (shortest): {bfs_path}")
    print(f"All paths found: {len(all_paths)}")
    for i, path in enumerate(all_paths, 1):
        print(f"  Path {i}: {path}")

    print("\n" + "=" * 50)

    # Run visualization demo
    print("STEP-BY-STEP BFS DEMO:")
    find_path_with_visualization(test_graph, 0, 6, "BFS")

    print("\n" + "=" * 50)

    # Run all demonstrations
    compare_path_finding_algorithms()
    practical_pathfinding_scenarios()
    advanced_pathfinding_techniques()
    pathfinding_best_practices()

    print("\n🎉 PATHFINDING GUIDE COMPLETE!")
    print("Ready to find paths in any graph!")
