"""
BFS (Breadth-First Search) Implementation
=========================================
Complete guide to BFS using queue with level-by-level exploration.
"""

from collections import deque


def bfs_with_visualization(graph, start):
    """
    BFS with complete step-by-step visualization
    Shows how queue works and why we use FIFO
    """
    print("🌊 BFS WITH QUEUE VISUALIZATION")
    print("=" * 40)
    print(f"Graph: {graph}")
    print(f"Starting from node: {start}")
    print("\nWhy Queue? Queue = First In, First Out (FIFO)")
    print("This ensures we visit nodes level by level!\n")

    visited = set()
    queue = deque([start])  # Initialize queue with start node
    visited.add(start)  # Mark start as visited immediately
    step = 1
    level = 0

    print(f"Initial state:")
    print(f"  Queue: {list(queue)}")
    print(f"  Visited: {sorted(visited)}")
    print(f"  Level {level}: [{start}]")
    print()

    current_level_nodes = [start]
    next_level_nodes = []

    while queue:
        print(f"--- Step {step} ---")
        print(f"Queue before dequeue: {list(queue)}")

        # Dequeue from front (FIFO - First In, First Out)
        node = queue.popleft()  # Remove from LEFT side (first added)
        print(f"⬅️  Dequeued: {node}")
        print(f"Queue after dequeue: {list(queue)}")

        print(f"🌟 Processing: {node}")

        # Get neighbors
        neighbors = graph.get(node, [])
        unvisited_neighbors = [n for n in neighbors if n not in visited]

        print(f"All neighbors of {node}: {neighbors}")
        print(f"Unvisited neighbors: {unvisited_neighbors}")

        if unvisited_neighbors:
            print(f"Adding to queue: {unvisited_neighbors}")
            for neighbor in unvisited_neighbors:
                visited.add(neighbor)  # Mark as visited when we add to queue
                queue.append(neighbor)  # Add to RIGHT side
                next_level_nodes.append(neighbor)
                print(f"  ➕ Added {neighbor} to queue and visited")
        else:
            print("🔚 No unvisited neighbors to add")

        print(f"Queue after adding: {list(queue)}")
        print(f"Visited set: {sorted(visited)}")

        # Check if we completed a level
        current_level_nodes.remove(node)
        if not current_level_nodes and next_level_nodes:
            level += 1
            current_level_nodes = next_level_nodes.copy()
            next_level_nodes = []
            print(
                f"🎊 Completed Level {level-1}, starting Level {level}: {current_level_nodes}"
            )

        print()
        step += 1

    print("🏁 Queue is empty - BFS complete!")
    print(f"Final visited nodes: {sorted(visited)}")
    return visited


def simple_bfs(graph, start):
    """
    Clean, simple BFS implementation
    This is what you'll use in practice
    """
    from collections import deque

    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []

    while queue:
        node = queue.popleft()  # FIFO
        result.append(node)
        print(f"Visiting: {node}")

        # Add unvisited neighbors to queue
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


def bfs_level_by_level(graph, start):
    """
    BFS that shows clear level-by-level traversal
    Perfect for understanding the "ripple effect"
    """
    from collections import deque

    print("🌊 BFS LEVEL-BY-LEVEL EXPLORATION")
    print("=" * 40)

    visited = set()
    queue = deque([start])
    visited.add(start)
    level = 0

    while queue:
        level_size = len(queue)  # Number of nodes at current level
        current_level = []

        print(f"Level {level}:", end=" ")

        # Process all nodes at current level
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)
            print(f"{node}", end=" ")

            # Add neighbors for next level
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        print(f" (explored: {current_level})")
        level += 1

    return visited


def bfs_shortest_path(graph, start, target):
    """
    Use BFS to find shortest path (minimum number of edges)
    BFS guarantees shortest path in unweighted graphs!
    """
    from collections import deque

    if start == target:
        return [start]

    visited = set()
    queue = deque([(start, [start])])  # Store (node, path_to_node)
    visited.add(start)

    while queue:
        node, path = queue.popleft()

        # Check all neighbors
        for neighbor in graph.get(node, []):
            if neighbor == target:
                return path + [neighbor]  # Found shortest path!

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found


def bfs_all_shortest_paths(graph, start):
    """
    Find shortest path distances to ALL nodes from start
    """
    from collections import deque

    distances = {start: 0}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        current_distance = distances[node]

        for neighbor in graph.get(node, []):
            if neighbor not in distances:
                distances[neighbor] = current_distance + 1
                queue.append(neighbor)

    return distances


def compare_dfs_vs_bfs():
    """
    Visual comparison of DFS vs BFS traversal order
    """
    print("🤔 DFS vs BFS COMPARISON")
    print("=" * 30)

    graph = {0: [1, 2], 1: [3, 4], 2: [5, 6], 3: [], 4: [], 5: [], 6: []}

    print(f"Graph: {graph}")
    print(
        """
Visual Tree:
      0
     / \\
    1   2
   / | | \\
  3  4 5  6
"""
    )

    print("\n--- DFS Traversal (Go Deep First) ---")
    print("Uses Stack (LIFO): Goes down one branch completely")

    # Simulate DFS
    visited_dfs = set()
    stack = [0]
    dfs_order = []

    while stack:
        node = stack.pop()
        if node not in visited_dfs:
            visited_dfs.add(node)
            dfs_order.append(node)

            # Add neighbors in reverse order for correct traversal
            neighbors = graph.get(node, [])
            for neighbor in reversed(neighbors):
                if neighbor not in visited_dfs:
                    stack.append(neighbor)

    print(f"DFS order: {dfs_order}")
    print("Path: 0 → 1 → 3 → 4 → 2 → 5 → 6 (deep first!)")

    print("\n--- BFS Traversal (Go Wide First) ---")
    print("Uses Queue (FIFO): Explores level by level")

    # Simulate BFS
    from collections import deque

    visited_bfs = set()
    queue = deque([0])
    visited_bfs.add(0)
    bfs_order = []

    while queue:
        node = queue.popleft()
        bfs_order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited_bfs:
                visited_bfs.add(neighbor)
                queue.append(neighbor)

    print(f"BFS order: {bfs_order}")
    print("Path: 0 → 1 → 2 → 3 → 4 → 5 → 6 (level by level!)")

    print("\n📊 Level-by-Level Breakdown:")
    print("Level 0: [0]")
    print("Level 1: [1, 2]")
    print("Level 2: [3, 4, 5, 6]")


def why_queue_for_bfs():
    """
    Explain why queue is essential for BFS
    """
    print("🤔 WHY QUEUE FOR BFS?")
    print("=" * 25)

    print(
        """
The Queue Property: FIFO (First In, First Out)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Think of a queue like a line at a store:
- First person in line gets served first
- New people join at the back
- People leave from the front

In BFS Context:
──────────────

1. 🌱 START: Add starting node to queue
2. 🔄 PROCESS: Remove node from FRONT (first added)
3. ➕ EXPAND: Add its neighbors to BACK
4. 🔁 REPEAT: Keep processing from front

This ensures we process nodes in the order they were discovered!

Example with Queue Operations:
────────────────────────────

Graph: 0→[1,2], 1→[3], 2→[4]

Step 1: queue = [0]                    ← Start with 0
Step 2: Remove 0, add its neighbors    ← queue = [1, 2]  
Step 3: Remove 1, add its neighbors    ← queue = [2, 3]
Step 4: Remove 2, add its neighbors    ← queue = [3, 4]
Step 5: Remove 3, add its neighbors    ← queue = [4]
Step 6: Remove 4, add its neighbors    ← queue = []

Result: 0, 1, 2, 3, 4 (level by level!)

If we used STACK instead:
────────────────────────

Step 1: stack = [0]                    ← Start with 0  
Step 2: Remove 0, add its neighbors    ← stack = [1, 2]
Step 3: Remove 2, add its neighbors    ← stack = [1, 4] 
Step 4: Remove 4, add its neighbors    ← stack = [1]
Step 5: Remove 1, add its neighbors    ← stack = [3]
Step 6: Remove 3, add its neighbors    ← stack = []

Result: 0, 2, 4, 1, 3 (NOT level by level - this is DFS!)

🎯 Queue = Level-by-level = BFS
🎯 Stack = Depth-first = DFS
"""
    )


def bfs_applications():
    """
    Show practical applications of BFS
    """
    print("🔧 PRACTICAL APPLICATIONS OF BFS")
    print("=" * 40)

    print(
        """
BFS is perfect for:

1. 🎯 SHORTEST PATH (Unweighted Graphs)
   - GPS navigation (equal road weights)
   - Social network connections
   - Puzzle solving (minimum moves)
   
2. 🌐 LEVEL-ORDER TRAVERSAL
   - File system by depth
   - Organization hierarchies  
   - Game level progression

3. 🔍 NEAREST NEIGHBOR PROBLEMS
   - Find closest store/service
   - Epidemic spread modeling
   - Network broadcast protocols

4. 🧩 PUZZLE SOLVING
   - Rubik's cube (minimum moves)
   - Word ladder problems
   - Maze solving (shortest path)

5. 🌳 TREE OPERATIONS
   - Level-order tree printing
   - Binary tree width
   - Find nodes at distance K

Why BFS over DFS?
✅ Guarantees shortest path
✅ Explores systematically
✅ Good for "closest" problems
✅ Memory usage predictable
"""
    )


def demonstrate_shortest_path():
    """
    Demonstrate BFS shortest path finding
    """
    print("🎯 BFS SHORTEST PATH DEMONSTRATION")
    print("=" * 40)

    # Create a network where shortest path matters
    network = {
        "Home": ["Park", "Store"],
        "Park": ["Home", "Cafe", "Library"],
        "Store": ["Home", "Mall"],
        "Cafe": ["Park", "School"],
        "Library": ["Park", "School"],
        "Mall": ["Store", "School"],
        "School": ["Cafe", "Library", "Mall"],
    }

    print("City Network:")
    for place, connections in network.items():
        print(f"  {place} ↔ {connections}")

    print(
        """
Visual Network:
    Home
   /    \\
Park -- Store
 | |     |
Cafe Library Mall
  \\  |   /
   School
"""
    )

    # Find shortest paths
    start = "Home"
    targets = ["School", "Mall", "Cafe"]

    print(f"\nShortest paths from {start}:")
    for target in targets:
        path = bfs_shortest_path(network, start, target)
        if path:
            distance = len(path) - 1
            print(f"  To {target}: {' → '.join(path)} (distance: {distance})")
        else:
            print(f"  To {target}: No path found")

    # Show all distances
    print(f"\nAll distances from {start}:")
    distances = bfs_all_shortest_paths(network, start)
    for place, distance in sorted(distances.items()):
        print(f"  {place}: {distance} steps")


def social_network_example():
    """
    Real-world example: Social network friend suggestions
    """
    print("\n🤝 SOCIAL NETWORK EXAMPLE")
    print("=" * 30)

    # Your friendship network
    friends = {
        "Kamran": ["Asad", "Shabab", "Saad"],
        "Asad": ["Kamran", "Shadman"],
        "Shabab": ["Kamran", "Zeeshan"],
        "Saad": ["Kamran", "Zeeshan"],
        "Shadman": ["Asad", "Ali"],
        "Zeeshan": ["Shabab", "Saad", "Ahmed"],
        "Ali": ["Shadman"],
        "Ahmed": ["Zeeshan"],
    }

    print("Friendship Network:")
    for person, friend_list in friends.items():
        print(f"  {person}: {friend_list}")

    def find_mutual_friends_distance(network, person1, person2):
        """Find how many steps apart two people are"""
        path = bfs_shortest_path(network, person1, person2)
        if path:
            return len(path) - 1, path
        return None, None

    def suggest_friends(network, person, max_distance=2):
        """Suggest friends within max_distance steps"""
        distances = bfs_all_shortest_paths(network, person)
        suggestions = []

        for other_person, distance in distances.items():
            if other_person != person and distance <= max_distance and distance > 1:
                suggestions.append((other_person, distance))

        return suggestions

    # Analyze connections
    person = "Kamran"
    print(f"\nAnalyzing connections for {person}:")

    # Direct friends
    print(f"Direct friends: {friends[person]}")

    # Friend suggestions
    suggestions = suggest_friends(friends, person, 2)
    print(f"Friend suggestions (2 steps away):")
    for suggested_person, distance in suggestions:
        path = bfs_shortest_path(friends, person, suggested_person)
        print(f"  {suggested_person} (via {' → '.join(path)})")

    # Connection distances
    print(f"\nConnection distances from {person}:")
    distances = bfs_all_shortest_paths(friends, person)
    for other_person, distance in sorted(distances.items()):
        if other_person != person:
            print(
                f"  {other_person}: {distance} {'step' if distance == 1 else 'steps'}"
            )


if __name__ == "__main__":
    # Start with why we use queue
    why_queue_for_bfs()

    # Show detailed visualization
    graph = {0: [1, 3], 1: [2], 2: [], 3: [4], 4: []}
    bfs_with_visualization(graph, 0)

    print("\n" + "=" * 60)

    # Show level-by-level exploration
    bfs_level_by_level(graph, 0)

    print("\n" + "=" * 60)

    # Compare DFS vs BFS
    compare_dfs_vs_bfs()

    print("\n" + "=" * 60)

    # Shortest path demonstration
    demonstrate_shortest_path()

    # Social network example
    social_network_example()

    # Show applications
    bfs_applications()

    print("\n✅ You now master BFS completely!")
    print("🎯 Next: Compare DFS vs BFS side by side")
    print("💡 Key takeaway: Queue = FIFO = Level by Level!")
