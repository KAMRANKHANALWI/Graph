"""
Minimum Spanning Tree
====================================
Learn how to connect all points with minimum cost!
"""


def kruskals_algorithm_simple(edges, vertices):
    """
    Simple Kruskal's algorithm to find minimum spanning tree
    """
    print("🌳 KRUSKAL'S ALGORITHM: Finding Minimum Spanning Tree")
    print("=" * 55)

    # Step 1: Sort edges by weight (cheapest first)
    edges.sort(key=lambda x: x[2])
    print("Step 1: Sort edges by cost")
    for i, (u, v, weight) in enumerate(edges):
        print(f"  {i+1}. {u} ↔ {v}: cost {weight}")

    # Step 2: Initialize Union-Find (to detect cycles)
    parent = {v: v for v in vertices}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False

    # Step 3: Pick edges one by one (if they don't create cycle)
    mst_edges = []
    total_cost = 0

    print(f"\nStep 2: Pick edges (avoid cycles)")

    for u, v, weight in edges:
        if union(u, v):
            mst_edges.append((u, v, weight))
            total_cost += weight
            print(f"  ✅ Added: {u} ↔ {v} (cost: {weight}) - Total: {total_cost}")

            # Stop when we have enough edges for a tree
            if len(mst_edges) == len(vertices) - 1:
                break
        else:
            print(f"  ❌ Skipped: {u} ↔ {v} (would create cycle)")

    print(f"\n🎉 Minimum Spanning Tree found!")
    print(f"   Total cost: {total_cost}")
    print(f"   Edges: {mst_edges}")

    return mst_edges, total_cost


def prims_algorithm_simple(graph, start_vertex):
    """
    Prim's algorithm - grows the tree from one vertex
    """
    print(f"🌱 PRIM'S ALGORITHM: Growing tree from {start_vertex}")
    print("=" * 50)

    # Start with one vertex
    in_tree = {start_vertex}
    mst_edges = []
    total_cost = 0

    vertices = set(graph.keys())

    step = 1
    while len(in_tree) < len(vertices):
        print(f"\nStep {step}: Tree has {list(in_tree)}")

        # Find cheapest edge from tree to outside
        min_edge = None
        min_cost = float("inf")

        for vertex in in_tree:
            for neighbor, cost in graph.get(vertex, []):
                if neighbor not in in_tree and cost < min_cost:
                    min_cost = cost
                    min_edge = (vertex, neighbor, cost)

        if min_edge:
            u, v, cost = min_edge
            in_tree.add(v)
            mst_edges.append(min_edge)
            total_cost += cost
            print(f"  ✅ Added: {u} ↔ {v} (cost: {cost}) - Total: {total_cost}")

        step += 1

    print(f"\n🎉 Minimum Spanning Tree found!")
    print(f"   Total cost: {total_cost}")
    print(f"   Edges: {mst_edges}")

    return mst_edges, total_cost


def simple_network_example():
    """
    Simple example: Connecting cities with minimum cable cost
    """
    print("🏙️ EXAMPLE: Connecting Cities with Cables")
    print("=" * 40)

    # Cities and connection costs
    cities = ["A", "B", "C", "D", "E"]

    # Edges: (city1, city2, cost_in_thousands)
    cable_costs = [
        ("A", "B", 10),  # A to B costs $10k
        ("A", "C", 15),  # A to C costs $15k
        ("A", "D", 20),  # A to D costs $20k
        ("B", "C", 12),  # B to C costs $12k
        ("B", "E", 25),  # B to E costs $25k
        ("C", "D", 8),  # C to D costs $8k
        ("C", "E", 18),  # C to E costs $18k
        ("D", "E", 14),  # D to E costs $14k
    ]

    print("Connection costs (in $1000s):")
    for city1, city2, cost in cable_costs:
        print(f"  {city1} ↔ {city2}: ${cost}k")

    print(f"\n🤔 Problem: Connect all {len(cities)} cities with minimum cost")
    print(f"   Need exactly {len(cities)-1} cables (for a tree)")

    # Solve with Kruskal's
    mst_edges, total_cost = kruskals_algorithm_simple(cable_costs.copy(), cities)

    print(f"\n💰 Solution: Total cost ${total_cost}k")
    print(f"   This is the cheapest way to connect all cities!")


def compare_algorithms():
    """
    Compare Kruskal's vs Prim's on the same problem
    """
    print("\n🆚 COMPARING KRUSKAL'S VS PRIM'S")
    print("=" * 35)

    # Convert edge list to adjacency list for Prim's
    graph = {
        "A": [("B", 10), ("C", 15), ("D", 20)],
        "B": [("A", 10), ("C", 12), ("E", 25)],
        "C": [("A", 15), ("B", 12), ("D", 8), ("E", 18)],
        "D": [("A", 20), ("C", 8), ("E", 14)],
        "E": [("B", 25), ("C", 18), ("D", 14)],
    }

    edges = [
        ("A", "B", 10),
        ("A", "C", 15),
        ("A", "D", 20),
        ("B", "C", 12),
        ("B", "E", 25),
        ("C", "D", 8),
        ("C", "E", 18),
        ("D", "E", 14),
    ]

    print("1️⃣ Kruskal's approach (sort all edges first):")
    kruskal_edges, kruskal_cost = kruskals_algorithm_simple(
        edges.copy(), ["A", "B", "C", "D", "E"]
    )

    print(f"\n{'-'*50}")

    print("2️⃣ Prim's approach (grow tree from one vertex):")
    prim_edges, prim_cost = prims_algorithm_simple(graph, "A")

    print(f"\n📊 Results:")
    print(f"   Both found the same minimum cost: ${kruskal_cost}k")
    print(f"   Both algorithms guarantee optimal solution!")


def real_world_applications():
    """
    Show where MST is used in real life
    """
    print("\n🌍 REAL-WORLD APPLICATIONS")
    print("=" * 30)

    print(
        """
🔧 WHERE MST IS USED:

1. 🌐 NETWORK DESIGN
   • Internet backbone connections
   • Telephone network layout  
   • Cable TV distribution
   • Computer network topology

2. 🛣️ TRANSPORTATION
   • Road network planning
   • Railway system design
   • Pipeline layout (oil, gas)
   • Delivery route optimization

3. 🔌 UTILITIES
   • Electrical grid design
   • Water distribution systems
   • Fiber optic cable layout
   • Power line connections

4. 💻 COMPUTER SCIENCE
   • Cluster analysis
   • Image segmentation
   • Approximation algorithms
   • Network broadcasting

5. 🏗️ CONSTRUCTION
   • Building wiring layout
   • Plumbing system design
   • HVAC duct networks
   • Bridge construction planning

💡 THE GOAL IS ALWAYS THE SAME:
• Connect all points
• Use minimum total cost/distance
• Create a tree (no cycles)
• Ensure everything is reachable
"""
    )


def which_algorithm_to_use():
    """
    Simple guide on when to use Kruskal's vs Prim's
    """
    print("\n🤔 KRUSKAL'S VS PRIM'S: WHICH TO USE?")
    print("=" * 40)

    print(
        """
🏃 KRUSKAL'S ALGORITHM:

✅ GOOD WHEN:
• You have a list of all edges
• Graph is sparse (few edges)
• You want to understand step-by-step
• Sorting edges is easy

📊 HOW IT WORKS:
• Sort all edges by weight
• Pick cheapest edges (avoid cycles)
• Uses Union-Find for cycle detection

🌱 PRIM'S ALGORITHM:

✅ GOOD WHEN:
• Graph is dense (many edges)  
• You have adjacency list representation
• You want to grow tree gradually
• Memory usage is important

📊 HOW IT WORKS:
• Start with one vertex
• Always add cheapest edge to tree
• Grows tree one vertex at a time

⚖️ COMPARISON:

                Kruskal's    Prim's
Time:           O(E log E)   O(E log V)
Space:          O(V)         O(V)
Best for:       Sparse       Dense
Edge format:    Edge list    Adjacency list
Growth:         Edge-based   Vertex-based

BOTH GIVE THE SAME OPTIMAL ANSWER!
"""
    )


def simple_mst_problems():
    """
    Practice problems for beginners
    """
    print("\n📝 PRACTICE PROBLEMS")
    print("=" * 20)

    print(
        """
🧠 TRY THESE YOURSELF:

Problem 1: Small Network
Connect 4 computers with these cable costs:
• A-B: $5    • A-C: $8    • A-D: $12
• B-C: $6    • B-D: $15   • C-D: $7

What's the minimum cost to connect all?
Answer: $18 (edges: A-B:5, B-C:6, C-D:7)

Problem 2: Office Layout  
Connect 5 departments with minimum wire:
• HR-IT: 10m     • HR-Sales: 15m   • HR-Finance: 20m
• IT-Sales: 12m  • IT-Finance: 25m • Sales-Finance: 8m
• Sales-Marketing: 18m  • Finance-Marketing: 14m

What's the minimum total wire needed?
Try solving with both Kruskal's and Prim's!

Problem 3: City Planning
You're planning roads between 6 towns.
Each road has a construction cost.
Find the minimum cost to connect all towns
so everyone can reach everyone else.

💡 SOLVING TIPS:
1. List all possible connections
2. Sort by cost (for Kruskal's)
3. Pick cheapest without creating cycles
4. Stop when you have n-1 edges (for n vertices)
"""
    )


if __name__ == "__main__":
    # Simple example
    simple_network_example()

    # Compare algorithms
    compare_algorithms()

    # Real-world applications
    real_world_applications()

    # Algorithm comparison guide
    which_algorithm_to_use()

    # Practice problems
    simple_mst_problems()

    print("\n✅ You now understand Minimum Spanning Trees!")
    print("🎯 Key insight: MST finds the cheapest way to connect everything!")
