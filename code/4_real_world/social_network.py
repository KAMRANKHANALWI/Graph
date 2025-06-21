"""
Social Network Analysis with Graphs
===================================
Real-world application: Analyze social networks using graph algorithms.
"""

from collections import deque, defaultdict
import random


class SocialNetwork:
    """
    Complete social network implementation using graphs
    """

    def __init__(self):
        self.friendships = {}  # adjacency list of friendships
        self.user_profiles = {}  # store user information

    def add_user(self, username, profile_info=None):
        """Add a new user to the network"""
        if username not in self.friendships:
            self.friendships[username] = []
            self.user_profiles[username] = profile_info or {}
            print(f"✅ Added user: {username}")
            return True
        else:
            print(f"⚠️ User {username} already exists")
            return False

    def add_friendship(self, user1, user2):
        """Create bidirectional friendship between two users"""
        # Ensure both users exist
        self.add_user(user1)
        self.add_user(user2)

        # Add bidirectional friendship
        if user2 not in self.friendships[user1]:
            self.friendships[user1].append(user2)
        if user1 not in self.friendships[user2]:
            self.friendships[user2].append(user1)

        print(f"🤝 {user1} and {user2} are now friends")

    def remove_friendship(self, user1, user2):
        """Remove friendship between two users"""
        if user1 in self.friendships and user2 in self.friendships[user1]:
            self.friendships[user1].remove(user2)
        if user2 in self.friendships and user1 in self.friendships[user2]:
            self.friendships[user2].remove(user1)
        print(f"💔 {user1} and {user2} are no longer friends")

    def get_friends(self, username):
        """Get list of direct friends"""
        return self.friendships.get(username, [])

    def degrees_of_separation(self, user1, user2):
        """
        Find shortest path between two users (BFS)
        Returns the degrees of separation and the path
        """
        if user1 == user2:
            return 0, [user1]

        if user1 not in self.friendships or user2 not in self.friendships:
            return -1, []

        visited = set([user1])
        queue = deque([(user1, [user1], 0)])

        while queue:
            current_user, path, distance = queue.popleft()

            for friend in self.friendships[current_user]:
                if friend == user2:
                    return distance + 1, path + [friend]

                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, path + [friend], distance + 1))

        return -1, []  # Not connected

    def find_mutual_friends(self, user1, user2):
        """Find common friends between two users"""
        friends1 = set(self.friendships.get(user1, []))
        friends2 = set(self.friendships.get(user2, []))
        return list(friends1.intersection(friends2))

    def suggest_friends(self, username, max_suggestions=5):
        """
        Suggest friends based on mutual connections
        Friends of friends who aren't already friends
        """
        if username not in self.friendships:
            return []

        current_friends = set(self.friendships[username])
        suggestions = defaultdict(int)  # potential_friend -> mutual_count

        # Look at friends of friends
        for friend in current_friends:
            for friend_of_friend in self.friendships[friend]:
                if (
                    friend_of_friend != username
                    and friend_of_friend not in current_friends
                ):
                    suggestions[friend_of_friend] += 1

        # Sort by number of mutual friends
        sorted_suggestions = sorted(
            suggestions.items(), key=lambda x: x[1], reverse=True
        )

        return sorted_suggestions[:max_suggestions]

    def find_influencers(self, top_n=5):
        """
        Find most connected users (highest degree centrality)
        """
        user_connections = [
            (user, len(friends)) for user, friends in self.friendships.items()
        ]

        # Sort by number of connections
        sorted_users = sorted(user_connections, key=lambda x: x[1], reverse=True)

        return sorted_users[:top_n]

    def find_friend_groups(self):
        """
        Find all connected components (friend groups)
        """
        visited = set()
        groups = []

        def dfs_group(user, current_group):
            visited.add(user)
            current_group.append(user)

            for friend in self.friendships.get(user, []):
                if friend not in visited:
                    dfs_group(friend, current_group)

        for user in self.friendships:
            if user not in visited:
                group = []
                dfs_group(user, group)
                groups.append(sorted(group))

        return groups

    def calculate_clustering_coefficient(self, username):
        """
        Calculate how tightly connected a user's friends are
        Clustering coefficient = (actual connections between friends) / (possible connections)
        """
        friends = self.friendships.get(username, [])

        if len(friends) < 2:
            return 0.0  # Need at least 2 friends to have clustering

        # Count actual connections between friends
        actual_connections = 0
        for i, friend1 in enumerate(friends):
            for friend2 in friends[i + 1 :]:
                if friend2 in self.friendships.get(friend1, []):
                    actual_connections += 1

        # Calculate possible connections
        possible_connections = len(friends) * (len(friends) - 1) // 2

        return (
            actual_connections / possible_connections
            if possible_connections > 0
            else 0.0
        )

    def find_shortest_path_all_users(self, start_user):
        """
        Find shortest path distances from start_user to all other users
        """
        distances = {start_user: 0}
        queue = deque([start_user])

        while queue:
            current_user = queue.popleft()
            current_distance = distances[current_user]

            for friend in self.friendships.get(current_user, []):
                if friend not in distances:
                    distances[friend] = current_distance + 1
                    queue.append(friend)

        return distances

    def analyze_network(self):
        """
        Comprehensive network analysis
        """
        print("📊 SOCIAL NETWORK ANALYSIS")
        print("=" * 30)

        # Basic statistics
        total_users = len(self.friendships)
        total_friendships = (
            sum(len(friends) for friends in self.friendships.values()) // 2
        )
        avg_friends = total_friendships * 2 / total_users if total_users > 0 else 0

        print(f"👥 Total users: {total_users}")
        print(f"🤝 Total friendships: {total_friendships}")
        print(f"📊 Average friends per user: {avg_friends:.1f}")

        # Find friend groups
        groups = self.find_friend_groups()
        print(f"🏘️ Friend groups: {len(groups)}")

        if len(groups) > 1:
            group_sizes = [len(group) for group in groups]
            print(f"   Group sizes: {sorted(group_sizes, reverse=True)}")
            print(f"   Largest group: {max(group_sizes)} users")
        else:
            print("   All users are connected!")

        # Find influencers
        influencers = self.find_influencers(3)
        print(f"🌟 Top influencers:")
        for i, (user, connections) in enumerate(influencers, 1):
            print(f"   {i}. {user} ({connections} friends)")

        # Network connectivity
        if total_users > 0:
            # Check if network is connected
            is_connected = len(groups) == 1
            print(f"🔗 Network connected: {is_connected}")

            if is_connected and total_users > 1:
                # Calculate average path length
                total_path_length = 0
                total_pairs = 0

                for user in list(self.friendships.keys())[
                    :5
                ]:  # Sample to avoid long computation
                    distances = self.find_shortest_path_all_users(user)
                    for other_user, distance in distances.items():
                        if other_user != user:
                            total_path_length += distance
                            total_pairs += 1

                if total_pairs > 0:
                    avg_path_length = total_path_length / total_pairs
                    print(f"📏 Average path length: {avg_path_length:.2f}")


def create_example_social_network():
    """
    Create a realistic social network example
    """
    print("🏗️ CREATING EXAMPLE SOCIAL NETWORK")
    print("=" * 38)

    network = SocialNetwork()

    # Add users with profiles
    users = [
        ("Kamran", {"age": 25, "location": "Karachi", "interests": ["tech", "gaming"]}),
        ("Asad", {"age": 24, "location": "Lahore", "interests": ["sports", "music"]}),
        (
            "Shabab",
            {
                "age": 26,
                "location": "Islamabad",
                "interests": ["travel", "photography"],
            },
        ),
        ("Saad", {"age": 23, "location": "Karachi", "interests": ["tech", "movies"]}),
        ("Shadman", {"age": 27, "location": "Lahore", "interests": ["music", "art"]}),
        (
            "Zeeshan",
            {"age": 25, "location": "Islamabad", "interests": ["sports", "travel"]},
        ),
        ("Ali", {"age": 24, "location": "Karachi", "interests": ["gaming", "tech"]}),
        (
            "Ahmed",
            {"age": 26, "location": "Lahore", "interests": ["photography", "art"]},
        ),
    ]

    for username, profile in users:
        network.add_user(username, profile)

    # Create friendships based on your original example + some extras
    friendships = [
        ("Kamran", "Asad"),  # Original friendships
        ("Kamran", "Shabab"),
        ("Kamran", "Saad"),
        ("Asad", "Shadman"),
        ("Shabab", "Zeeshan"),
        ("Saad", "Zeeshan"),
        ("Shadman", "Ali"),  # Extended network
        ("Zeeshan", "Ahmed"),
        ("Ali", "Ahmed"),
        ("Saad", "Ali"),  # Creates more connections
    ]

    print("\nAdding friendships:")
    for user1, user2 in friendships:
        network.add_friendship(user1, user2)

    return network


def demonstrate_social_network_analysis():
    """
    Demonstrate various social network analysis features
    """
    network = create_example_social_network()

    print("\n" + "=" * 50)

    # Network analysis
    network.analyze_network()

    print("\n" + "=" * 50)
    print("🔍 DETAILED ANALYSIS EXAMPLES")
    print("=" * 30)

    # Degrees of separation
    user1, user2 = "Kamran", "Ahmed"
    degrees, path = network.degrees_of_separation(user1, user2)
    print(f"\n🎯 Connection between {user1} and {user2}:")
    if degrees != -1:
        print(f"   Degrees of separation: {degrees}")
        print(f"   Connection path: {' → '.join(path)}")
    else:
        print(f"   Not connected!")

    # Mutual friends
    print(f"\n👥 Mutual friends between Kamran and Asad:")
    mutual = network.find_mutual_friends("Kamran", "Asad")
    print(f"   {mutual if mutual else 'No mutual friends'}")

    # Friend suggestions
    print(f"\n💡 Friend suggestions for Shadman:")
    suggestions = network.suggest_friends("Shadman", 3)
    for suggested_friend, mutual_count in suggestions:
        print(f"   {suggested_friend} ({mutual_count} mutual friends)")

    # Clustering coefficient
    print(f"\n🕸️ How tightly connected are each user's friends?")
    for user in ["Kamran", "Saad", "Zeeshan"]:
        coefficient = network.calculate_clustering_coefficient(user)
        print(f"   {user}: {coefficient:.2f} (0=scattered, 1=fully connected)")

    # Friend groups
    print(f"\n🏘️ Friend groups in the network:")
    groups = network.find_friend_groups()
    for i, group in enumerate(groups, 1):
        print(f"   Group {i}: {group}")


def simulate_viral_spread():
    """
    Simulate how information spreads through social network (BFS)
    """
    print("\n🦠 VIRAL INFORMATION SPREAD SIMULATION")
    print("=" * 40)

    network = create_example_social_network()

    # Simulate information spreading from Kamran
    start_user = "Kamran"

    print(f"📱 {start_user} posts something interesting...")
    print("Let's see how it spreads through the network!")

    informed = set([start_user])
    queue = deque([(start_user, 0)])  # (user, time_step)
    spread_timeline = []

    while queue:
        current_user, time_step = queue.popleft()
        spread_timeline.append((time_step, current_user))

        # Inform friends (with some probability)
        for friend in network.get_friends(current_user):
            if friend not in informed:
                # Simulate probability of sharing (70% chance)
                if random.random() < 0.7:
                    informed.add(friend)
                    queue.append((friend, time_step + 1))

    print(f"\n📊 Information spread timeline:")
    current_time = -1
    for time_step, user in spread_timeline:
        if time_step != current_time:
            current_time = time_step
            print(f"\n   Time {time_step}:")
        print(f"     {user} sees the post")

    print(f"\n🎯 Spread statistics:")
    print(f"   Total reached: {len(informed)} out of {len(network.friendships)} users")
    print(f"   Reach percentage: {len(informed)/len(network.friendships)*100:.1f}%")
    print(f"   Max time steps: {max(time for time, _ in spread_timeline)}")


def social_network_applications():
    """
    Show various applications of social network analysis
    """
    print("\n🚀 SOCIAL NETWORK APPLICATIONS")
    print("=" * 35)

    print(
        """
REAL-WORLD APPLICATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━

1. 👥 FRIEND RECOMMENDATIONS
   - Find friends of friends
   - Calculate mutual connections
   - Suggest based on interests/location

2. 🎯 TARGETED ADVERTISING  
   - Find influential users
   - Identify interest clusters
   - Optimize ad placement

3. 🔍 FRAUD DETECTION
   - Detect suspicious connection patterns
   - Find fake account clusters
   - Analyze abnormal behavior spread

4. 📊 MARKET RESEARCH
   - Understand information flow
   - Identify opinion leaders
   - Track trend propagation

5. 🌐 NETWORK OPTIMIZATION
   - Improve platform performance
   - Identify connection bottlenecks
   - Optimize content delivery

6. 🔒 PRIVACY & SECURITY
   - Detect spam networks
   - Find coordinated inauthentic behavior
   - Protect user privacy

GRAPH ALGORITHMS USED:
━━━━━━━━━━━━━━━━━━━━━━━

• BFS → Shortest connection paths
• DFS → Friend group detection  
• Centrality → Influence measurement
• Clustering → Community detection
• PageRank → Authority/reputation
• Community Detection → Interest groups
"""
    )


def advanced_social_network_features():
    """
    Advanced features for social network analysis
    """
    print("\n🔬 ADVANCED FEATURES")
    print("=" * 25)

    print(
        """
ADVANCED METRICS:
━━━━━━━━━━━━━━━━━

1. 📊 CENTRALITY MEASURES
   - Degree centrality (connections)
   - Betweenness centrality (bridge users)
   - Closeness centrality (reach efficiency)
   - Eigenvector centrality (connected to important users)

2. 🏘️ COMMUNITY DETECTION  
   - Modularity optimization
   - Louvain algorithm
   - Label propagation
   - Spectral clustering

3. 🔗 LINK PREDICTION
   - Predict future friendships
   - Common neighbors score
   - Adamic-Adar index
   - Jaccard coefficient

4. 📈 NETWORK EVOLUTION
   - Track network growth
   - Identify connection patterns
   - Predict network changes
   - Analyze user behavior over time

5. 🎯 INFLUENCE ANALYSIS
   - Measure information spread
   - Identify key influencers
   - Model viral processes
   - Optimize marketing strategies
"""
    )


if __name__ == "__main__":
    # Main demonstration
    demonstrate_social_network_analysis()

    # Viral spread simulation
    simulate_viral_spread()

    # Show applications
    social_network_applications()

    # Advanced features
    advanced_social_network_features()

    print("\n✅ You now understand social network analysis with graphs!")
    print("🎯 Next: Explore other real-world applications")
    print(
        "💡 Key insight: Graphs are perfect for modeling relationships and connections!"
    )
