"""
Shortest Path Algorithms
"""

from collections import deque
import heapq


def bfs_shortest_path(graph, start, end):
    """
    Find shortest path using BFS (works for unweighted graphs)
    """
    print(f"🎯 Finding shortest path: {start} → {end}")

    if start == end:
        return [start]

    # BFS setup
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current_node, path = queue.popleft()
        print(f"  Checking: {current_node}")

        # Look at neighbors
        for neighbor in graph.get(current_node, []):
            if neighbor == end:
                final_path = path + [neighbor]
                print(f"  ✅ Found path: {' → '.join(final_path)}")
                return final_path

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    print("  ❌ No path found")
    return None


def dijkstra_simple(graph, start, end):
    """
    Simple Dijkstra for weighted graphs
    Finds cheapest/shortest path by weight
    """
    print(f"💰 Finding cheapest path: {start} → {end}")

    # Setup
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous = {}
    unvisited = [(0, start)]

    while unvisited:
        current_dist, current_node = heapq.heappop(unvisited)
        print(f"  Visiting: {current_node} (cost: {current_dist})")

        if current_node == end:
            # Build path
            path = []
            node = end
            while node in previous:
                path.append(node)
                node = previous[node]
            path.append(start)
            path.reverse()

            print(
                f"  ✅ Found cheapest path: {' → '.join(path)} (cost: {current_dist})"
            )
            return path, current_dist

        # Check neighbors
        for neighbor, weight in graph.get(current_node, []):
            new_dist = current_dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(unvisited, (new_dist, neighbor))
                print(f"    Updated {neighbor}: cost {new_dist}")

    print("  ❌ No path found")
    return None, float("inf")


def compare_paths(graph_unweighted, graph_weighted, start, end):
    """
    Compare BFS vs Dijkstra on the same route
    """
    print("🆚 COMPARING PATH ALGORITHMS")
    print("=" * 35)

    # BFS on unweighted graph
    print("\n1. BFS (counts steps only):")
    bfs_path = bfs_shortest_path(graph_unweighted, start, end)
    if bfs_path:
        print(f"   Steps: {len(bfs_path) - 1}")

    # Dijkstra on weighted graph
    print("\n2. Dijkstra (considers weights):")
    dijkstra_path, cost = dijkstra_simple(graph_weighted, start, end)
    if dijkstra_path:
        print(f"   Steps: {len(dijkstra_path) - 1}, Total cost: {cost}")

    # Summary
    print(f"\n📊 Summary:")
    print(f"   BFS: Good for 'fewest steps'")
    print(f"   Dijkstra: Good for 'lowest cost'")


def simple_example():
    """
    Simple example anyone can understand
    """
    print("🏠 SIMPLE EXAMPLE: Getting to School")
    print("=" * 40)

    # Unweighted graph (just connections)
    places = {
        "Home": ["Park", "Store"],
        "Park": ["Home", "School"],
        "Store": ["Home", "Mall", "School"],
        "Mall": ["Store"],
        "School": [],
    }

    # Weighted graph (with distances in minutes)
    places_with_time = {
        "Home": [("Park", 5), ("Store", 10)],
        "Park": [("Home", 5), ("School", 15)],
        "Store": [("Home", 10), ("Mall", 5), ("School", 8)],
        "Mall": [("Store", 5)],
        "School": [],
    }

    print("Places and connections:")
    for place, connections in places.items():
        print(f"  {place}: {connections}")

    compare_paths(places, places_with_time, "Home", "School")


def city_example():
    """
    City transportation example
    """
    print("\n🏙️ CITY EXAMPLE: Traveling Between Cities")
    print("=" * 45)

    # Unweighted (just connections)
    cities = {
        "New York": ["Boston", "Philadelphia"],
        "Boston": ["New York", "Chicago"],
        "Philadelphia": ["New York", "Washington"],
        "Washington": ["Philadelphia", "Atlanta"],
        "Chicago": ["Boston", "Denver"],
        "Atlanta": ["Washington", "Miami"],
        "Denver": ["Chicago", "Los Angeles"],
        "Los Angeles": ["Denver"],
        "Miami": ["Atlanta"],
    }

    # Weighted (with costs in dollars)
    cities_with_cost = {
        "New York": [("Boston", 50), ("Philadelphia", 30)],
        "Boston": [("New York", 50), ("Chicago", 150)],
        "Philadelphia": [("New York", 30), ("Washington", 40)],
        "Washington": [("Philadelphia", 40), ("Atlanta", 80)],
        "Chicago": [("Boston", 150), ("Denver", 200)],
        "Atlanta": [("Washington", 80), ("Miami", 100)],
        "Denver": [("Chicago", 200), ("Los Angeles", 250)],
        "Los Angeles": [("Denver", 250)],
        "Miami": [("Atlanta", 100)],
    }

    compare_paths(cities, cities_with_cost, "New York", "Los Angeles")


def when_to_use_what():
    """
    Simple guide on when to use each algorithm
    """
    print("\n🤔 WHEN TO USE WHAT?")
    print("=" * 25)

    print(
        """
📋 SIMPLE DECISION GUIDE:

🌊 Use BFS when:
   • All connections are equal (unweighted)
   • You want fewest steps/hops
   • Simple graphs
   • Example: Social network connections

💰 Use Dijkstra when:
   • Connections have different costs (weighted) 
   • You want lowest total cost
   • Example: GPS routing, flight costs

📊 Quick Comparison:
┌─────────────┬─────────────┬─────────────┐
│ Algorithm   │ Best For    │ Works With  │
├─────────────┼─────────────┼─────────────┤
│ BFS         │ Fewest hops │ Unweighted  │
│ Dijkstra    │ Lowest cost │ Weighted    │
└─────────────┴─────────────┴─────────────┘

💡 Remember:
• BFS = Fast and simple
• Dijkstra = More powerful but complex
• Both guarantee optimal results!
"""
    )


if __name__ == "__main__":
    # Run simple examples
    simple_example()
    city_example()
    when_to_use_what()

    print("\n✅ You now understand shortest path algorithms!")
    print("🎯 Key takeaway: Choose based on whether your graph has weights!")
