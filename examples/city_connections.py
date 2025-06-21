"""
City Connections Example
========================
Example showing how cities connect via roads, flights, etc.
"""

from collections import deque
import heapq


def create_road_network():
    """
    Create a simple road network between cities
    """
    # Roads between cities (undirected)
    roads = {
        "Mumbai": ["Delhi", "Pune", "Ahmedabad"],
        "Delhi": ["Mumbai", "Chandigarh", "Jaipur"],
        "Bangalore": ["Chennai", "Hyderabad", "Mumbai"],
        "Chennai": ["Bangalore", "Hyderabad"],
        "Pune": ["Mumbai", "Ahmedabad"],
        "Chandigarh": ["Delhi"],
        "Jaipur": ["Delhi"],
        "Hyderabad": ["Bangalore", "Chennai"],
        "Ahmedabad": ["Mumbai", "Pune"],
    }
    return roads


def create_flight_network():
    """
    Create flight network with costs
    """
    # Flights with costs (city -> [(destination, cost)])
    flights = {
        "Mumbai": [("Delhi", 6000), ("Bangalore", 8000), ("Dubai", 18000)],
        "Delhi": [("Mumbai", 6000), ("Chandigarh", 4000), ("London", 65000)],
        "Bangalore": [("Mumbai", 8000), ("Chennai", 5000), ("Singapore", 22000)],
        "Chennai": [("Bangalore", 5000), ("Dubai", 20000), ("Singapore", 25000)],
        "Dubai": [("Mumbai", 18000), ("Chennai", 20000), ("London", 30000)],
        "London": [("Delhi", 65000), ("Dubai", 30000), ("New York", 45000)],
        "Singapore": [("Bangalore", 22000), ("Chennai", 25000), ("New York", 80000)],
        "New York": [("London", 45000), ("Singapore", 80000)],
    }
    return flights


def show_network(network, title, weighted=False):
    """
    Display any network clearly
    """
    print(f"🗺️ {title}")
    print("=" * (len(title) + 4))

    for city, connections in network.items():
        if weighted:
            conn_str = ", ".join(f"{dest}(₹{cost})" for dest, cost in connections)
        else:
            conn_str = ", ".join(connections)
        print(f"  {city}: {conn_str}")

    total_connections = sum(len(connections) for connections in network.values())
    if not weighted:
        total_connections //= 2  # Each road counted twice

    print(f"\nTotal cities: {len(network)}")
    print(f"Total connections: {total_connections}")


def find_road_route(roads, start_city, end_city):
    """
    Find route between cities using roads (BFS)
    """
    print(f"\n🛣️ Finding road route: {start_city} → {end_city}")

    if start_city == end_city:
        print(f"  Already there!")
        return [start_city]

    visited = set([start_city])
    queue = deque([(start_city, [start_city])])

    while queue:
        current_city, route = queue.popleft()

        for connected_city in roads.get(current_city, []):
            if connected_city == end_city:
                final_route = route + [connected_city]
                print(f"  ✅ Route found: {' → '.join(final_route)}")
                print(f"  Cities to pass through: {len(final_route) - 1}")
                return final_route

            if connected_city not in visited:
                visited.add(connected_city)
                queue.append((connected_city, route + [connected_city]))

    print(f"  ❌ No road route found")
    return None


def find_cheapest_flight(flights, start_city, end_city):
    """
    Find cheapest flight route using Dijkstra's algorithm
    """
    print(f"\n✈️ Finding cheapest flight: {start_city} → {end_city}")

    if start_city not in flights:
        print(f"  ❌ No flights from {start_city}")
        return None, 0

    # Dijkstra's algorithm
    distances = {city: float("inf") for city in flights}
    distances[start_city] = 0
    previous = {}
    unvisited = [(0, start_city)]

    while unvisited:
        current_cost, current_city = heapq.heappop(unvisited)

        if current_city == end_city:
            # Reconstruct path
            route = []
            city = end_city
            while city in previous:
                route.append(city)
                city = previous[city]
            route.append(start_city)
            route.reverse()

            print(f"  ✅ Cheapest route: {' → '.join(route)}")
            print(f"  Total cost: ₹{current_cost}")
            return route, current_cost

        # Check all flights from current city
        for destination, cost in flights.get(current_city, []):
            new_cost = current_cost + cost

            if new_cost < distances[destination]:
                distances[destination] = new_cost
                previous[destination] = current_city
                heapq.heappush(unvisited, (new_cost, destination))

    print(f"  ❌ No flight route found")
    return None, 0


def compare_transportation():
    """
    Compare different ways to travel between cities
    """
    print(f"\n🚗🛣️✈️ COMPARING TRANSPORTATION OPTIONS")
    print("=" * 45)

    roads = create_road_network()
    flights = create_flight_network()

    # Test routes
    test_routes = [
        ("Mumbai", "Chennai"),
        ("Delhi", "Singapore"),
        ("Bangalore", "London"),
    ]

    for start, end in test_routes:
        print(f"\n📍 Traveling from {start} to {end}:")
        print("-" * 30)

        # Try by road
        road_route = find_road_route(roads, start, end)

        # Try by flight
        flight_route, flight_cost = find_cheapest_flight(flights, start, end)

        # Compare
        print(f"  📊 Comparison:")
        if road_route:
            print(f"    Road: {len(road_route)-1} stops, likely cheaper but slower")
        if flight_route:
            print(f"    Flight: ₹{flight_cost}, faster but more expensive")


def find_all_reachable_cities(network, start_city, max_stops=3):
    """
    Find all cities reachable within a certain number of stops
    """
    print(f"\n🎯 Cities reachable from {start_city} in {max_stops} stops:")

    visited = set()
    current_level = [start_city]
    all_reachable = {start_city: 0}  # city -> minimum stops

    for stop in range(1, max_stops + 1):
        next_level = []

        for city in current_level:
            for neighbor in network.get(city, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_level.append(neighbor)
                    all_reachable[neighbor] = stop

        if next_level:
            print(f"  {stop} stop(s): {next_level}")

        current_level = next_level

    print(f"\n  Summary: {len(all_reachable)} cities reachable")
    for city, stops in sorted(all_reachable.items()):
        if stops == 0:
            print(f"    {city}: Starting point")
        else:
            print(f"    {city}: {stops} stop(s) away")


def check_connectivity(network, city1, city2):
    """
    Check if two cities are connected (any path exists)
    """
    print(f"\n🔗 Checking if {city1} and {city2} are connected:")

    if city1 not in network or city2 not in network:
        print(f"  ❌ One or both cities not in network")
        return False

    visited = set()
    queue = deque([city1])
    visited.add(city1)

    while queue:
        current = queue.popleft()

        if current == city2:
            print(f"  ✅ {city1} and {city2} are connected!")
            return True

        for neighbor in network.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    print(f"  ❌ {city1} and {city2} are NOT connected")
    return False


def find_travel_hub(network):
    """
    Find the city that connects to the most other cities
    """
    print(f"\n🌟 Finding travel hub (most connected city):")

    connection_count = {}

    for city, connections in network.items():
        connection_count[city] = len(connections)

    # Sort by number of connections
    sorted_cities = sorted(connection_count.items(), key=lambda x: x[1], reverse=True)

    print(f"  Cities ranked by connections:")
    for i, (city, count) in enumerate(sorted_cities, 1):
        print(f"    {i}. {city}: {count} direct connections")

    hub_city = sorted_cities[0][0]
    print(f"\n  🏆 Travel hub: {hub_city}")
    return hub_city


def emergency_routes(roads, from_city):
    """
    Find all possible escape routes from a city
    """
    print(f"\n🚨 Emergency routes from {from_city}:")

    if from_city not in roads:
        print(f"  ❌ {from_city} not found in road network")
        return

    direct_routes = roads[from_city]
    print(f"  Direct routes: {direct_routes}")

    # Find routes with 1 connection
    one_stop_routes = {}
    for intermediate_city in direct_routes:
        for final_city in roads.get(intermediate_city, []):
            if final_city != from_city and final_city not in direct_routes:
                if intermediate_city not in one_stop_routes:
                    one_stop_routes[intermediate_city] = []
                one_stop_routes[intermediate_city].append(final_city)

    if one_stop_routes:
        print(f"  One-stop routes:")
        for intermediate, destinations in one_stop_routes.items():
            print(f"    Via {intermediate}: {destinations}")


def tourism_planning():
    """
    Plan tourism routes visiting multiple cities
    """
    print(f"\n🎒 TOURISM ROUTE PLANNING")
    print("=" * 30)

    roads = create_road_network()

    # Popular tourist destinations
    tourist_spots = ["Mumbai", "Delhi", "Bangalore"]

    print(f"Must-visit cities: {tourist_spots}")
    print(f"\nPossible touring routes:")

    # Generate different route combinations
    import itertools

    route_count = 0
    for route in itertools.permutations(tourist_spots):
        route_count += 1
        route_list = list(route)

        # Check if this route is possible
        route_possible = True
        total_legs = []

        for i in range(len(route_list) - 1):
            current_city = route_list[i]
            next_city = route_list[i + 1]

            # Find route between current and next city
            temp_route = find_road_route(roads, current_city, next_city)
            if not temp_route:
                route_possible = False
                break
            else:
                total_legs.append(f"{current_city}→{next_city}")

        if route_possible:
            print(f"  Route {route_count}: {' then '.join(total_legs)}")
        else:
            print(
                f"  Route {route_count}: {' then '.join(total_legs)} (❌ Not possible)"
            )


def practical_tips():
    """
    Practical tips for using graph algorithms in transportation
    """
    print(f"\n💡 PRACTICAL TIPS FOR TRANSPORTATION NETWORKS")
    print("=" * 50)

    print(
        """
🗺️ REAL-WORLD APPLICATIONS:

1. 📱 GPS NAVIGATION
   • Use Dijkstra for shortest/fastest routes
   • Consider traffic, road conditions, tolls
   • Real-time updates for optimal paths

2. ✈️ FLIGHT BOOKING
   • Find cheapest connections
   • Consider layover times
   • Multiple airlines and alliances

3. 🚌 PUBLIC TRANSPORT
   • Bus/train route planning
   • Transfer optimization
   • Schedule coordination

4. 🚚 DELIVERY SERVICES
   • Optimize delivery routes
   • Minimize fuel costs
   • Handle multiple destinations

⚡ ALGORITHM CHOICES:

• BFS: Shortest path (minimum stops)
• Dijkstra: Cheapest/fastest path (weighted)
• DFS: Check if route exists
• Floyd-Warshall: All-pairs shortest paths

🎯 OPTIMIZATION TIPS:

• Cache frequently requested routes
• Use heuristics for large networks
• Consider bidirectional search
• Pre-compute popular destinations
• Update network in real-time
"""
    )


if __name__ == "__main__":
    print("🌍 CITY CONNECTIONS NETWORK ANALYSIS")
    print("=" * 45)

    # Create networks
    roads = create_road_network()
    flights = create_flight_network()

    # Show networks
    show_network(roads, "ROAD NETWORK")
    print()
    show_network(flights, "FLIGHT NETWORK", weighted=True)

    # Test basic routing
    print("\n" + "=" * 60)
    find_road_route(roads, "Mumbai", "Chennai")
    find_cheapest_flight(flights, "Delhi", "New York")

    # Compare transportation options
    print("\n" + "=" * 60)
    compare_transportation()

    # Reachability analysis
    print("\n" + "=" * 60)
    find_all_reachable_cities(roads, "Mumbai", 2)

    # Connectivity checks
    print("\n" + "=" * 60)
    check_connectivity(roads, "Mumbai", "Chennai")
    check_connectivity(roads, "Pune", "Chandigarh")

    # Find travel hub
    print("\n" + "=" * 60)
    find_travel_hub(roads)

    # Emergency planning
    print("\n" + "=" * 60)
    emergency_routes(roads, "Delhi")

    # Tourism planning
    print("\n" + "=" * 60)
    tourism_planning()

    # Practical tips
    print("\n" + "=" * 60)
    practical_tips()

    print("\n🎉 CITY CONNECTIONS ANALYSIS COMPLETE!")
    print("🎯 Key Takeaway: Different algorithms for different travel needs!")
    print("💡 BFS for shortest routes, Dijkstra for cheapest/fastest!")
