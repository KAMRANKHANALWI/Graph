"""
DFS Iterative Implementation
============================
Complete guide to Depth-First Search using explicit stack (no recursion).
"""


def dfs_iterative_with_visualization(graph, start):
    """
    DFS using explicit stack with step-by-step visualization
    Shows exactly how the stack works and why we use LIFO
    """
    print("🚀 DFS ITERATIVE WITH STACK VISUALIZATION")
    print("=" * 50)
    print(f"Graph: {graph}")
    print(f"Starting from node: {start}")
    print("\nWhy Stack? Stack = Last In, First Out (LIFO)")
    print("This mimics the recursion call stack behavior!\n")

    visited = set()
    stack = [start]  # Initialize stack with start node
    step = 1

    print(f"Initial state:")
    print(f"  Stack: {stack}")
    print(f"  Visited: {sorted(visited)}")
    print()

    while stack:
        print(f"--- Step {step} ---")
        print(f"Stack before pop: {stack}")

        # Pop from stack (LIFO - Last In, First Out)
        node = stack.pop()  # Remove from RIGHT side (last added)
        print(f"⬅️  Popped: {node}")
        print(f"Stack after pop: {stack}")

        if node not in visited:
            # Visit the node
            visited.add(node)
            print(f"✅ Visiting: {node}")
            print(f"Updated visited: {sorted(visited)}")

            # Get neighbors
            neighbors = graph.get(node, [])
            unvisited_neighbors = [n for n in neighbors if n not in visited]

            print(f"All neighbors of {node}: {neighbors}")
            print(f"Unvisited neighbors: {unvisited_neighbors}")

            if unvisited_neighbors:
                # Add neighbors to stack in REVERSE order
                # Why reverse? So we visit them in the original order!
                reversed_neighbors = list(reversed(unvisited_neighbors))
                print(f"Adding to stack (reversed): {reversed_neighbors}")

                for neighbor in reversed_neighbors:
                    if neighbor not in visited:  # Double-check
                        stack.append(neighbor)
                        print(f"  ➕ Added {neighbor} to stack")
            else:
                print("🔚 No unvisited neighbors to add")

            print(f"Stack after adding: {stack}")
        else:
            print(f"⚠️  {node} already visited, skipping")

        print(f"Current visited set: {sorted(visited)}")
        print()
        step += 1

    print("🏁 Stack is empty - DFS complete!")
    print(f"Final visited nodes: {sorted(visited)}")
    return visited


def simple_dfs_iterative(graph, start):
    """
    Clean, simple DFS iterative implementation
    This is what you'll use in practice
    """
    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()  # LIFO

        if node not in visited:
            visited.add(node)
            result.append(node)
            print(f"Visiting: {node}")

            # Add neighbors in reverse order for correct traversal
            neighbors = graph.get(node, [])
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)

    return result


def dfs_iterative_with_path(graph, start):
    """
    DFS iterative that also tracks the path to each node
    Useful for pathfinding
    """
    visited = set()
    stack = [(start, [start])]  # Store (node, path_to_node)
    paths = {}

    while stack:
        node, path = stack.pop()

        if node not in visited:
            visited.add(node)
            paths[node] = path
            print(f"Visiting {node}, path: {' → '.join(map(str, path))}")

            # Add neighbors with extended paths
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return paths


def compare_stack_vs_recursion():
    """
    Compare stack-based DFS with recursive DFS
    """
    print("🤔 STACK vs RECURSION COMPARISON")
    print("=" * 40)

    print(
        """
RECURSIVE DFS:                    ITERATIVE DFS:
─────────────                     ──────────────

✅ Pros:                          ✅ Pros:
  • Shorter, cleaner code           • No recursion limit issues
  • Natural to understand           • Explicit control over stack
  • Automatic backtracking          • Can be modified easily
  • Matches mathematical def        • Memory usage visible
                                   • Can pause/resume easily

❌ Cons:                          ❌ Cons:
  • Recursion depth limit           • More code to write
  • Hidden memory usage             • Manual stack management
  • Stack overflow possible         • Less intuitive initially
  • Harder to modify mid-run        • Need to handle order carefully

WHEN TO USE EACH:
━━━━━━━━━━━━━━━━━

🎯 Use RECURSIVE when:
  • Writing quick prototypes
  • Graph is guaranteed small
  • Code clarity is priority
  • Teaching/learning concepts

🎯 Use ITERATIVE when:
  • Dealing with large graphs
  • Need to avoid stack overflow
  • Want explicit memory control
  • Need to modify algorithm mid-run
  • Production code

Both produce IDENTICAL results - just different implementation!
"""
    )


def demonstrate_order_matters():
    """
    Show why neighbor order matters in iterative DFS
    """
    print("⚠️  ORDER MATTERS IN ITERATIVE DFS")
    print("=" * 40)

    graph = {0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}

    print(f"Graph: {graph}")
    print(
        """
Visual:     0
           / \\
          1   2
          |   |
          3   4
"""
    )

    print("\n--- Without Reversing Neighbors ---")
    print("Adding neighbors in original order: [1, 2]")
    print("Stack operations:")

    visited = set()
    stack = [0]
    step = 1

    while stack and step <= 3:  # Just show first few steps
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(f"Step {step}: Visit {node}")
            neighbors = graph.get(node, [])
            if neighbors:
                print(
                    f"  Add neighbors {neighbors} → stack becomes {stack + neighbors}"
                )
                stack.extend(neighbors)
        step += 1

    print("\nResult: Visits 2 before 1 (because 2 was added last, popped first)")

    print("\n--- With Reversing Neighbors ---")
    print("Adding neighbors in REVERSE order: [2, 1]")
    print("Stack operations:")

    visited = set()
    stack = [0]
    step = 1

    while stack and step <= 3:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(f"Step {step}: Visit {node}")
            neighbors = graph.get(node, [])
            if neighbors:
                reversed_neighbors = list(reversed(neighbors))
                print(
                    f"  Add reversed neighbors {reversed_neighbors} → stack becomes {stack + reversed_neighbors}"
                )
                stack.extend(reversed_neighbors)
        step += 1

    print("\nResult: Visits 1 before 2 (natural left-to-right order)")


def stack_operations_tutorial():
    """
    Tutorial on how stack operations work
    """
    print("📚 STACK OPERATIONS TUTORIAL")
    print("=" * 35)

    print(
        """
Python List as Stack:
────────────────────

stack = []           # Empty stack
stack.append(item)   # Push item (add to RIGHT end)
item = stack.pop()   # Pop item (remove from RIGHT end)

Visual Example:
──────────────

Initial: stack = []

append(1): [1]        ← 1 added to right
append(2): [1, 2]     ← 2 added to right  
append(3): [1, 2, 3]  ← 3 added to right

pop(): returns 3, stack = [1, 2]  ← removed from right
pop(): returns 2, stack = [1]     ← removed from right  
pop(): returns 1, stack = []      ← removed from right

This is LIFO: Last In, First Out
The last item added (3) is the first item removed.

In DFS Context:
──────────────
- We add neighbors to stack
- We process the MOST RECENTLY added neighbor first
- This creates the "go deep" behavior of DFS
"""
    )


def advanced_dfs_techniques():
    """
    Show advanced techniques with iterative DFS
    """
    print("🚀 ADVANCED DFS TECHNIQUES")
    print("=" * 30)

    print("1. DFS with Early Termination")
    print("─" * 30)

    def dfs_find_target(graph, start, target):
        """Stop DFS early when target is found"""
        visited = set()
        stack = [start]

        while stack:
            node = stack.pop()
            if node == target:
                print(f"🎯 Found target {target}!")
                return True

            if node not in visited:
                visited.add(node)
                print(f"Searching... visited {node}")

                for neighbor in reversed(graph.get(node, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)

        print(f"❌ Target {target} not found")
        return False

    graph = {0: [1, 2], 1: [3, 4], 2: [5], 3: [], 4: [], 5: []}
    print(f"Searching for node 4 in graph: {graph}")
    dfs_find_target(graph, 0, 4)

    print("\n2. DFS with Cycle Detection")
    print("─" * 30)

    def dfs_detect_cycle(graph):
        """Detect if graph has cycles using DFS"""
        WHITE, GRAY, BLACK = 0, 1, 2  # Not visited, visiting, visited
        colors = {node: WHITE for node in graph}

        def has_cycle_from(node):
            if colors[node] == GRAY:  # Back edge found!
                return True
            if colors[node] == BLACK:  # Already processed
                return False

            colors[node] = GRAY  # Mark as being processed

            for neighbor in graph.get(node, []):
                if has_cycle_from(neighbor):
                    return True

            colors[node] = BLACK  # Mark as completely processed
            return False

        for node in graph:
            if colors[node] == WHITE:
                if has_cycle_from(node):
                    return True
        return False

    cycle_graph = {0: [1], 1: [2], 2: [0]}  # 0→1→2→0 (cycle!)
    no_cycle_graph = {0: [1], 1: [2], 2: []}

    print(f"Graph with cycle {cycle_graph}: {dfs_detect_cycle(cycle_graph)}")
    print(f"Graph without cycle {no_cycle_graph}: {dfs_detect_cycle(no_cycle_graph)}")


if __name__ == "__main__":
    # Start with stack basics
    stack_operations_tutorial()

    # Show detailed visualization
    graph = {0: [1, 3], 1: [2], 2: [], 3: [4], 4: []}
    dfs_iterative_with_visualization(graph, 0)

    print("\n" + "=" * 60)

    # Simple clean implementation
    print("🎯 SIMPLE DFS ITERATIVE")
    print("=" * 25)
    print("Clean implementation for daily use:")
    simple_dfs_iterative(graph, 0)

    print("\n" + "=" * 60)

    # Compare approaches
    compare_stack_vs_recursion()

    # Show why order matters
    demonstrate_order_matters()

    # Advanced techniques
    advanced_dfs_techniques()

    print("\n✅ You now master DFS Iterative!")
    print("🎯 Next: Learn BFS (Breadth-First Search)")
    print("💡 Key takeaway: Stack = LIFO = Go Deep!")
