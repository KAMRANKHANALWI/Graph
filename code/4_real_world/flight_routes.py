"""
Flight Route Optimization with Graphs
=====================================
Real-world application: Analyze flight networks and find optimal routes.
"""

from collections import deque, defaultdict
import heapq


class FlightNetwork:
    """
    Flight network management system using graph algorithms
    """

    def __init__(self):
        self.routes = {}  # city -> [(destination, distance, price, duration)]
        self.city_info = {}  # city -> {timezone, country, etc.}

    def add_city(self, city_code, info=None):
        """Add a city to the network"""
        if city_code not in self.routes:
            self.routes[city_code] = []
            self.city_info[city_code] = info or {}
            return True
        return False

    def add_flight(self, from_city, to_city, distance, price, duration):
        """Add a flight route between cities"""
        # Ensure cities exist
        self.add_city(from_city)
        self.add_city(to_city)

        # Add flight (directed - flights are one-way)
        flight_info = {
            "destination": to_city,
            "distance": distance,
            "price": price,
            "duration": duration,
        }
        self.routes[from_city].append(flight_info)
        print(
            f"✈️ Added flight: {from_city} → {to_city} ({distance}km, ${price}, {duration}h)"
        )

    def find_shortest_route_distance(self, start, destination):
        """
        Find shortest route by distance using Dijkstra's algorithm
        """
        print(f"🎯 Finding shortest route by DISTANCE: {start} → {destination}")

        if start not in self.routes or destination not in self.routes:
            return None, None

        # Dijkstra's algorithm
        distances = {city: float("inf") for city in self.routes}
        distances[start] = 0
        previous = {}
        priority_queue = [(0, start)]
        visited = set()

        while priority_queue:
            current_distance, current_city = heapq.heappop(priority_queue)

            if current_city in visited:
                continue

            visited.add(current_city)
            print(f"  Visiting {current_city} (distance: {current_distance}km)")

            if current_city == destination:
                # Reconstruct path
                path = []
                city = destination
                total_distance = distances[destination]

                while city in previous:
                    path.append(city)
                    city = previous[city]
                path.append(start)
                path.reverse()

                return path, total_distance

            # Check all flights from current city
            for flight in self.routes[current_city]:
                neighbor = flight["destination"]
                distance = flight["distance"]
                new_distance = current_distance + distance

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_city
                    heapq.heappush(priority_queue, (new_distance, neighbor))
                    print(f"    Updated distance to {neighbor}: {new_distance}km")

        return None, None  # No route found

    def find_cheapest_route(self, start, destination):
        """
        Find cheapest route by price using modified Dijkstra's
        """
        print(f"💰 Finding CHEAPEST route: {start} → {destination}")

        if start not in self.routes or destination not in self.routes:
            return None, None

        prices = {city: float("inf") for city in self.routes}
        prices[start] = 0
        previous = {}
        priority_queue = [(0, start)]
        visited = set()

        while priority_queue:
            current_price, current_city = heapq.heappop(priority_queue)

            if current_city in visited:
                continue

            visited.add(current_city)
            print(f"  Visiting {current_city} (price: ${current_price})")

            if current_city == destination:
                # Reconstruct path
                path = []
                city = destination
                total_price = prices[destination]

                while city in previous:
                    path.append(city)
                    city = previous[city]
                path.append(start)
                path.reverse()

                return path, total_price

            # Check all flights from current city
            for flight in self.routes[current_city]:
                neighbor = flight["destination"]
                price = flight["price"]
                new_price = current_price + price

                if new_price < prices[neighbor]:
                    prices[neighbor] = new_price
                    previous[neighbor] = current_city
                    heapq.heappush(priority_queue, (new_price, neighbor))
                    print(f"    Updated price to {neighbor}: ${new_price}")

        return None, None

    def find_fastest_route(self, start, destination):
        """
        Find fastest route by duration
        """
        print(f"⚡ Finding FASTEST route: {start} → {destination}")

        if start not in self.routes or destination not in self.routes:
            return None, None

        durations = {city: float("inf") for city in self.routes}
        durations[start] = 0
        previous = {}
        priority_queue = [(0, start)]
        visited = set()

        while priority_queue:
            current_duration, current_city = heapq.heappop(priority_queue)

            if current_city in visited:
                continue

            visited.add(current_city)

            if current_city == destination:
                # Reconstruct path
                path = []
                city = destination
                total_duration = durations[destination]

                while city in previous:
                    path.append(city)
                    city = previous[city]
                path.append(start)
                path.reverse()

                return path, total_duration

            # Check all flights from current city
            for flight in self.routes[current_city]:
                neighbor = flight["destination"]
                duration = flight["duration"]
                new_duration = current_duration + duration

                if new_duration < durations[neighbor]:
                    durations[neighbor] = new_duration
                    previous[neighbor] = current_city
                    heapq.heappush(priority_queue, (new_duration, neighbor))

        return None, None

    def find_all_routes_with_stops(self, start, destination, max_stops=3):
        """
        Find all possible routes with maximum number of stops using DFS
        """
        print(
            f"🛣️ Finding all routes with max {max_stops} stops: {start} → {destination}"
        )

        all_routes = []

        def dfs_routes(current_city, path, stops):
            if stops > max_stops:
                return

            if current_city == destination and len(path) > 1:
                route_info = self._calculate_route_totals(path)
                all_routes.append((path.copy(), route_info))
                return

            for flight in self.routes.get(current_city, []):
                next_city = flight["destination"]
                if next_city not in path:  # Avoid cycles
                    path.append(next_city)
                    dfs_routes(next_city, path, stops + 1)
                    path.pop()

        dfs_routes(start, [start], 0)
        return all_routes

    def _calculate_route_totals(self, path):
        """Calculate total distance, price, and duration for a route"""
        total_distance = 0
        total_price = 0
        total_duration = 0

        for i in range(len(path) - 1):
            from_city = path[i]
            to_city = path[i + 1]

            # Find the flight between these cities
            for flight in self.routes.get(from_city, []):
                if flight["destination"] == to_city:
                    total_distance += flight["distance"]
                    total_price += flight["price"]
                    total_duration += flight["duration"]
                    break

        return {
            "distance": total_distance,
            "price": total_price,
            "duration": total_duration,
            "stops": len(path) - 2,  # excluding start and destination
        }

    def find_hub_cities(self, top_n=5):
        """
        Find hub cities (most connected airports)
        """
        # Count outgoing and incoming flights
        outgoing = {city: len(flights) for city, flights in self.routes.items()}
        incoming = defaultdict(int)

        for city, flights in self.routes.items():
            for flight in flights:
                incoming[flight["destination"]] += 1

        # Calculate total connections
        total_connections = {}
        for city in self.routes:
            total_connections[city] = outgoing.get(city, 0) + incoming.get(city, 0)

        # Sort by total connections
        sorted_hubs = sorted(
            total_connections.items(), key=lambda x: x[1], reverse=True
        )

        return sorted_hubs[:top_n]

    def analyze_network(self):
        """
        Comprehensive flight network analysis
        """
        print("📊 FLIGHT NETWORK ANALYSIS")
        print("=" * 30)

        total_cities = len(self.routes)
        total_routes = sum(len(flights) for flights in self.routes.values())

        print(f"🏙️ Total cities: {total_cities}")
        print(f"✈️ Total routes: {total_routes}")

        if total_cities > 0:
            avg_routes_per_city = total_routes / total_cities
            print(f"📊 Average routes per city: {avg_routes_per_city:.1f}")

        # Find hub cities
        hubs = self.find_hub_cities(3)
        print(f"🌟 Top hub cities:")
        for i, (city, connections) in enumerate(hubs, 1):
            print(f"   {i}. {city} ({connections} connections)")

        # Check connectivity
        connected_components = self._find_connected_components()
        print(f"🔗 Connected components: {len(connected_components)}")

        if len(connected_components) == 1:
            print("   ✅ All cities are reachable from each other")
        else:
            print("   ❌ Some cities are isolated")
            for i, component in enumerate(connected_components, 1):
                print(f"     Component {i}: {component}")

    def _find_connected_components(self):
        """Find connected components in the flight network"""
        visited = set()
        components = []

        def dfs(city, component):
            visited.add(city)
            component.append(city)

            # Check outgoing flights
            for flight in self.routes.get(city, []):
                destination = flight["destination"]
                if destination not in visited:
                    dfs(destination, component)

            # Check incoming flights (treat as undirected for connectivity)
            for other_city, flights in self.routes.items():
                for flight in flights:
                    if flight["destination"] == city and other_city not in visited:
                        dfs(other_city, component)

        for city in self.routes:
            if city not in visited:
                component = []
                dfs(city, component)
                components.append(sorted(component))

        return components


def create_example_flight_network():
    """
    Create a realistic flight network example
    """
    print("🏗️ CREATING EXAMPLE FLIGHT NETWORK")
    print("=" * 35)

    network = FlightNetwork()

    # Add major cities with information
    cities = {
        "NYC": {"name": "New York", "country": "USA", "timezone": "EST"},
        "LAX": {"name": "Los Angeles", "country": "USA", "timezone": "PST"},
        "LHR": {"name": "London", "country": "UK", "timezone": "GMT"},
        "CDG": {"name": "Paris", "country": "France", "timezone": "CET"},
        "NRT": {"name": "Tokyo", "country": "Japan", "timezone": "JST"},
        "DXB": {"name": "Dubai", "country": "UAE", "timezone": "GST"},
        "SIN": {"name": "Singapore", "country": "Singapore", "timezone": "SGT"},
        "SYD": {"name": "Sydney", "country": "Australia", "timezone": "AEDT"},
    }

    for code, info in cities.items():
        network.add_city(code, info)

    # Add flight routes (from_city, to_city, distance_km, price_usd, duration_hours)
    flights = [
        # North America routes
        ("NYC", "LAX", 3944, 350, 6.0),
        ("LAX", "NYC", 3944, 380, 5.5),
        # Transatlantic routes
        ("NYC", "LHR", 5585, 600, 7.0),
        ("LHR", "NYC", 5585, 650, 8.0),
        ("NYC", "CDG", 5837, 580, 7.5),
        ("CDG", "NYC", 5837, 620, 8.5),
        # European routes
        ("LHR", "CDG", 344, 150, 1.5),
        ("CDG", "LHR", 344, 160, 1.5),
        # Hub to Asia routes
        ("LHR", "DXB", 5500, 450, 7.0),
        ("DXB", "LHR", 5500, 480, 7.5),
        ("CDG", "DXB", 5253, 420, 6.5),
        ("DXB", "CDG", 5253, 450, 7.0),
        # Dubai hub routes
        ("DXB", "NRT", 7003, 520, 9.0),
        ("NRT", "DXB", 7003, 550, 10.0),
        ("DXB", "SIN", 5586, 380, 7.5),
        ("SIN", "DXB", 5586, 400, 8.0),
        ("DXB", "SYD", 11908, 680, 14.0),
        ("SYD", "DXB", 11908, 720, 15.0),
        # Asia-Pacific routes
        ("NRT", "SIN", 5312, 420, 7.0),
        ("SIN", "NRT", 5312, 450, 6.5),
        ("SIN", "SYD", 6317, 380, 8.0),
        ("SYD", "SIN", 6317, 400, 7.5),
        # Trans-Pacific routes
        ("LAX", "NRT", 8817, 650, 11.5),
        ("NRT", "LAX", 8817, 680, 10.0),
        ("LAX", "SYD", 12051, 750, 15.0),
        ("SYD", "LAX", 12051, 800, 13.5),
    ]

    print("\nAdding flight routes:")
    for flight in flights:
        network.add_flight(*flight)

    return network


def demonstrate_route_optimization():
    """
    Demonstrate various route optimization strategies
    """
    network = create_example_flight_network()

    print("\n" + "=" * 60)

    # Network analysis
    network.analyze_network()

    print("\n" + "=" * 60)
    print("🎯 ROUTE OPTIMIZATION EXAMPLES")
    print("=" * 35)

    start, destination = "NYC", "SYD"

    # Find different types of optimal routes
    print(f"\nFinding routes from {start} to {destination}:")

    # Shortest distance
    path_dist, total_dist = network.find_shortest_route_distance(start, destination)
    if path_dist:
        print(f"\n🏃 Shortest by distance: {' → '.join(path_dist)}")
        print(f"   Total distance: {total_dist:.0f} km")

    # Cheapest price
    path_price, total_price = network.find_cheapest_route(start, destination)
    if path_price:
        print(f"\n💰 Cheapest by price: {' → '.join(path_price)}")
        print(f"   Total price: ${total_price:.0f}")

    # Fastest duration
    path_time, total_time = network.find_fastest_route(start, destination)
    if path_time:
        print(f"\n⚡ Fastest by time: {' → '.join(path_time)}")
        print(f"   Total duration: {total_time:.1f} hours")

    # All possible routes
    print(f"\n🛣️ All possible routes (max 2 stops):")
    all_routes = network.find_all_routes_with_stops(start, destination, 2)

    for i, (path, info) in enumerate(all_routes[:5], 1):  # Show top 5
        print(f"   Route {i}: {' → '.join(path)}")
        print(
            f"     Distance: {info['distance']}km, Price: ${info['price']}, Time: {info['duration']:.1f}h"
        )
        print(f"     Stops: {info['stops']}")


def flight_route_applications():
    """
    Show practical applications of flight route optimization
    """
    print("\n🚀 FLIGHT ROUTE OPTIMIZATION APPLICATIONS")
    print("=" * 45)

    print(
        """
REAL-WORLD APPLICATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━

1. ✈️ AIRLINE ROUTE PLANNING
   - Optimize flight schedules
   - Minimize fuel costs
   - Maximize passenger convenience
   - Hub-and-spoke vs point-to-point

2. 🎫 TRAVEL BOOKING SYSTEMS
   - Find cheapest combinations
   - Balance price vs convenience
   - Multi-city trip planning
   - Real-time route updates

3. 📊 NETWORK ANALYSIS
   - Identify hub airports
   - Analyze market competition
   - Route profitability analysis
   - Capacity planning

4. 🚨 DISRUPTION MANAGEMENT
   - Reroute during weather
   - Handle airport closures
   - Minimize passenger impact
   - Crew scheduling optimization

5. 💼 CARGO LOGISTICS
   - Optimize freight routes
   - Minimize shipping costs
   - Handle time-sensitive cargo
   - Multi-modal transportation

GRAPH ALGORITHMS USED:
━━━━━━━━━━━━━━━━━━━━━━━

• Dijkstra's Algorithm → Shortest/cheapest/fastest paths
• DFS → Find all possible routes
• Connected Components → Network connectivity
• Centrality Measures → Hub identification
• Network Flow → Capacity optimization
• Minimum Spanning Tree → Network design
"""
    )


def advanced_flight_optimization():
    """
    Advanced optimization techniques
    """
    print("\n🔬 ADVANCED OPTIMIZATION TECHNIQUES")
    print("=" * 40)

    print(
        """
ADVANCED FEATURES:
━━━━━━━━━━━━━━━━━━

1. 🕒 TIME-DEPENDENT ROUTING
   - Consider flight schedules
   - Account for layover times
   - Time zone calculations
   - Day-of-week variations

2. 🎯 MULTI-OBJECTIVE OPTIMIZATION
   - Balance multiple criteria
   - Pareto optimal solutions
   - User preference weights
   - Trade-off analysis

3. 🌐 DYNAMIC ROUTING
   - Real-time price updates
   - Weather-based rerouting
   - Capacity constraints
   - Dynamic pricing models

4. 📊 MACHINE LEARNING INTEGRATION
   - Predict flight delays
   - Price forecasting
   - Demand prediction
   - Route recommendation

5. 🔄 NETWORK OPTIMIZATION
   - Fleet allocation
   - Frequency optimization
   - Seasonal adjustments
   - Competition analysis

IMPLEMENTATION CONSIDERATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Scale: Handle millions of routes
• Speed: Real-time response needed
• Accuracy: Up-to-date information
• Reliability: Handle failures gracefully
• Flexibility: Adapt to changes quickly
"""
    )


def route_comparison_tool():
    """
    Tool to compare different route options
    """
    print("\n🔧 ROUTE COMPARISON TOOL")
    print("=" * 30)

    network = create_example_flight_network()

    def compare_routes(start, destination):
        print(f"\n📋 ROUTE COMPARISON: {start} → {destination}")
        print("-" * 40)

        # Get all three optimization types
        distance_route = network.find_shortest_route_distance(start, destination)
        price_route = network.find_cheapest_route(start, destination)
        time_route = network.find_fastest_route(start, destination)

        routes = [
            ("Shortest Distance", distance_route),
            ("Cheapest Price", price_route),
            ("Fastest Time", time_route),
        ]

        print(f"{'Criteria':<20} {'Route':<25} {'Value':<15}")
        print("-" * 60)

        for criteria, (path, value) in routes:
            if path and value is not None:
                route_str = " → ".join(path)
                if len(route_str) > 22:
                    route_str = route_str[:19] + "..."

                if "Distance" in criteria:
                    value_str = f"{value:.0f} km"
                elif "Price" in criteria:
                    value_str = f"${value:.0f}"
                else:
                    value_str = f"{value:.1f} h"

                print(f"{criteria:<20} {route_str:<25} {value_str:<15}")
            else:
                print(f"{criteria:<20} {'No route found':<25} {'N/A':<15}")

    # Compare routes for different city pairs
    test_routes = [("NYC", "SYD"), ("LHR", "NRT"), ("LAX", "CDG")]

    for start, destination in test_routes:
        compare_routes(start, destination)


if __name__ == "__main__":
    # Main demonstration
    demonstrate_route_optimization()

    # Show applications
    flight_route_applications()

    # Advanced techniques
    advanced_flight_optimization()

    # Route comparison tool
    route_comparison_tool()

    print("\n✅ You now understand flight route optimization with graphs!")
    print("🎯 Next: Explore more real-world graph applications")
    print("💡 Key insight: Different optimization goals require different algorithms!")
