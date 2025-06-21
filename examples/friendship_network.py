"""
Friendship Network Example
==========================
Your original friendship network example made simple and interactive.
"""

from collections import deque


def create_friendship_network():
    """
    Create the friendship network from your original example
    """
    friends = {
        "Kamran": ["Asad", "Shabab", "Saad"],
        "Asad": ["Kamran", "Shadman"],
        "Shabab": ["Kamran", "Zeeshan"],
        "Saad": ["Kamran", "Zeeshan"],
        "Shadman": ["Asad"],
        "Zeeshan": ["Shabab", "Saad"],
    }
    return friends


def show_network(friends):
    """
    Display the friendship network clearly
    """
    print("👥 FRIENDSHIP NETWORK")
    print("=" * 25)

    print("Friendships:")
    for person, friend_list in friends.items():
        print(f"  {person}: {friend_list}")

    # Count total friendships
    total_friendships = sum(len(friend_list) for friend_list in friends.values()) // 2
    print(f"\nTotal people: {len(friends)}")
    print(f"Total friendships: {total_friendships}")


def find_connection_path(friends, person1, person2):
    """
    Find how two people are connected through friends
    """
    print(f"\n🔍 Finding connection: {person1} ↔ {person2}")

    if person1 == person2:
        print(f"  Same person!")
        return [person1]

    # BFS to find shortest path
    visited = set([person1])
    queue = deque([(person1, [person1])])

    while queue:
        current_person, path = queue.popleft()

        # Check all friends of current person
        for friend in friends.get(current_person, []):
            if friend == person2:
                final_path = path + [friend]
                print(f"  ✅ Connection found: {' → '.join(final_path)}")
                print(f"  Degrees of separation: {len(final_path) - 1}")
                return final_path

            if friend not in visited:
                visited.add(friend)
                queue.append((friend, path + [friend]))

    print(f"  ❌ No connection found")
    return None


def find_mutual_friends(friends, person1, person2):
    """
    Find friends that two people have in common
    """
    print(f"\n👥 Finding mutual friends: {person1} & {person2}")

    friends1 = set(friends.get(person1, []))
    friends2 = set(friends.get(person2, []))

    mutual = friends1.intersection(friends2)

    if mutual:
        print(f"  ✅ Mutual friends: {list(mutual)}")
    else:
        print(f"  ❌ No mutual friends")

    return list(mutual)


def suggest_new_friends(friends, person):
    """
    Suggest new friends based on friends of friends
    """
    print(f"\n💡 Friend suggestions for {person}:")

    current_friends = set(friends.get(person, []))
    suggestions = set()

    # Look at friends of friends
    for friend in current_friends:
        for friend_of_friend in friends.get(friend, []):
            if friend_of_friend != person and friend_of_friend not in current_friends:
                suggestions.add(friend_of_friend)

    if suggestions:
        print(f"  Suggested friends: {list(suggestions)}")
        for suggestion in suggestions:
            # Show through whom they're connected
            for friend in current_friends:
                if suggestion in friends.get(friend, []):
                    print(f"    {suggestion} (through {friend})")
                    break
    else:
        print(f"  No suggestions found")

    return list(suggestions)


def analyze_network_structure(friends):
    """
    Analyze the structure of the friendship network
    """
    print(f"\n📊 NETWORK ANALYSIS")
    print("=" * 20)

    # Find most connected person
    connections = [
        (person, len(friend_list)) for person, friend_list in friends.items()
    ]
    connections.sort(key=lambda x: x[1], reverse=True)

    print(f"Most connected people:")
    for i, (person, count) in enumerate(connections[:3], 1):
        print(f"  {i}. {person}: {count} friends")

    # Check if everyone is connected
    def is_network_connected():
        visited = set()
        start_person = next(iter(friends))
        queue = deque([start_person])
        visited.add(start_person)

        while queue:
            current = queue.popleft()
            for friend in friends.get(current, []):
                if friend not in visited:
                    visited.add(friend)
                    queue.append(friend)

        return len(visited) == len(friends)

    if is_network_connected():
        print(f"\n✅ Network is connected: Everyone can reach everyone!")
    else:
        print(f"\n❌ Network is disconnected: Some people are isolated")


def interactive_exploration(friends):
    """
    Let users explore the network interactively
    """
    print(f"\n🎮 INTERACTIVE EXPLORATION")
    print("=" * 30)

    people = list(friends.keys())

    # Test all possible connections
    print("Testing all possible connections:")

    for i, person1 in enumerate(people):
        for person2 in people[i + 1 :]:
            find_connection_path(friends, person1, person2)

    # Test mutual friends
    print(f"\n" + "=" * 40)
    print("Testing mutual friends:")

    test_pairs = [("Kamran", "Asad"), ("Asad", "Zeeshan"), ("Shabab", "Saad")]
    for person1, person2 in test_pairs:
        find_mutual_friends(friends, person1, person2)

    # Test friend suggestions
    print(f"\n" + "=" * 40)
    print("Testing friend suggestions:")

    for person in ["Shadman", "Zeeshan", "Asad"]:
        suggest_new_friends(friends, person)


def simulate_adding_friendship(friends, person1, person2):
    """
    Show what happens when we add a new friendship
    """
    print(f"\n➕ ADDING NEW FRIENDSHIP: {person1} ↔ {person2}")
    print("=" * 45)

    # Check if they're already friends
    if person2 in friends.get(person1, []):
        print(f"  ⚠️ {person1} and {person2} are already friends!")
        return friends

    # Add the friendship (bidirectional)
    if person1 not in friends:
        friends[person1] = []
    if person2 not in friends:
        friends[person2] = []

    friends[person1].append(person2)
    friends[person2].append(person1)

    print(f"  ✅ Added friendship between {person1} and {person2}")

    # Show impact
    print(f"  Impact:")
    print(f"    {person1} now has {len(friends[person1])} friends")
    print(f"    {person2} now has {len(friends[person2])} friends")

    return friends


def demonstrate_graph_concepts():
    """
    Use the friendship network to explain graph concepts
    """
    print(f"\n🎓 GRAPH CONCEPTS EXPLAINED")
    print("=" * 30)

    friends = create_friendship_network()

    print(
        """
GRAPH TERMINOLOGY:
• Vertices/Nodes: People (Kamran, Asad, etc.)
• Edges: Friendships (connections between people)
• Undirected: Friendship goes both ways
• Degree: Number of friends a person has
• Path: Chain of friendships connecting two people
• Connected: Everyone can reach everyone through friends

REAL EXAMPLES:
"""
    )

    # Show examples
    print(f"• Vertex: Kamran")
    print(f"• Edges from Kamran: {friends['Kamran']}")
    print(f"• Degree of Kamran: {len(friends['Kamran'])}")

    path = find_connection_path(friends, "Shadman", "Zeeshan")
    if path:
        print(f"• Path from Shadman to Zeeshan: {' → '.join(path)}")


def main():
    """
    Main demonstration of the friendship network
    """
    print("🌟 FRIENDSHIP NETWORK EXPLORATION")
    print("=" * 40)

    # Create and show the network
    friends = create_friendship_network()
    show_network(friends)

    # Analyze the network
    analyze_network_structure(friends)

    # Interactive exploration
    interactive_exploration(friends)

    # Show graph concepts
    demonstrate_graph_concepts()

    # Try adding a new friendship
    print(f"\n" + "=" * 50)
    friends_updated = simulate_adding_friendship(friends.copy(), "Shadman", "Zeeshan")

    print(f"\nAfter adding Shadman ↔ Zeeshan:")
    find_connection_path(friends_updated, "Shadman", "Saad")


if __name__ == "__main__":
    main()

    print("\n✅ You explored your friendship network with graphs!")
    print("🎯 This shows how graphs help analyze real relationships!")
