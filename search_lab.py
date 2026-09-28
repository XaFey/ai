import pygame
import sys
import argparse
import time
from collections import deque, defaultdict
import heapq

class SearchProblem:
    def get_start_state(self):
        pass
    def is_goal(self, state):
        pass
    def get_successors(self, state):
        pass
###################
###The Problems###
###################
class GridProblem(SearchProblem):
    def __init__(self):
        self.grid_size = 5
        self.start = (0,0)
        self.goal = (4, 4)
        self.obstacles = {(1,1), (2, 2), (3, 3)}

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def get_successors(self, state):
        x, y = state
        directions = [(-1, 0), (1,0), (0,-1), (0,1)]
        successors = []
        for dx, dy in directions:
            nx, ny = x +dx, y + dy
            if 0<=nx < self.grid_size and 0 <= ny <self.grid_size and (nx, ny) not in self.obstacles:
                successors.append(((nx, ny), f"Move ({dx}, {dy})", 1))
        return successors

    def heuristic(self, state):
        return abs(state[0] - self.goal[0] + abs(state[1] - self.goal[1]))

class Romania(SearchProblem):
    def __init__(self):
        self.start = 'Arad'
        self.goal = 'Bucharest'
        self.map_data = {
            'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
            'Zerind': [('Arad', 75), ('Oradea', 71)],
            'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
            'Timisoara': [('Arad', 118), ('Lugoj', 111)],
            'Oradea': [('Zerind', 71), ('Sibiu', 151)],
            'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
            'Mehadia': [('Lugoj', 70), ('Dobreta', 75)],
            'Dobreta': [('Mehadia', 75), ('Craiova', 120)],
            'Craiova': [('Dobreta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
            'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
            'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
            'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
            'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
            'Giurgiu': [('Bucharest', 90)],
            'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
            'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
            'Eforie': [('Hirsova', 86)],
            'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
            'Iasi': [('Vaslui', 92), ('Neamt', 87)],
            'Neamt': [('Iasi', 87)]
        }
        # Straight-line distance heuristic to Bucharest
        self.h_values = {
            'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Dobreta': 242,
            'Eforie': 161, 'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151,
            'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
            'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193, 'Sibiu': 253,
            'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
        }

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def get_successors(self, state):
        successors = []
        for neighbor, cost in self.map_data.get(state, []):
            successors.append((neighbor, f"Drive to {neighbor}", cost))
        return successors

    def heuristic(self, state):
        return self.h_values.get(state, 0)

class Ei_Puzzle(SearchProblem):
    def __init__(self):
        self.start = ((7, 2, 4), (5, 0, 6), (8, 3, 1))
        self.goal = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def get_successors(self, state):
        successors = []
        r, c = next((i, j) for i, row in enumerate(state) for j, val in enumerate(row) if val == 0)
        
        directions = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
        for dr, dc, name in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_board = [list(row) for row in state]
                new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
                new_state = tuple(tuple(row) for row in new_board)
                successors.append((new_state, f"Slide {name}", 1))
        return successors

    def heuristic(self, state):
        dist = 0
        for r in range(3):
            for c in range(3):
                val = state[r][c]
                if val != 0:
                    
                    gr, gc = next((i, j) for i, row in enumerate(self.goal) for j, v in enumerate(row) if v == val)
                    dist += abs(r - gr) + abs(c - gc)
        return dist

class Cannibals(SearchProblem):
    def __init__(self):
        self.start = (3, 3, 1)
        self.goal = (0, 0, 0)

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def get_successors(self, state):
        successors = []
        m_l, c_l, boat = state
        
        boat_moves = [(1,0), (2,0), (0,1), (0,2), (1,1)]
        
        for dm, dc in boat_moves:
            if boat == 1: 
                nm_l, nc_l, n_boat = m_l - dm, c_l - dc, 0
            else: 
                nm_l, nc_l, n_boat = m_l + dm, c_l + dc, 1
                
            if 0 <= nm_l <= 3 and 0 <= nc_l <= 3:
                right_m, right_c = 3 - nm_l, 3 - nc_l
                left_valid = (nm_l == 0 or nm_l >= nc_l)
                right_valid = (right_m == 0 or right_m >= right_c)
                
                if left_valid and right_valid:
                    successors.append(((nm_l, nc_l, n_boat), f"Move {dm}M, {dc}C", 1))
        return successors

    def heuristic(self, state):
\        return (state[0] + state[1]) // 2

class Water_Jugs(SearchProblem):
    def __init__(self):
        self.start = (0, 0)

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        # Goal is exactly 2 gallons in the 4-gallon jug
        return state[0] == 2

    def get_successors(self, state):
        j4, j3 = state
        successors = []
        
        # 1. Fill Jug 4
        successors.append(((4, j3), "Fill Jug 4", 1))
        # 2. Fill Jug 3
        successors.append(((j4, 3), "Fill Jug 3", 1))
        # 3. Empty Jug 4
        successors.append(((0, j3), "Empty Jug 4", 1))
        # 4. Empty Jug 3
        successors.append(((j4, 0), "Empty Jug 3", 1))
        
        # 5. Pour Jug 4 into Jug 3
        pour = min(j4, 3 - j3)
        successors.append(((j4 - pour, j3 + pour), "Pour 4 into 3", 1))
        
        # 6. Pour Jug 3 into Jug 4
        pour = min(j3, 4 - j4)
        successors.append(((j4 + pour, j3 - pour), "Pour 3 into 4", 1))
        
        return successors

    def heuristic(self, state):
        return abs(2 - state[0])

class Vacuum_World(SearchProblem):
    def __init__(self):
        # Robot starts in 'A', both rooms are dirty (True)
        self.start = ('A', True, True)

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        _, a_dirty, b_dirty = state
        return not a_dirty and not b_dirty

    def get_successors(self, state):
        pos, a_dirty, b_dirty = state
        successors = []
        
        # Action: Suck dirt if current room is dirty
        if pos == 'A' and a_dirty:
            successors.append((('A', False, b_dirty), "Suck A", 1))
        elif pos == 'B' and b_dirty:
            successors.append((('B', a_dirty, False), "Suck B", 1))
            
        # Action: Move Left/Right
        if pos == 'A':
            successors.append((('B', a_dirty, b_dirty), "Move to B", 1))
        else:
            successors.append((('A', a_dirty, b_dirty), "Move to A", 1))
            
        return successors

    def heuristic(self, state):
        # Count remaining dirty rooms
        return sum([state[1], state[2]])

class Sliding_Tile(SearchProblem):
    def __init__(self):
        self.start = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 0, 12), (13, 14, 11, 15))
        self.goal = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def get_successors(self, state):
        successors = []
        r, c = next((i, j) for i, row in enumerate(state) for j, val in enumerate(row) if val == 0)
        
        directions = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
        for dr, dc, name in directions:
            nr, nc = r + dr, c + dc
            # Notice the boundary check is now 4 instead of 3
            if 0 <= nr < 4 and 0 <= nc < 4:
                # Create new board configuration via deep copy and swap
                new_board = [list(row) for row in state]
                new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
                new_state = tuple(tuple(row) for row in new_board)
                successors.append((new_state, f"Slide {name}", 1))
        return successors

    def heuristic(self, state):
        # Manhattan Distance Heuristic
        dist = 0
        # Loops check 4 rows and 4 columns
        for r in range(4):
            for c in range(4):
                val = state[r][c]
                if val != 0:
                    # Find where val belongs in goal
                    gr, gc = next((i, j) for i, row in enumerate(self.goal) for j, v in enumerate(row) if v == val)
                    dist += abs(r - gr) + abs(c - gc)
        return dist

class River(SearchProblem):
    def __init__(self):
        self.start = (frozenset(['F', 'W', 'G', 'C']), 1)
        self.goal = (frozenset(), 0)

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return len(state[0]) == 0 and state[1] == 0

    def get_successors(self, state):
        successors = []
        bank, farmer_side = state
        other_bank = frozenset(['F', 'W', 'G', 'C']) - bank
        
        if farmer_side == 1: 
            travellers = [frozenset(['F'])] + [frozenset(['F', item]) for item in bank if item != 'F']
            for t in travellers:
                new_start_bank = bank - t
                new_other_bank = other_bank | t
                
                if self._is_valid(new_start_bank) and self._is_valid(new_other_bank):
                    successors.append(((new_start_bank, 0), f"Cross with {list(t)}", 1))
        else:
            travellers = [frozenset(['F'])] + [frozenset(['F', item]) for item in other_bank if item != 'F']
            for t in travellers:
                new_start_bank = bank | t
                new_other_bank = other_bank - t
                
                if self._is_valid(new_start_bank) and self._is_valid(new_other_bank):
                    successors.append(((new_start_bank, 1), f"Return with {list(t)}", 1))
                    
        return successors

    def _is_valid(self, bank_contents):
        if 'W' in bank_contents and 'G' in bank_contents and 'F' not in bank_contents:
            return False
        if 'G' in bank_contents and 'C' in bank_contents and 'F' not in bank_contents:
            return False
        return True

    def heuristic(self, state):
        return len(state[0])
    
class CustomMaze(SearchProblem):
    def __init__(self):
        self.grid_size = 10
        self.start = (0,0)
        self.goal = (9,9)
        self.obstacles = {(1, 2), (1,3), (2, 5), (3, 1), (3, 4), (4, 6), (4 ,7),
                          (5, 0), (5, 9), (6,3), (6, 5), (7, 1), (8,4), (9, 2), (2,8),
                          (3,9), (0,5)}

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def get_successors(self, state):
        x, y = state
        directions = [(-1, 0), (1,0), (0,-1), (0,1)]
        successors = []
        for dx, dy in directions:
            nx, ny = x +dx, y + dy
            if 0<=nx < self.grid_size and 0 <= ny <self.grid_size and (nx, ny) not in self.obstacles:
                successors.append(((nx, ny), f"Move ({dx}, {dy})", 1))
        return successors

    def heuristic(self, state):
        return abs(state[0] - self.goal[0] + abs(state[1] - self.goal[1]))
##############################################
###The Search Methods###
##############################################
def bfs(problem, visualize_func, speed):
    start = problem.get_start_state()
    frontier = deque([start])
    came_from = {start: None}
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        current = frontier.popleft()
        explored.add(current)
        nodes_expanded += 1
        visualize_func(problem, explored, set(frontier), current, came_from)
        time.sleep(speed)

        if problem.is_goal(current):
            return reconstruct_path(came_from, current), nodes_expanded, max_frontier
        for next_state, _, _ in problem.get_successors(current):
            if next_state not in came_from:
                frontier.append(next_state)
                came_from[next_state] = current
                max_frontier = max(max_frontier, len(frontier))
    return None, nodes_expanded, max_frontier

def dfs(problem, visualize_func, speed):
    start = problem.get_start_state()
    frontier = [start]
    came_from = {start: None}
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        current = frontier.pop()
        explored.add(current)
        nodes_expanded += 1
        visualize_func(problem, explored, set(frontier), current, came_from)
        time.sleep(speed)

        if problem.is_goal(current):
            return reconstruct_path(came_from, current), nodes_expanded, max_frontier
        for next_state, _, _ in problem.get_successors(current):
            if next_state not in came_from:
                frontier.append(next_state)
                came_from[next_state] = current
                max_frontier = max(max_frontier, len(frontier))
    return None, nodes_expanded, max_frontier

def ucs(problem, visualize_func, speed):
    def ucs(problem, visualize_func, speed):
        start = problem.get_start_state()
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    
    csf = {start: 0} 
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        current_cost, current = heapq.heappop(frontier) 
        
        if current in explored:
            continue
            
        explored.add(current)
        nodes_expanded += 1
        
        frontier_states = set([item[-1] for item in frontier])
        visualize_func(problem, explored, frontier_states, current, came_from)
        time.sleep(speed)

        if problem.is_goal(current):
            return reconstruct_path(came_from, current), nodes_expanded, max_frontier
            
        for next_state, _, step_cost in problem.get_successors(current):
            if next_state not in csf or nc < csf[next_state]:
                csf[next_state] = nc 
                heapq.heappush(frontier, (nc, next_state))
                came_from[next_state] = current
                max_frontier = max(max_frontier, len(frontier))
                
    return None, nodes_expanded, max_frontier
def greedy(problem, visualize_func, speed):
    start = problem.get_start_state()
    frontier = []
    heapq.heappush(frontier, (problem.heuristic(start), start))
    
    came_from = {start: None}
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        h_cost, current = heapq.heappop(frontier)
        
        if current in explored: 
            continue
            
        explored.add(current)
        nodes_expanded += 1
        
        frontier_states = set([item[-1] for item in frontier])
        visualize_func(problem, explored, frontier_states, current, came_from)
        time.sleep(speed)

        if problem.is_goal(current):
            return reconstruct_path(came_from, current), nodes_expanded, max_frontier
        
        for next_state, _, _ in problem.get_successors(current):
            # Greedy doesn't care about optimal cost, just if it has been visited
            if next_state not in explored and next_state not in came_from:
                heapq.heappush(frontier, (problem.heuristic(next_state), next_state))
                came_from[next_state] = current
                max_frontier = max(max_frontier, len(frontier))
                
    return None, nodes_expanded, max_frontier
def astar(problem, visualize_func, speed):
    start = problem.get_start_state()
    frontier = []
    # heapq tuple: (f_cost, g_cost, state)
    heapq.heappush(frontier, (problem.heuristic(start), 0, start))
    
    came_from = {start: None}
    cost_so_far = {start: 0} # Tracks the actual g_cost
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        f_cost, current_g, current = heapq.heappop(frontier)
        
        if current in explored: 
            continue
            
        explored.add(current)
        nodes_expanded += 1
        
        frontier_states = set([item[-1] for item in frontier])
        visualize_func(problem, explored, frontier_states, current, came_from)
        time.sleep(speed)

        if problem.is_goal(current):
            return reconstruct_path(came_from, current), nodes_expanded, max_frontier
        
        for next_state, _, step_cost in problem.get_successors(current):
            new_g = current_g + step_cost
            
            # If we found an unvisited state, OR a cheaper route to an existing state
            if next_state not in cost_so_far or new_g < cost_so_far[next_state]:
                cost_so_far[next_state] = new_g
                
                # f = g (actual past cost) + h (estimated future cost)
                f_value = new_g + problem.heuristic(next_state)
                
                heapq.heappush(frontier, (f_value, new_g, next_state))
                came_from[next_state] = current
                max_frontier = max(max_frontier, len(frontier))
                
    return None, nodes_expanded, max_frontier

def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]

pygame.init()
CELL_SIZE = 100
COLORS = {
    'bg': (255, 255, 255), 'grid': (0,0,0), 'explored': (200, 200, 200),
    'frontier': (0, 0, 255), 'current': (255, 0, 0), 'goal': (0, 255, 0),
    'path': (255, 255, 0), 'obstacle': (100, 100, 100), 'start': (0, 0, 255)
}

def visualize_grid(problem, explored, frontier, current, came_from):
    screen = pygame.display.set_mode((problem.grid_size * CELL_SIZE, problem.grid_size * CELL_SIZE))
    screen.fill(COLORS['bg'])

    for x in range(problem.grid_size):
        for y in range(problem.grid_size):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLORS['grid'], rect, 1)
            state = (x, y)
            if state in problem.obstacles:
                pygame.draw.rect(screen, COLORS['obstacle'], rect)
            elif state == problem.get_start_state:
                pygame.draw.rect(screen, COLORS['state'], rect)
            elif state == problem.goal:
                pygame.draw.rect(screen, COLORS['goal'], rect)
            elif state in explored:
                pygame.draw.rect(screen, COLORS['explored'], rect)
            elif state in frontier:
                pygame.draw.rect(screen, COLORS['frontier'], rect)

            if current:
                rect = pygame.Rect(current[0]*CELL_SIZE, current[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLORS['current'], rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', required=True, choices=['bfs', 'dfs', 'ucs', 'greedy', 'astar'])
    parser.add_argument('--problem', type=int, required=True, choices=range(1,11))
    parser.add_argument('--speed', type=float, default = 0.5)
    args= parser.parse_args()
    
    problems = {
        1: GridProblem(), 2: Ei_Puzzle(), 3: Cannibals(), 4: Water_Jugs(), 
        5: Vacuum_World(), 6: Sliding_Tile(), 8: River(), 9: CustomMaze(), 10: Romania()
    }
    problem = problems[args.problem]

    strategies = {
        'bfs': bfs, 'dfs': dfs, 'ucs': ucs, 'greedy':greedy, 'astar': astar
 }
    search_func = strategies[args.strategy]

    path, expanded, max_f = search_func(problem, visualize_grid, args.speed)
    print(f'Path: {path}\n Expanded: {expanded}\n Max Frontier: {max_f}')
    if path:
        print(f'Cost: {len(path) - 1}')

if __name__ == "__main__":
    main()


#Challenge 1
path, expanded, max_f = search_func(problem, visualize_grid, args.speed
for state in path:
            # Don't color over the start or goal squares
    if state != problem.get_start_state() and state != problem.goal:
        rect = pygame.Rect(state[0]*CELL_SIZE, state[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, COLORS['path'], rect)
# 2 3 4 5 on paper
