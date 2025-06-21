"""
DFS Recursive Implementation
============================
Complete guide to Depth-First Search using recursion with visualization.
"""


class DFSRecursiveVisualizer:
    """Visualize how DFS recursion works with call stack"""

    def __init__(self):
        self.step = 0
        self.max_depth = 0

    def dfs_with_full_visualization(
        self, graph, node, visited=None, depth=0, path=None
    ):
        """
        DFS with complete step-by-step visualization
        Shows recursion stack, backtracking, and path building
        """
        # Initialize on first call
        if visited is None:
            visited = set()
            path = []
            print("🚀 Starting DFS Recursive Traversal")
            print("=" * 50)
            print(f"Graph: {graph}")
            print()

        # Track maximum recursion depth
        self.max_depth = max(self.max_depth, depth)

        # Show entering function
        self.step += 1
        indent = "  " * depth
        print(f"Step {self.step}: {indent}📥 ENTER dfs({node}) - Depth {depth}")
        print(f"{indent}   🎯 Current path: {path}")
        print(f"{indent}   ✅ Visited so far: {sorted(visited)}")
        print(f"{indent}   📚 Call stack depth: {depth}")

        # Add current node to visited and path
        visited.add(node)
        path.append(node)
        print(f"{indent}   ➕ Added {node} to visited and path")
        print(f"{indent}   🌟 Now visiting: {node}")

        # Get neighbors
        neighbors = graph.get(node, [])
        unvisited_neighbors = [n for n in neighbors if n not in visited]

        print(f"{indent}   🔍 All neighbors of {node}: {neighbors}")
        print(f"{indent}   🆕 Unvisited neighbors: {unvisited_neighbors}")

        if not unvisited_neighbors:
            print(f"{indent}   🔚 No unvisited neighbors - this is a DEAD END!")

        # Recursively visit unvisited neighbors
        for neighbor in unvisited_neighbors:
            print(f"{indent}   ⬇️  Going DEEPER to explore {neighbor}")
            self.dfs_with_full_visualization(graph, neighbor, visited, depth + 1, path)
            print(f"{indent}   ⬆️  RETURNED from exploring {neighbor}")

        # Show exiting function (backtracking)
        print(f"{indent}📤 EXIT dfs({node}) - Backtracking")
        if depth > 0:
            print(f"{indent}   🔄 Backtracking to previous level")
        print()

        return visited, path


def simple_dfs_recursive(graph, node, visited=None):
    """
    Clean, simple DFS recursive implementation
    This is what you'll actually use in practice
    """
    if visited is None:
        visited = set()

    # Visit current node
    visited.add(node)
    print(f"Visiting: {node}")

    # Recursively visit all unvisited neighbors
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            simple_dfs_recursive(graph, neighbor, visited)

    return visited


def dfs_with_path(graph, node, visited=None, path=None):
    """
    DFS that also tracks the path taken
    Useful for pathfinding algorithms
    """
    if visited is None:
        visited = set()
        path = []

    visited.add(node)
    path.append(node)

    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            dfs_with_path(graph, neighbor, visited, path)

    return visited, path


def dfs_find_path(graph, start, target, path=None):
    """
    Use DFS to find a path between two nodes
    Returns the first path found (not necessarily shortest)
    """
    if path is None:
        path = []

    path = path + [start]

    # Found target!
    if start == target:
        return path

    # Explore neighbors
    for neighbor in graph.get(start, []):
        if neighbor not in path:  # Avoid cycles
            new_path = dfs_find_path(graph, neighbor, target, path)
            if new_path:
                return new_path

    return None  # No path found


def dfs_find_all_paths(graph, start, target, path=None):
    """
    Find ALL paths between two nodes using DFS
    """
    if path is None:
        path = []

    path = path + [start]

    if start == target:
        return [path]

    paths = []
    for neighbor in graph.get(start, []):
        if neighbor not in path:  # Avoid cycles
            new_paths = dfs_find_all_paths(graph, neighbor, target, path)
            paths.extend(new_paths)

    return paths


def understand_recursion_stack():
    """
    Explain how the recursion stack works in DFS
    """
    print("🧠 UNDERSTANDING THE RECURSION STACK")
    print("=" * 45)

    print(
        """
How DFS Recursion Works:

1. 📞 FUNCTION CALL: When we call dfs(node), Python puts it on the call stack
2. 🔄 RECURSION: Each neighbor call creates a NEW function call on the stack  
3. 📚 STACK GROWS: Stack gets deeper as we go deeper into the graph
4. 🔚 BASE CASE: When no more unvisited neighbors, function returns
5. ⬆️  BACKTRACK: Python automatically goes back to previous function call
6. 🔄 REPEAT: Continue until all functions have returned

Visual Example:
                                                    
Step 1: dfs(0) called           Step 2: dfs(1) called from dfs(0)
┌─────────────────┐            ┌─────────────────┐
│ dfs(0)          │            │ dfs(1)          │ ← Current
│ node = 0        │            │ node = 1        │
│ neighbors=[1,3] │            ├─────────────────┤
└─────────────────┘            │ dfs(0)          │ ← Waiting
                               │ node = 0        │
                               │ neighbors=[1,3] │
                               └─────────────────┘

Step 3: dfs(2) called           Step 4: dfs(2) returns
┌─────────────────┐            ┌─────────────────┐
│ dfs(2)          │            │ dfs(1)          │ ← Resumes
│ node = 2        │            │ node = 1        │
│ neighbors=[]    │ ← No more  ├─────────────────┤
├─────────────────┤            │ dfs(0)          │ ← Still waiting
│ dfs(1)          │ ← Waiting  │ node = 0        │
│ node = 1        │            │ neighbors=[1,3] │
├─────────────────┤            └─────────────────┘
│ dfs(0)          │ ← Waiting
│ node = 0        │
│ neighbors=[1,3] │
└─────────────────┘

This is how Python automatically handles the "backtracking" for us!
"""
    )


def demonstrate_dfs_recursive():
    """
    Demonstrate DFS recursive with different examples
    """
    print("🌟 DFS RECURSIVE DEMONSTRATIONS")
    print("=" * 40)

    # Example 1: Simple linear graph
    print("--- Example 1: Linear Graph ---")
    linear_graph = {0: [1], 1: [2], 2: [3], 3: []}
    print(f"Graph: {linear_graph}")
    print("Visual: 0 → 1 → 2 → 3")
    print("\nDFS Traversal:")
    simple_dfs_recursive(linear_graph, 0)

    print("\n" + "-" * 30)

    # Example 2: Tree-like graph
    print("--- Example 2: Tree Graph ---")
    tree_graph = {0: [1, 3], 1: [2], 2: [], 3: [4], 4: []}
    print(f"Graph: {tree_graph}")
    print(
        """Visual:    0
         / \\
        1   3
        |   |
        2   4"""
    )
    print("\nDFS Traversal:")
    simple_dfs_recursive(tree_graph, 0)

    print("\n" + "-" * 30)

    # Example 3: Graph with cycle (but we avoid it)
    print("--- Example 3: Graph with Cycles ---")
    cycle_graph = {0: [1, 2], 1: [3], 2: [3], 3: [0]}  # 3 points back to 0!
    print(f"Graph: {cycle_graph}")
    print("Visual: 0 ⟷ 1")
    print("        ↕   ↓")
    print("        2 → 3")
    print("\nDFS Traversal (cycles avoided by visited set):")
    simple_dfs_recursive(cycle_graph, 0)


def demonstrate_pathfinding():
    """
    Show how DFS can be used for pathfinding
    """
    print("\n🎯 DFS FOR PATHFINDING")
    print("=" * 30)

    # Create a more complex graph
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": ["F"],
        "F": ["G"],
        "G": [],
    }

    print(f"Graph: {graph}")
    print(
        """
Visual Network:
    A
   / \\
  B   C
 / |   \\
D  E    F
   |   / \\
   └→ G ←┘
"""
    )

    # Find single path
    path = dfs_find_path(graph, "A", "G")
    print(f"First path from A to G: {' → '.join(path) if path else 'No path'}")

    # Find all paths
    all_paths = dfs_find_all_paths(graph, "A", "G")
    print(f"All paths from A to G:")
    for i, path in enumerate(all_paths, 1):
        print(f"  Path {i}: {' → '.join(path)}")


def dfs_applications():
    """
    Show practical applications of DFS
    """
    print("\n🔧 PRACTICAL APPLICATIONS OF DFS")
    print("=" * 40)

    print(
        """
DFS is perfect for:

1. 🔍 PATHFINDING
   - Find any path between two nodes
   - Maze solving
   - Game AI movement

2. 🔄 CYCLE DETECTION  
   - Detect if graph has cycles
   - Dependency resolution
   - Deadlock detection

3. 🌳 TREE TRAVERSAL
   - File system traversal
   - Parse trees
   - Decision trees

4. 🏝️ CONNECTED COMPONENTS
   - Find isolated groups
   - Social network clusters
   - Image segmentation

5. 🎯 TOPOLOGICAL SORTING
   - Task scheduling
   - Course prerequisites
   - Build dependencies

Why DFS? 
✅ Simple to implement
✅ Uses less memory than BFS
✅ Natural for recursive problems
✅ Goes "deep" quickly - good for finding distant solutions
"""
    )


if __name__ == "__main__":
    # First understand the concept
    understand_recursion_stack()

    # Then see it in action with full visualization
    print("\n" + "=" * 60)
    print("🔍 DETAILED DFS VISUALIZATION")
    print("=" * 60)

    graph = {0: [1, 3], 1: [2], 2: [], 3: [4], 4: []}
    visualizer = DFSRecursiveVisualizer()
    visited, path = visualizer.dfs_with_full_visualization(graph, 0)

    print(f"🏁 FINAL RESULTS:")
    print(f"   Visited nodes: {sorted(visited)}")
    print(f"   Final path: {path}")
    print(f"   Maximum recursion depth: {visualizer.max_depth}")

    # Simple demonstrations
    demonstrate_dfs_recursive()

    # Pathfinding examples
    demonstrate_pathfinding()

    # Applications
    dfs_applications()

    print("\n✅ You now understand DFS Recursive completely!")
    print("🎯 Next: Learn DFS Iterative (using explicit stack)")
    print("💡 Both approaches do the same thing, just differently!")
