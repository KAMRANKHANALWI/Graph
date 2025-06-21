"""
Dijkstra's Shortest Path Algorithm
==================================
Advanced graph algorithm for finding shortest paths in weighted graphs!
"""

import heapq
from collections import defaultdict


def dijkstra_algorithm(graph, start):
    """
    Dijkstra's algorithm implementation with detailed steps
    Returns shortest distances and paths to all nodes from start
    """
    print(f"🎯 DIJKSTRA'S ALGORITHM: Finding shortest paths from {start}")
    print("=" * 55)

    # Initialize distances and previous nodes
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous = {}

    # Priority queue: (distance, node)
    priority_queue = [(0, start)]
    visited = set()

    print(f"Initial state:")
    print(f"  Distances: {dict(distances)}")
    print(f"  Priority queue: {priority_queue}")
    print()

    step = 1

    while priority_queue:
        # Get node with minimum distance
        current_distance, current_node = heapq.heappop(priority_queue)

        print(f"--- Step {step} ---")
        print(f"Processing node: {current_node} (distance: {current_distance})")

        # Skip if already visited (can happen with duplicate entries)
        if current_node in visited:
            print(f"  {current_node} already visited, skipping")
            continue

        # Mark as visited
        visited.add(current_node)
        print(f"  Marked {current_node} as visited")

        # Check all neighbors
        neighbors = graph.get(current_node, [])
        print(f"  Neighbors: {[(neighbor, weight) for neighbor, weight in neighbors]}")

        for neighbor, weight in neighbors:
            if neighbor not in visited:
                # Calculate new distance
                new_distance = current_distance + weight

                print(
                    f"    Checking {neighbor}: current={distances[neighbor]}, new={new_distance}"
                )

                # If we found a shorter path
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))
                    print(f"    ✅ Updated distance to {neighbor}: {new_distance}")
                else:
                    print(f"    ❌ No improvement for {neighbor}")

        print(f"  Current distances: {dict(distances)}")
        print(f"  Priority queue: {sorted(priority_queue)}")
        print()
        step += 1

    return distances, previous


def reconstruct_path(previous, start, target):
    """
    Reconstruct the shortest path from start to target
    """
    if target not in previous and target != start:
        return None  # No path exists

    path = []
    current = target

    while current is not None:
        path.append(current)
        current = previous.get(current)

    path.reverse()

    # Verify path starts from start node
    if path[0] != start:
        return None

    return path


def dijkstra_single_target(graph, start, target):
    """
    Optimized Dijkstra for single target (stops when target is found)
    """
    print(f"🎯 DIJKSTRA TO SINGLE TARGET: {start} → {target}")
    print("=" * 45)

    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous = {}
    priority_queue = [(0, start)]
    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        print(f"  Visiting: {current_node} (distance: {current_distance})")

        # Early termination when target is reached
        if current_node == target:
            print(f"🎉 Target {target} reached!")
            path = reconstruct_path(previous, start, target)
            return distances[target], path

        # Process neighbors
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in visited:
                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

    return float("inf"), None  # Target not reachable


def create_weighted_graph_examples():
    """
    Create example weighted graphs for testing
    """
    examples = {}

    # Simple weighted graph
    examples["simple"] = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 1), ("D", 5)],
        "C": [("D", 8), ("E", 10)],
        "D": [("E", 2)],
        "E": [],
    }

    # City network with distances
    examples["cities"] = {
        "New York": [("Boston", 215), ("Philadelphia", 95), ("Washington", 225)],
        "Boston": [("New York", 215), ("Chicago", 983)],
        "Philadelphia": [("New York", 95), ("Washington", 140), ("Pittsburgh", 305)],
        "Washington": [("New York", 225), ("Philadelphia", 140), ("Atlanta", 640)],
        "Pittsburgh": [("Philadelphia", 305), ("Chicago", 460), ("Atlanta", 760)],
        "Chicago": [("Boston", 983), ("Pittsburgh", 460), ("Denver", 1000)],
        "Atlanta": [("Washington", 640), ("Pittsburgh", 760), ("Miami", 650)],
        "Denver": [("Chicago", 1000), ("Los Angeles", 1015)],
        "Los Angeles": [("Denver", 1015), ("San Francisco", 380)],
        "San Francisco": [("Los Angeles", 380)],
        "Miami": [("Atlanta", 650)],
    }

    # Network with cycles
    examples["network"] = {
        0: [(1, 10), (3, 5)],
        1: [(2, 1), (3, 2)],
        2: [(4, 4)],
        3: [(1, 3), (2, 9), (4, 2)],
        4: [(0, 7), (2, 6)],
    }

    return examples


def demonstrate_dijkstra():
    """
    Comprehensive demonstration of Dijkstra's algorithm
    """
    print("🌟 DIJKSTRA'S ALGORITHM DEMONSTRATION")
    print("=" * 45)

    examples = create_weighted_graph_examples()

    # Test with simple graph
    print("Testing with simple weighted graph:")
    print("-" * 35)

    simple_graph = examples["simple"]
    print(f"Graph: {simple_graph}")

    # Visual representation
    print("\nGraph visualization:")
    print("    A ─4→ B")
    print("    │     │")
    print("    2     1")
    print("    ↓     ↓")
    print("    C ─8→ D ─2→ E")
    print("      10↗")
    print()

    # Run Dijkstra from A
    distances, previous = dijkstra_algorithm(simple_graph, "A")

    print("📊 FINAL RESULTS:")
    print(f"Shortest distances from A: {dict(distances)}")

    # Show paths to all nodes
    print("\nShortest paths from A:")
    for target in ["B", "C", "D", "E"]:
        path = reconstruct_path(previous, "A", target)
        if path:
            path_str = " → ".join(path)
            print(f"  A to {target}: {path_str} (distance: {distances[target]})")
        else:
            print(f"  A to {target}: No path")


def dijkstra_vs_bfs_comparison():
    """
    Compare Dijkstra with BFS to show why weights matter
    """
    print("\n🆚 DIJKSTRA vs BFS COMPARISON")
    print("=" * 35)

    # Graph where BFS and Dijkstra give different results
    graph = {"A": [("B", 1), ("C", 4)], "B": [("D", 100)], "C": [("D", 1)], "D": []}

    print("Test graph:")
    print("  A ─1→ B ─100→ D")
    print("  │              ↑")
    print("  4              1")
    print("  ↓              │")
    print("  C ─────────────┘")
    print()

    # BFS (unweighted shortest path)
    from collections import deque

    def bfs_shortest_path(graph, start, target):
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            node, path = queue.popleft()

            if node == target:
                return path

            for neighbor, _ in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    # Compare results
    start, target = "A", "D"

    # BFS result
    bfs_path = bfs_shortest_path(graph, start, target)
    print(f"BFS (unweighted) path A→D: {' → '.join(bfs_path)}")
    print(f"BFS path length: {len(bfs_path) - 1} edges")

    # Calculate BFS path weight
    bfs_weight = 0
    if bfs_path:
        for i in range(len(bfs_path) - 1):
            from_node, to_node = bfs_path[i], bfs_path[i + 1]
            for neighbor, weight in graph[from_node]:
                if neighbor == to_node:
                    bfs_weight += weight
                    break
    print(f"BFS path total weight: {bfs_weight}")

    # Dijkstra result
    dijkstra_distance, dijkstra_path = dijkstra_single_target(graph, start, target)
    print(f"\nDijkstra path A→D: {' → '.join(dijkstra_path)}")
    print(f"Dijkstra path weight: {dijkstra_distance}")

    print(f"\n💡 Key insight:")
    print(
        f"• BFS finds path with fewest edges: {len(bfs_path) - 1} edges, weight {bfs_weight}"
    )
    print(
        f"• Dijkstra finds path with minimum weight: {len(dijkstra_path) - 1} edges, weight {dijkstra_distance}"
    )
    print(f"• When edges have different weights, Dijkstra is the correct choice!")


def real_world_dijkstra_example():
    """
    Real-world example: GPS navigation system
    """
    print("\n🗺️ REAL-WORLD EXAMPLE: GPS Navigation")
    print("=" * 40)

    examples = create_weighted_graph_examples()
    cities_graph = examples["cities"]

    print("US Cities Network (distances in miles):")
    for city, connections in cities_graph.items():
        if connections:
            conn_str = ", ".join(f"{dest}({dist})" for dest, dist in connections)
            print(f"  {city}: {conn_str}")
        else:
            print(f"  {city}: No outgoing connections")

    # Find shortest route
    start_city = "New York"
    target_city = "Los Angeles"

    print(f"\nFinding shortest route: {start_city} → {target_city}")

    distance, path = dijkstra_single_target(cities_graph, start_city, target_city)

    if path:
        print(f"✅ Shortest route found!")
        print(f"   Path: {' → '.join(path)}")
        print(f"   Total distance: {distance} miles")

        # Show detailed route
        print(f"\n📍 Detailed route:")
        total_distance = 0
        for i in range(len(path) - 1):
            from_city = path[i]
            to_city = path[i + 1]

            # Find distance between cities
            for dest, dist in cities_graph[from_city]:
                if dest == to_city:
                    total_distance += dist
                    print(f"   {i+1}. {from_city} → {to_city}: {dist} miles")
                    break

        print(f"   Total: {total_distance} miles")
    else:
        print(f"❌ No route found!")


def dijkstra_applications():
    """
    Show various applications of Dijkstra's algorithm
    """
    print("\n🚀 DIJKSTRA'S ALGORITHM APPLICATIONS")
    print("=" * 40)

    print(
        """
REAL-WORLD APPLICATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━

1. 🗺️ GPS NAVIGATION
   - Shortest route between locations
   - Traffic-aware routing
   - Multi-modal transportation
   - Real-time route updates

2. 🌐 NETWORK ROUTING
   - Internet packet routing
   - Telecommunications networks
   - Data center traffic optimization
   - Content delivery networks

3. ✈️ FLIGHT SCHEDULING
   - Airline route optimization
   - Airport connection planning
   - Cargo logistics
   - Emergency rerouting

4. 🎮 GAME AI
   - NPC pathfinding
   - Resource optimization
   - Strategy game AI
   - Procedural content generation

5. 📊 FINANCIAL MODELING
   - Currency exchange optimization
   - Portfolio optimization
   - Risk analysis
   - Market arbitrage detection

6. 🏭 SUPPLY CHAIN
   - Warehouse optimization
   - Distribution planning
   - Cost minimization
   - Delivery scheduling

ALGORITHM CHARACTERISTICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ ADVANTAGES:
• Guarantees optimal shortest path
• Works with positive edge weights
• Efficient for sparse graphs
• Can find paths to all nodes

❌ LIMITATIONS:
• Requires non-negative weights
• O(V²) time with simple implementation
• O((V+E)logV) with binary heap
• Single-source only

VARIANTS & OPTIMIZATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━

• A* Search: Uses heuristics for faster pathfinding
• Bidirectional Dijkstra: Search from both ends
• Multi-source Dijkstra: Multiple starting points
• All-pairs shortest paths: Floyd-Warshall algorithm
"""
    )


def dijkstra_complexity_analysis():
    """
    Analyze time and space complexity of Dijkstra's algorithm
    """
    print("\n📊 COMPLEXITY ANALYSIS")
    print("=" * 25)

    print(
        """
TIME COMPLEXITY:
━━━━━━━━━━━━━━━━

Implementation        Time Complexity    Space Complexity
─────────────────────────────────────────────────────────
Simple (array)        O(V²)             O(V)
Binary heap           O((V+E)logV)      O(V)
Fibonacci heap        O(VlogV + E)      O(V)

Where: V = vertices, E = edges

SPACE BREAKDOWN:
━━━━━━━━━━━━━━━━

• Distance array: O(V)
• Previous array: O(V) 
• Priority queue: O(V)
• Visited set: O(V)
Total: O(V)

PERFORMANCE FACTORS:
━━━━━━━━━━━━━━━━━━━━

• Dense graphs (E ≈ V²): Binary heap preferred
• Sparse graphs (E ≈ V): Simple array may be better
• Multiple queries: Precompute all-pairs distances
• Large graphs: Consider approximation algorithms

OPTIMIZATION TECHNIQUES:
━━━━━━━━━━━━━━━━━━━━━━━━━

1. 🎯 Early termination for single target
2. 🔄 Bidirectional search for long paths  
3. 📊 A* search with heuristics
4. 🧠 Preprocessing for repeated queries
5. 📈 Parallel/distributed computation
"""
    )


def advanced_dijkstra_variants():
    """
    Show advanced variants and optimizations
    """
    print("\n🔬 ADVANCED DIJKSTRA VARIANTS")
    print("=" * 35)

    print(
        """
ADVANCED VARIANTS:
━━━━━━━━━━━━━━━━━━

1. 🎯 A* SEARCH
   - Uses heuristic function h(n)
   - f(n) = g(n) + h(n)
   - Faster for single target
   - Requires admissible heuristic

2. 🔄 BIDIRECTIONAL DIJKSTRA
   - Search from both start and end
   - Meet in the middle
   - ~2x faster for long paths
   - More complex implementation

3. 🌟 MULTI-SOURCE DIJKSTRA
   - Multiple starting points
   - Find nearest facility
   - Emergency services optimization
   - Market analysis

4. 📊 K-SHORTEST PATHS
   - Find K best paths
   - Alternative route planning
   - Risk analysis
   - Backup planning

5. 🎮 DYNAMIC DIJKSTRA
   - Handle graph changes
   - Real-time updates
   - Traffic-aware routing
   - Network optimization
"""
    )

    # Example: Simple A* implementation
    def a_star_search(graph, start, goal, heuristic):
        """
        A* search algorithm (simplified version)
        """
        import heapq

        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            for neighbor, weight in graph.get(current, []):
                tentative_g = g_score[current] + weight

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found

    # Example heuristic (Manhattan distance for grid)
    def manhattan_heuristic(node, goal):
        # Simplified: assume nodes are coordinates
        if isinstance(node, tuple) and isinstance(goal, tuple):
            return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
        return 0  # Default for non-coordinate nodes

    print("\nExample A* vs Dijkstra:")
    print("• A* uses heuristic to guide search toward goal")
    print("• Explores fewer nodes than Dijkstra")
    print("• Still guarantees optimal path (with admissible heuristic)")


def dijkstra_implementation_guide():
    """
    Step-by-step implementation guide
    """
    print("\n📋 IMPLEMENTATION GUIDE")
    print("=" * 25)

    print(
        """
STEP-BY-STEP ALGORITHM:
━━━━━━━━━━━━━━━━━━━━━━━

1. 🏁 INITIALIZATION
   - Set distance to start = 0
   - Set all other distances = ∞
   - Create empty priority queue
   - Add start to priority queue

2. 🔄 MAIN LOOP (while queue not empty)
   - Extract node with minimum distance
   - Mark node as visited
   - For each unvisited neighbor:
     * Calculate new distance
     * If shorter than current distance:
       → Update distance
       → Update previous node
       → Add to priority queue

3. 🎯 TERMINATION
   - All reachable nodes processed
   - Distances array contains shortest distances
   - Previous array allows path reconstruction

IMPLEMENTATION TEMPLATE:
━━━━━━━━━━━━━━━━━━━━━━━

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {}
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)
        
        for neighbor, weight in graph[current]:
            new_dist = current_dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances, previous
```

COMMON PITFALLS:
━━━━━━━━━━━━━━━━

❌ Forgetting to check if node already visited
❌ Using negative edge weights
❌ Not handling disconnected components
❌ Incorrect priority queue usage
❌ Forgetting to update previous pointers

DEBUGGING TIPS:
━━━━━━━━━━━━━━━

✅ Print distances at each step
✅ Verify priority queue ordering
✅ Check graph representation
✅ Test with simple examples first
✅ Validate final paths manually
"""
    )


def dijkstra_quiz_and_exercises():
    """
    Interactive quiz and exercises
    """
    print("\n🧠 DIJKSTRA'S ALGORITHM QUIZ")
    print("=" * 30)

    print(
        """
QUICK QUIZ:
━━━━━━━━━━━

1. ❓ What is the time complexity of Dijkstra's with binary heap?
   Answer: O((V+E)logV)

2. ❓ Can Dijkstra handle negative edge weights?
   Answer: No, it requires non-negative weights

3. ❓ What data structure is used for the priority queue?
   Answer: Binary heap (min-heap)

4. ❓ How do you reconstruct the shortest path?
   Answer: Follow the 'previous' pointers backward from target

5. ❓ When would you use A* instead of Dijkstra?
   Answer: When you have a good heuristic and single target

PRACTICE EXERCISES:
━━━━━━━━━━━━━━━━━━━

Exercise 1: Implement Dijkstra for this graph
    A ─3→ B ─2→ C
    │     │     │
    4     1     1
    ↓     ↓     ↓
    D ─1→ E ─3→ F

Exercise 2: Find shortest path A→F step by step

Exercise 3: Modify algorithm to:
• Stop when target is found
• Find K shortest paths
• Handle bidirectional search

Exercise 4: Compare with BFS on unweighted graph

Exercise 5: Implement with different data structures:
• Simple array vs binary heap
• Measure performance difference
"""
    )


if __name__ == "__main__":
    # Main demonstration
    demonstrate_dijkstra()

    # Compare with BFS
    dijkstra_vs_bfs_comparison()

    # Real-world example
    real_world_dijkstra_example()

    # Show applications
    dijkstra_applications()

    # Complexity analysis
    dijkstra_complexity_analysis()

    # Advanced variants
    advanced_dijkstra_variants()

    # Implementation guide
    dijkstra_implementation_guide()

    # Quiz and exercises
    dijkstra_quiz_and_exercises()

    print("\n✅ You now master Dijkstra's shortest path algorithm!")
    print("🎯 This completes your graph algorithms journey!")
    print(
        "💡 Key insight: Choose the right algorithm for your specific problem constraints!"
    )
