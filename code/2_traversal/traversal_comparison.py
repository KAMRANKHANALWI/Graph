"""
DFS vs BFS Traversal Comparison
===============================
Side-by-side comparison of DFS and BFS with visualizations and use cases.
"""

from collections import deque
import time


def side_by_side_comparison(graph, start):
    """
    Run DFS and BFS on the same graph and compare results
    """
    print("🆚 DFS vs BFS SIDE-BY-SIDE COMPARISON")
    print("=" * 50)
    print(f"Graph: {graph}")
    print(f"Starting node: {start}")

    # Visualize the graph structure first
    print("\nGraph Structure:")
    max_node = max(
        max(graph.keys()),
        max(max(neighbors) for neighbors in graph.values() if neighbors),
    )
    levels = create_level_structure(graph, start)

    for level, nodes in levels.items():
        print(f"  Level {level}: {sorted(nodes)}")

    print("\n" + "=" * 25 + " DFS " + "=" * 25)

    # DFS Implementation
    def dfs_detailed(graph, start):
        visited = set()
        stack = [start]
        order = []
        steps = []

        step = 1
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                steps.append(f"Step {step}: Visit {node} (stack: {stack})")

                # Add neighbors in reverse order
                neighbors = graph.get(node, [])
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)

                step += 1

        return order, steps

    dfs_order, dfs_steps = dfs_detailed(graph, start)

    print("DFS Process (Stack - LIFO):")
    for step in dfs_steps:
        print(f"  {step}")
    print(f"Final DFS order: {dfs_order}")

    print("\n" + "=" * 25 + " BFS " + "=" * 25)

    # BFS Implementation
    def bfs_detailed(graph, start):
        visited = set([start])
        queue = deque([start])
        order = []
        steps = []

        step = 1
        while queue:
            node = queue.popleft()
            order.append(node)
            steps.append(f"Step {step}: Visit {node} (queue: {list(queue)})")

            # Add unvisited neighbors
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

            step += 1

        return order, steps

    bfs_order, bfs_steps = bfs_detailed(graph, start)

    print("BFS Process (Queue - FIFO):")
    for step in bfs_steps:
        print(f"  {step}")
    print(f"Final BFS order: {bfs_order}")

    # Summary comparison
    print("\n" + "=" * 20 + " COMPARISON " + "=" * 20)
    print(f"DFS order: {dfs_order}")
    print(f"BFS order: {bfs_order}")
    print(f"Same nodes visited: {set(dfs_order) == set(bfs_order)}")
    print(f"Same order: {dfs_order == bfs_order}")

    return dfs_order, bfs_order


def create_level_structure(graph, start):
    """
    Create level structure for visualization
    """
    visited = set([start])
    current_level = [start]
    levels = {0: [start]}
    level = 0

    while current_level:
        next_level = []
        for node in current_level:
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_level.append(neighbor)

        if next_level:
            level += 1
            levels[level] = next_level
            current_level = next_level
        else:
            break

    return levels


def visualize_traversal_paths(graph, start):
    """
    Show the actual path each algorithm takes through the graph
    """
    print("🛤️  TRAVERSAL PATH VISUALIZATION")
    print("=" * 40)

    # DFS path
    visited_dfs = set()
    stack = [start]
    dfs_path = []

    while stack:
        node = stack.pop()
        if node not in visited_dfs:
            visited_dfs.add(node)
            dfs_path.append(node)

            neighbors = graph.get(node, [])
            for neighbor in reversed(neighbors):
                if neighbor not in visited_dfs:
                    stack.append(neighbor)

    # BFS path
    visited_bfs = set([start])
    queue = deque([start])
    bfs_path = []

    while queue:
        node = queue.popleft()
        bfs_path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited_bfs:
                visited_bfs.add(neighbor)
                queue.append(neighbor)

    print(f"DFS path: {' → '.join(map(str, dfs_path))}")
    print(f"BFS path: {' → '.join(map(str, bfs_path))}")

    # Show movement pattern
    print("\nMovement Pattern:")
    print("DFS: Goes DEEP first - like exploring a cave system")
    print("BFS: Goes WIDE first - like ripples in a pond")


def performance_comparison(graph, start):
    """
    Compare performance characteristics
    """
    print("\n⚡ PERFORMANCE COMPARISON")
    print("=" * 30)

    # Time both algorithms
    def time_algorithm(func, *args):
        start_time = time.time()
        result = func(*args)
        end_time = time.time()
        return result, (end_time - start_time) * 1000  # Convert to milliseconds

    def dfs_simple(graph, start):
        visited = set()
        stack = [start]
        result = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor in reversed(graph.get(node, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return result

    def bfs_simple(graph, start):
        visited = set([start])
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result

    dfs_result, dfs_time = time_algorithm(dfs_simple, graph, start)
    bfs_result, bfs_time = time_algorithm(bfs_simple, graph, start)

    print(f"DFS time: {dfs_time:.3f} ms")
    print(f"BFS time: {bfs_time:.3f} ms")

    # Memory usage estimation
    print("\nMemory Usage:")
    print("DFS: O(h) where h = height of graph (recursion depth)")
    print("BFS: O(w) where w = width of graph (max nodes in queue)")

    # Calculate actual memory for this graph
    levels = create_level_structure(graph, start)
    max_width = max(len(nodes) for nodes in levels.values())
    max_depth = len(levels)

    print(f"For this graph:")
    print(f"  Max depth (DFS memory): {max_depth}")
    print(f"  Max width (BFS memory): {max_width}")


def when_to_use_which():
    """
    Comprehensive guide on when to use DFS vs BFS
    """
    print("\n🎯 WHEN TO USE DFS vs BFS")
    print("=" * 35)

    print(
        """
🔍 USE DFS WHEN:
━━━━━━━━━━━━━━━

✅ Finding ANY path (not necessarily shortest)
✅ Detecting cycles in graphs
✅ Topological sorting
✅ Solving puzzles with backtracking
✅ Tree/graph traversal where order doesn't matter
✅ Memory is limited (uses less memory)
✅ Graph is very wide but not deep

Examples:
• Maze solving (any solution)
• Sudoku solver
• Finding connected components
• Dependency resolution

🌊 USE BFS WHEN:
━━━━━━━━━━━━━━━

✅ Finding SHORTEST path (unweighted graphs)
✅ Level-order traversal needed
✅ Finding nodes at specific distance
✅ Spreading/propagation problems
✅ Finding closest neighbor
✅ Social network analysis

Examples:
• GPS shortest route
• Social network degrees of separation
• Web crawling (breadth first)
• Finding nearest gas station
• Game AI pathfinding

⚖️  COMPLEXITY COMPARISON:
━━━━━━━━━━━━━━━━━━━━━━━━━

                 DFS        BFS
Time:           O(V + E)   O(V + E)
Space:          O(h)       O(w)
                ↑          ↑
            height      width

Both visit every vertex and edge once!
Difference is in SPACE usage pattern.
"""
    )


def practical_examples():
    """
    Show practical examples of when to use each
    """
    print("\n💼 PRACTICAL EXAMPLES")
    print("=" * 25)

    # Example 1: Social Network
    print("Example 1: Social Network Analysis")
    print("-" * 35)

    social_graph = {
        "You": ["Alice", "Bob"],
        "Alice": ["You", "Carol", "Dave"],
        "Bob": ["You", "Eve"],
        "Carol": ["Alice", "Frank"],
        "Dave": ["Alice"],
        "Eve": ["Bob", "Frank"],
        "Frank": ["Carol", "Eve"],
    }

    print("Task: Find shortest connection to Frank")

    def bfs_shortest_path(graph, start, target):
        if start == target:
            return [start]

        visited = set([start])
        queue = deque([(start, [start])])

        while queue:
            node, path = queue.popleft()
            for neighbor in graph.get(node, []):
                if neighbor == target:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    path_to_frank = bfs_shortest_path(social_graph, "You", "Frank")
    print(f"Shortest path to Frank: {' → '.join(path_to_frank)}")
    print("✅ BFS wins - guarantees shortest path!\n")

    # Example 2: File System
    print("Example 2: File System Search")
    print("-" * 30)

    file_system = {
        "/": ["home", "usr", "var"],
        "home": ["user1", "user2"],
        "usr": ["bin", "lib"],
        "var": ["log", "tmp"],
        "user1": ["documents", "downloads"],
        "user2": ["projects"],
        "bin": [],
        "lib": [],
        "log": [],
        "tmp": [],
        "documents": [],
        "downloads": [],
        "projects": [],
    }

    print("Task: Find any file in deep directory structure")

    def dfs_find_any(graph, start, target):
        visited = set()
        stack = [start]

        while stack:
            node = stack.pop()
            if node == target:
                return True
            if node not in visited:
                visited.add(node)
                for neighbor in graph.get(node, []):
                    stack.append(neighbor)
        return False

    found = dfs_find_any(file_system, "/", "projects")
    print(f"Found 'projects' directory: {found}")
    print("✅ DFS wins - uses less memory for deep searches!")


def algorithm_decision_tree():
    """
    Decision tree to help choose between DFS and BFS
    """
    print("\n🌳 ALGORITHM DECISION TREE")
    print("=" * 30)

    print(
        """
Start Here: What do you need?
│
├─ Need SHORTEST path?
│  ├─ YES → Use BFS ✅
│  └─ NO → Continue below
│
├─ Need to visit ALL nodes?
│  ├─ Memory limited? 
│  │  ├─ YES → Use DFS ✅
│  │  └─ NO → Either works, prefer BFS for consistent ordering
│  └─ NO → Continue below
│
├─ Looking for ANY solution?
│  ├─ Deep graph? → Use DFS ✅
│  └─ Wide graph? → Use BFS ✅
│
├─ Need level-by-level processing?
│  └─ YES → Use BFS ✅
│
├─ Implementing backtracking?
│  └─ YES → Use DFS ✅
│
└─ When in doubt → Use BFS (more predictable memory usage)

🎯 Quick Rules of Thumb:
• Shortest path → BFS
• Any path → DFS  
• Level order → BFS
• Deep search → DFS
• Memory matters → DFS
• Consistent results → BFS
"""
    )


if __name__ == "__main__":
    # Test with the standard example graph
    graph = {0: [1, 3], 1: [2], 2: [], 3: [4], 4: []}

    # Side-by-side comparison
    side_by_side_comparison(graph, 0)

    # Visual path comparison
    visualize_traversal_paths(graph, 0)

    # Performance analysis
    performance_comparison(graph, 0)

    # When to use which
    when_to_use_which()

    # Practical examples
    practical_examples()

    # Decision tree
    algorithm_decision_tree()

    print("\n✅ You now know exactly when to use DFS vs BFS!")
    print("🎯 Next: Learn advanced graph algorithms")
    print("💡 Key takeaway: Choose based on your specific needs!")
