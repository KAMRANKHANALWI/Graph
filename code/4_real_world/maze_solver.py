"""
Maze Solver using Graph Algorithms
==================================
Real-world application: Solve mazes using BFS and DFS algorithms.
"""

from collections import deque
import random

class MazeSolver:
    """
    Maze representation and solving using graph algorithms
    """
    
    def __init__(self, maze_grid):
        """
        Initialize maze from 2D grid
        '.' = empty space, '#' = wall, 'S' = start, 'E' = end
        """
        self.grid = maze_grid
        self.rows = len(maze_grid)
        self.cols = len(maze_grid[0]) if maze_grid else 0
        self.start = None
        self.end = None
        self.graph = {}
        
        # Find start and end positions
        for r in range(self.rows):
            for c in range(self.cols):
                if maze_grid[r][c] == 'S':
                    self.start = (r, c)
                elif maze_grid[r][c] == 'E':
                    self.end = (r, c)
        
        # Convert maze to graph
        self._build_graph()
    
    def _build_graph(self):
        """Convert 2D maze grid to graph representation"""
        print("🏗️ Converting maze to graph...")
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != '#':  # Not a wall
                    current_pos = (r, c)
                    self.graph[current_pos] = []
                    
                    # Check all 4 directions
                    for dr, dc in directions:
                        new_r, new_c = r + dr, c + dc
                        
                        # Check bounds and if it's not a wall
                        if (0 <= new_r < self.rows and 
                            0 <= new_c < self.cols and 
                            self.grid[new_r][new_c] != '#'):
                            
                            neighbor_pos = (new_r, new_c)
                            self.graph[current_pos].append(neighbor_pos)
        
        print(f"✅ Graph built: {len(self.graph)} nodes, {sum(len(neighbors) for neighbors in self.graph.values())//2} edges")
    
    def solve_bfs(self):
        """
        Solve maze using BFS (guarantees shortest path)
        """
        print("🌊 SOLVING MAZE WITH BFS (Shortest Path)")
        print("=" * 45)
        
        if not self.start or not self.end:
            print("❌ Start or end position not found!")
            return None, None
        
        visited = set([self.start])
        queue = deque([(self.start, [self.start])])
        nodes_explored = 0
        
        while queue:
            current_pos, path = queue.popleft()
            nodes_explored += 1
            
            print(f"  Step {nodes_explored}: Exploring {current_pos}")
            
            if current_pos == self.end:
                print(f"🎉 SOLUTION FOUND!")
                print(f"   Path length: {len(path)} steps")
                print(f"   Nodes explored: {nodes_explored}")
                return path, nodes_explored
            
            # Explore neighbors
            for neighbor in self.graph.get(current_pos, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        print("❌ No solution found!")
        return None, nodes_explored
    
    def solve_dfs(self):
        """
        Solve maze using DFS (finds any path, not necessarily shortest)
        """
        print("🕳️ SOLVING MAZE WITH DFS (Any Path)")
        print("=" * 40)
        
        if not self.start or not self.end:
            print("❌ Start or end position not found!")
            return None, None
        
        visited = set()
        nodes_explored = [0]  # Use list to modify in nested function
        
        def dfs_recursive(current_pos, path):
            visited.add(current_pos)
            nodes_explored[0] += 1
            
            print(f"  Step {nodes_explored[0]}: Exploring {current_pos}")
            
            if current_pos == self.end:
                print(f"🎉 SOLUTION FOUND!")
                return path
            
            # Try each neighbor
            for neighbor in self.graph.get(current_pos, []):
                if neighbor not in visited:
                    result = dfs_recursive(neighbor, path + [neighbor])
                    if result:  # Solution found
                        return result
            
            print(f"  🔙 Backtracking from {current_pos}")
            return None
        
        solution = dfs_recursive(self.start, [self.start])
        
        if solution:
            print(f"   Path length: {len(solution)} steps")
            print(f"   Nodes explored: {nodes_explored[0]}")
        else:
            print("❌ No solution found!")
        
        return solution, nodes_explored[0]
    
    def solve_dfs_iterative(self):
        """
        Solve maze using iterative DFS with explicit stack
        """
        print("📚 SOLVING MAZE WITH ITERATIVE DFS")
        print("=" * 40)
        
        if not self.start or not self.end:
            return None, None
        
        visited = set()
        stack = [(self.start, [self.start])]
        nodes_explored = 0
        
        while stack:
            current_pos, path = stack.pop()  # LIFO
            
            if current_pos in visited:
                continue
            
            visited.add(current_pos)
            nodes_explored += 1
            
            print(f"  Step {nodes_explored}: Exploring {current_pos}")
            
            if current_pos == self.end:
                print(f"🎉 SOLUTION FOUND!")
                print(f"   Path length: {len(path)} steps")
                print(f"   Nodes explored: {nodes_explored}")
                return path, nodes_explored
            
            # Add neighbors to stack (in reverse order for natural left-to-right exploration)
            neighbors = self.graph.get(current_pos, [])
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
        
        print("❌ No solution found!")
        return None, nodes_explored
    
    def find_all_paths(self, max_length=None):
        """
        Find all possible paths from start to end
        """
        print("🛣️ FINDING ALL POSSIBLE PATHS")
        print("=" * 30)
        
        if not self.start or not self.end:
            return []
        
        all_paths = []
        
        def dfs_all_paths(current_pos, path):
            if max_length and len(path) > max_length:
                return
            
            if current_pos == self.end:
                all_paths.append(path.copy())
                return
            
            for neighbor in self.graph.get(current_pos, []):
                if neighbor not in path:  # Avoid cycles
                    dfs_all_paths(neighbor, path + [neighbor])
        
        dfs_all_paths(self.start, [self.start])
        
        print(f"Found {len(all_paths)} paths")
        if all_paths:
            lengths = [len(path) for path in all_paths]
            print(f"Shortest path: {min(lengths)} steps")
            print(f"Longest path: {max(lengths)} steps")
        
        return all_paths
    
    def visualize_path(self, path):
        """
        Visualize the maze with the solution path
        """
        if not path:
            print("No path to visualize!")
            return
        
        print("🎨 MAZE VISUALIZATION WITH SOLUTION")
        print("=" * 40)
        
        # Create copy of grid
        visual_grid = [row[:] for row in self.grid]
        
        # Mark path (except start and end)
        for pos in path[1:-1]:
            r, c = pos
            visual_grid[r][c] = '*'
        
        # Print the maze
        print("Legend: S=Start, E=End, *=Path, #=Wall, .=Empty")
        print()
        for row in visual_grid:
            print(''.join(row))
        print()
    
    def compare_algorithms(self):
        """
        Compare BFS vs DFS performance
        """
        print("📊 ALGORITHM COMPARISON")
        print("=" * 25)
        
        # Test BFS
        bfs_path, bfs_explored = self.solve_bfs()
        
        print("\n" + "-"*50)
        
        # Test DFS (create new instance to reset)
        dfs_path, dfs_explored = self.solve_dfs()
        
        print("\n" + "-"*50)
        
        # Test Iterative DFS
        iter_dfs_path, iter_dfs_explored = self.solve_dfs_iterative()
        
        print("\n📈 RESULTS SUMMARY:")
        print("-" * 20)
        
        if bfs_path:
            print(f"BFS: {len(bfs_path)} steps, {bfs_explored} nodes explored")
        if dfs_path:
            print(f"DFS (recursive): {len(dfs_path)} steps, {dfs_explored} nodes explored")
        if iter_dfs_path:
            print(f"DFS (iterative): {len(iter_dfs_path)} steps, {iter_dfs_explored} nodes explored")
        
        if bfs_path and dfs_path:
            print(f"\nBFS found optimal path: {len(bfs_path) <= len(dfs_path)}")
            efficiency_bfs = len(bfs_path) / bfs_explored if bfs_explored > 0 else 0
            efficiency_dfs = len(dfs_path) / dfs_explored if dfs_explored > 0 else 0
            print(f"BFS efficiency: {efficiency_bfs:.3f}")
            print(f"DFS efficiency: {efficiency_dfs:.3f}")

def create_sample_maze():
    """Create a sample maze for testing"""
    return [
        ['S', '.', '#', '.', '.'],
        ['.', '.', '#', '.', '#'],
        ['#', '.', '.', '.', '#'],
        ['#', '#', '#', '.', '.'],
        ['.', '.', '.', '.', 'E']
    ]

def create_larger_maze():
    """Create a larger, more complex maze"""
    return [
        ['S', '.', '#', '.', '.', '.', '#', '.', '.'],
        ['.', '.', '#', '.', '#', '.', '#', '.', '#'],
        ['#', '.', '.', '.', '#', '.', '.', '.', '#'],
        ['#', '#', '#', '.', '#', '#', '#', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '#', '.', '#'],
        ['.', '#', '#', '#', '.', '.', '#', '.', '#'],
        ['.', '.', '.', '#', '.', '.', '.', '.', '.'],
        ['#', '#', '.', '#', '#', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', 'E']
    ]

def maze_solving_tips():
    """
    Tips for understanding maze solving algorithms
    """
    print("💡 MAZE SOLVING ALGORITHM TIPS")
    print("=" * 35)
    
    print("""
🎯 ALGORITHM CHOICE:
━━━━━━━━━━━━━━━━━━━

• Need shortest path? → BFS
• Any solution is fine? → DFS
• Memory limited? → DFS (less memory)
• Large maze? → BFS (more predictable)

🧠 HOW THEY WORK:
━━━━━━━━━━━━━━━━━

BFS (Breadth-First Search):
  • Explores all positions at distance 1, then 2, then 3...
  • Uses a queue (FIFO)
  • Guarantees shortest path
  • More memory usage

DFS (Depth-First Search):
  • Goes as deep as possible, then backtracks
  • Uses a stack (LIFO) or recursion
  • Finds any path (not necessarily shortest)
  • Less memory usage

⚡ PERFORMANCE TIPS:
━━━━━━━━━━━━━━━━━━━

• BFS is better for mazes with many short paths
• DFS is better for mazes with few long paths
• Use iterative DFS to avoid stack overflow
• Early termination when goal found

🔧 PRACTICAL APPLICATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━

• Video game pathfinding
• Robot navigation
• GPS route finding
• Puzzle solving
• Network routing
""")

def generate_random_maze(rows, cols, wall_probability=0.3):
    """
    Generate a random maze (might not always be solvable)
    """
    maze = [['.' for _ in range(cols)] for _ in range(rows)]
    
    # Add random walls
    for r in range(rows):
        for c in range(cols):
            if random.random() < wall_probability:
                maze[r][c] = '#'
    
    # Set start and end
    maze[0][0] = 'S'
    maze[rows-1][cols-1] = 'E'
    
    # Clear path around start and end
    if rows > 1:
        maze[1][0] = '.'
    if cols > 1:
        maze[0][1] = '.'
    if rows > 1:
        maze[rows-2][cols-1] = '.'
    if cols > 1:
        maze[rows-1][cols-2] = '.'
    
    return maze

if __name__ == "__main__":
    print("🎮 MAZE SOLVER DEMONSTRATION")
    print("=" * 40)
    
    # Test with sample maze
    print("Testing with sample 5x5 maze:")
    sample_maze = create_sample_maze()
    
    print("\nMaze layout:")
    for row in sample_maze:
        print(''.join(row))
    
    solver = MazeSolver(sample_maze)
    
    print(f"\nStart: {solver.start}")
    print(f"End: {solver.end}")
    
    # Compare algorithms
    solver.compare_algorithms()
    
    # Find and visualize shortest path
    print("\n" + "="*60)
    bfs_path, _ = solver.solve_bfs()
    solver.visualize_path(bfs_path)
    
    # Find all paths
    print("\n" + "="*60)
    all_paths = solver.find_all_paths(max_length=15)
    if all_paths:
        print(f"\nFirst few paths found:")
        for i, path in enumerate(all_paths[:3], 1):
            print(f"  Path {i}: {len(path)} steps")
    
    # Test with larger maze
    print("\n" + "="*80)
    print("Testing with larger 9x9 maze:")
    
    larger_maze = create_larger_maze()
    print("\nMaze layout:")
    for row in larger_maze:
        print(''.join(row))
    
    larger_solver = MazeSolver(larger_maze)
    larger_solver.compare_algorithms()
    
    # Tips
    print("\n" + "="*60)
    maze_solving_tips()
    
    # Test random maze
    print("\n" + "="*60)
    print("Testing with random 6x6 maze:")
    
    random.seed(42)  # For reproducible results
    random_maze = generate_random_maze(6, 6, 0.25)
    print("\nRandom maze layout:")
    for row in random_maze:
        print(''.join(row))
    
    random_solver = MazeSolver(random_maze)
    path, explored = random_solver.solve_bfs()
    random_solver.visualize_path(path)
    
    print("\n🎉 MAZE SOLVING COMPLETE!")
    print("🎯 Key Takeaway: BFS for shortest paths, DFS for any path!")