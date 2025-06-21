"""
Topological Sort - Simple Guide
===============================
Learn how to order tasks when some must come before others.
"""

from collections import deque, defaultdict


def topological_sort_simple(graph):
    """
    Simple topological sort using Kahn's algorithm
    Perfect for beginners to understand!
    """
    print("📋 TOPOLOGICAL SORT: Finding correct order")
    print("=" * 45)

    # Step 1: Count incoming edges for each node
    in_degree = defaultdict(int)

    # Initialize all nodes with 0 incoming edges
    for node in graph:
        in_degree[node] = 0

    # Count actual incoming edges
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    print("Step 1: Count dependencies")
    for node, count in in_degree.items():
        print(f"  {node}: {count} dependencies")

    # Step 2: Find nodes with no dependencies (can start immediately)
    queue = deque()
    for node, count in in_degree.items():
        if count == 0:
            queue.append(node)

    print(f"\nStep 2: Nodes that can start now: {list(queue)}")

    # Step 3: Process nodes one by one
    result = []
    step = 3

    while queue:
        current = queue.popleft()
        result.append(current)

        print(f"\nStep {step}: Process {current}")

        # Remove this node's outgoing edges
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            print(f"  {neighbor} now has {in_degree[neighbor]} dependencies")

            # If neighbor has no more dependencies, add it to queue
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                print(f"  ✅ {neighbor} is ready!")

        step += 1

    # Check if we processed all nodes (no cycles)
    if len(result) == len(graph):
        print(f"\n🎉 Success! Correct order: {result}")
        return result
    else:
        print(f"\n❌ Error! Graph has cycles - impossible to sort")
        return None


def course_prerequisites_example():
    """
    Real example: College course prerequisites
    """
    print("🎓 EXAMPLE: College Course Prerequisites")
    print("=" * 40)

    # Course dependencies (course -> list of courses that depend on it)
    courses = {
        "Math101": ["Math201", "Physics101"],
        "Math201": ["Math301", "Stats201"],
        "Math301": ["AdvancedMath"],
        "Physics101": ["Physics201"],
        "Physics201": ["AdvancedPhysics"],
        "Stats201": ["DataScience"],
        "English101": ["English201"],
        "English201": ["Literature"],
        "AdvancedMath": [],
        "AdvancedPhysics": [],
        "DataScience": [],
        "Literature": [],
    }

    print("Course dependencies:")
    for course, depends_on in courses.items():
        if depends_on:
            print(f"  {course} is needed for: {depends_on}")
        else:
            print(f"  {course} is a final course")

    print(f"\n🤔 Question: What order should you take these courses?")
    order = topological_sort_simple(courses)

    if order:
        print(f"\n📚 Recommended course order:")
        for i, course in enumerate(order, 1):
            print(f"  {i}. {course}")


def project_tasks_example():
    """
    Simple example: Project task dependencies
    """
    print("\n🏗️ EXAMPLE: Building a House (Task Dependencies)")
    print("=" * 50)

    # Task dependencies
    tasks = {
        "Foundation": ["Walls", "Plumbing"],
        "Walls": ["Roof", "Electrical"],
        "Roof": ["Painting"],
        "Plumbing": ["Testing"],
        "Electrical": ["Painting", "Testing"],
        "Painting": ["Cleanup"],
        "Testing": ["Cleanup"],
        "Cleanup": [],
    }

    print("Task dependencies:")
    for task, next_tasks in tasks.items():
        if next_tasks:
            print(f"  After {task}: can do {next_tasks}")
        else:
            print(f"  {task}: final task")

    print(f"\n🤔 Question: What order should we do these tasks?")
    order = topological_sort_simple(tasks)

    if order:
        print(f"\n🔨 Recommended task order:")
        for i, task in enumerate(order, 1):
            print(f"  Day {i}: {task}")


def detect_impossible_ordering():
    """
    Show what happens when there's a cycle (impossible to order)
    """
    print("\n❌ EXAMPLE: Impossible Ordering (Circular Dependencies)")
    print("=" * 55)

    # This has a cycle: A needs B, B needs C, C needs A!
    impossible_tasks = {
        "TaskA": ["TaskB"],  # A depends on B
        "TaskB": ["TaskC"],  # B depends on C
        "TaskC": ["TaskA"],  # C depends on A (creates cycle!)
    }

    print("Circular dependencies:")
    print("  TaskA needs TaskB to be done first")
    print("  TaskB needs TaskC to be done first")
    print("  TaskC needs TaskA to be done first")
    print("  🔄 This creates an impossible situation!")

    result = topological_sort_simple(impossible_tasks)

    if not result:
        print("\n💡 This is why we check for cycles!")
        print("   In real life: circular dependencies break systems")


def simple_dfs_topological_sort(graph):
    """
    Alternative method using DFS (depth-first search)
    Simpler to understand for some people
    """
    print("\n🔄 ALTERNATIVE METHOD: DFS Topological Sort")
    print("=" * 45)

    visited = set()
    result = []

    def dfs(node):
        visited.add(node)
        print(f"  Visiting: {node}")

        # Visit all nodes that depend on this one
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)

        # Add to result AFTER visiting dependencies
        result.append(node)
        print(f"  ✅ Finished: {node}")

    # Start DFS from each unvisited node
    for node in graph:
        if node not in visited:
            print(f"\nStarting from: {node}")
            dfs(node)

    # Reverse the result (because we added nodes after visiting their dependencies)
    result.reverse()
    print(f"\nDFS Result: {result}")
    return result


def when_to_use_topological_sort():
    """
    Simple guide on when this is useful
    """
    print("\n🎯 WHEN TO USE TOPOLOGICAL SORT")
    print("=" * 35)

    print(
        """
🔧 REAL-WORLD USES:

1. 📚 COURSE SCHEDULING
   • Plan study order
   • University curricula
   • Training programs
   • Skill development paths

2. 🏗️ PROJECT MANAGEMENT
   • Task dependencies
   • Build systems
   • Manufacturing processes
   • Construction planning

3. 💻 SOFTWARE DEVELOPMENT
   • Compile order
   • Package dependencies
   • Library loading
   • Feature rollouts

4. 📦 PACKAGE MANAGERS
   • npm, pip, apt-get
   • Install dependencies first
   • Avoid circular dependencies
   • Update order

5. 🎯 GOAL PLANNING
   • Personal development
   • Career planning
   • Learning roadmaps
   • Achievement unlocking

✅ USE WHEN YOU HAVE:
• Tasks with dependencies
• "Must do X before Y" relationships  
• Need to find valid ordering
• Want to detect circular dependencies

❌ DON'T USE WHEN:
• No dependencies between tasks
• All tasks can be done in parallel
• Order doesn't matter
• Working with undirected graphs
"""
    )


def comparison_of_methods():
    """
    Compare the two topological sort methods
    """
    print("\n🆚 COMPARING TOPOLOGICAL SORT METHODS")
    print("=" * 45)

    print(
        """
📊 METHOD COMPARISON:

1. 🏃 KAHN'S ALGORITHM (BFS-based):
   ✅ Easy to understand step-by-step
   ✅ Clearly shows dependencies being resolved
   ✅ Detects cycles easily
   ✅ Good for explaining to beginners
   
2. 🔄 DFS-BASED:
   ✅ More concise code
   ✅ Uses recursion naturally
   ✅ Good for programmers
   ❌ Harder to trace by hand

BOTH METHODS:
• Same time complexity: O(V + E)
• Same space complexity: O(V)
• Both detect cycles
• Both produce valid orderings

🎯 CHOOSE BASED ON:
• Kahn's: Better for learning/teaching
• DFS: Better for implementation
"""
    )


def quick_reference():
    """
    Quick reference for topological sort
    """
    print("\n📖 QUICK REFERENCE")
    print("=" * 20)

    print(
        """
🔥 TOPOLOGICAL SORT CHEAT SHEET:

WHAT IT DOES:
• Orders tasks with dependencies
• Ensures prerequisites come first
• Detects impossible situations (cycles)

SIMPLE STEPS:
1. Count dependencies for each task
2. Start with tasks that have no dependencies
3. Remove completed tasks from dependency counts
4. Repeat until all tasks done

KAHN'S ALGORITHM:
```python
def topological_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    queue = [node for node, degree in in_degree.items() if degree == 0]
    result = []
    
    while queue:
        current = queue.pop(0)
        result.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == len(graph) else None
```

TIME COMPLEXITY: O(V + E)
SPACE COMPLEXITY: O(V)
"""
    )


if __name__ == "__main__":
    print("🎯 TOPOLOGICAL SORT DEMONSTRATION")
    print("=" * 40)

    # Course prerequisites example
    course_prerequisites_example()

    # Project tasks example
    project_tasks_example()

    # Show impossible case
    detect_impossible_ordering()

    # DFS alternative
    print("\n" + "=" * 60)
    simple_tasks = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    print("Testing DFS method with simple graph:", simple_tasks)
    simple_dfs_topological_sort(simple_tasks)

    # Educational content
    print("\n" + "=" * 60)
    when_to_use_topological_sort()

    print("\n" + "=" * 60)
    comparison_of_methods()

    print("\n" + "=" * 60)
    quick_reference()

    print("\n🎉 TOPOLOGICAL SORT COMPLETE!")
    print("🎯 Key Takeaway: Perfect for ordering tasks with dependencies!")
    print("💡 Remember: If there's a cycle, ordering is impossible!")
