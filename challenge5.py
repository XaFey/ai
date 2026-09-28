#Challenge 5
class Arm(SearchProblem):
    def __init__(self):
        self.grid_size = 10
        self.start = (0,0)
        self.goal = (3, 0)
        self.obstacles = {(1,2), (2, 2), (5, 3), }

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
# 2 3 4 5 on paper