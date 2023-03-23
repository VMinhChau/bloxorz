def init():
    global row, col, block_id, objects, previous, is_test, pygame_display, is_bfs, goal_x, goal_y
    row, col, block_id, is_test, pygame_display, is_bfs, goal_x, goal_y = [0, 0, 0, 1, 0, 0, 0, 0]
    objects = []
    previous = []
