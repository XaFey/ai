#Challenge 1
path, expanded, max_f = search_func(problem, visualize_grid, args.speed)
for state in path:
            # Don't color over the start or goal squares
    if state != problem.get_start_state() and state != problem.goal:
        rect = pygame.Rect(state[0]*CELL_SIZE, state[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, COLORS['path'], rect)


