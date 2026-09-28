#Challenge 3
class GridProblem2(SearchProblem):
    def __init__(self):
        self.grid_size = 5
        self.start = (0,0, 0)
        self.goal = (4, 4)
        #x, y, time
        self.obstacles = {(1,1), (2, 2), (3, 3)}

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        x, y, t = state
        return state == self.goal

    def get_successors(self, state):
        x, y, t = state
        directions = [(-1, 0), (1,0), (0,-1), (0,1), (0,0)]
        successors = []
        for dx, dy in directions:
            nx, ny = x +dx, y + dy
            if 0<=nx < self.grid_size and 0 <= ny <self.grid_size and (nx, ny) not in self.obstacles:
                successors.append(((nx, ny), f"Move ({dx}, {dy})", 1))
        return successors

    def heuristic(self, state):
        return abs(state[0] - self.goal[0] + abs(state[1] - self.goal[1]))