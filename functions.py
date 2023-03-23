import global_variables
from treenode import TreeNode

def add_move(queue, block):
    if process_state(block):
        if is_visited(block):
            return None
        else:
            queue.append(block)
            global_variables.previous.append(block)
            return True
        
    return False


def sort_switch(block, x, y):
    game_map = block.game_map
    for obj in global_variables.objects:
        if (x, y) == (obj["position"][0], obj["position"][1]):  # find object by position
            if obj["switch"] != "sort_switch":  # for debugging
                print("sort_switch wrong type !!!")
                break
            blocks_4_process = obj["blocks_process"]
            for i in range(blocks_4_process):
                bridge_x = obj["point"][i][0]
                bridge_y = obj["point"][i][1]

                if obj["type"] == "toggle":
                    if game_map[bridge_y][bridge_x] == '.':
                        block.game_map[bridge_y][bridge_x] = '#'
                    else:
                        block.game_map[bridge_y][bridge_x] = '.'
                elif obj["type"] == "open":
                    block.game_map[bridge_y][bridge_x] = '#'

                elif obj["type"] == "close":
                    block.game_map[bridge_y][bridge_x] = '.'
                else:
                    print("Error at func sort_switch")


def hard_switch(block, x, y):
    for obj in global_variables.objects:
        if (x, y) == (obj["position"][0], obj["position"][1]):  # find object by position
            if obj["switch"] != "hard_switch":  # for debugging
                print("sort_switch wrong type !!!")
                break
            blocks_4_process = obj["blocks_process"]
            for i in range(blocks_4_process):
                bridge_x = obj["point"][i][0]
                bridge_y = obj["point"][i][1]

                if obj["type"] == "toggle":
                    if block.game_map[bridge_y][bridge_x] == '.':
                        block.game_map[bridge_y][bridge_x] = '#'
                    else:
                        block.game_map[bridge_y][bridge_x] = '.'
                elif obj["type"] == "open":
                    block.game_map[bridge_y][bridge_x] = '#'

                elif obj["type"] == "close":
                    block.game_map[bridge_y][bridge_x] = '.'
                else:
                    print("Error at func hard_switch")


def teleport_switch(block, x, y):
    for obj in global_variables.objects:
        if (x, y) == (obj["position"][0], obj["position"][1]):  # find object by position
            if obj["switch"] != "teleport_switch":  # for debugging
                print("teleport_switch wrong type !!!")
                break
            block.x = obj["point"][0][0]
            block.y = obj["point"][0][1]
            block.x_split = obj["point"][1][0]
            block.y_split = obj["point"][1][1]
            block.status = "SPLIT"


def process_state(block):
    if is_valid_move(block):
        x = block.x
        y = block.y
        x_split = block.x_split
        y_split = block.y_split
        status = block.status
        game_map = block.game_map
        # if standing then hard button can be pressed
        if status == "STAND" and game_map[y][x] == "x":
            hard_switch(block, x, y)
        if status == "STAND" and game_map[y][x] == 'o':
            sort_switch(block, x, y)
        if status == "LIE_HORIZONTAL":
            if game_map[y][x] == 'o':
                sort_switch(block, x, y)
            # elif game_map[y][x-1] == 'o':
            #     sort_switch(block, x - 1, y)
            elif game_map[y][x+1] == 'o':
                sort_switch(block, x + 1, y)
        if status == "LIE_VERTICAL":
            if game_map[y][x] == 'o':
                # print(str(x) + ' ' + str(y))
                sort_switch(block, x, y)
            elif game_map[y-1][x] == 'o':
                sort_switch(block, x, y - 1)
            # elif game_map[y+1][x] == 'o':
            #     sort_switch(block, x, y + 1)
        if status == "SPLIT" and game_map[y][x] == 'o':
            sort_switch(block, x, y)
        if status == "SPLIT" and game_map[y_split][x_split] == 'o':
            sort_switch(block, x_split, y_split)
        if status == "STAND" and game_map[y][x] == "@":
            teleport_switch(block, x, y)

        #  if block status is "split" and 2 split parts are close enough then make it a complete block
        if status == "SPLIT":
            if y == y_split and x == x_split - 1:
                block.status = "LIE_HORIZONTAL"
            if y == y_split and x == x_split + 1:
                block.status = "LIE_HORIZONTAL"
                block.x = x_split

            if y == y_split - 1 and x == x_split:
                block.status = "LIE_VERTICAL"
            if y == y_split + 1 and x == x_split:
                block.status = "LIE_VERTICAL"
                block.y = y_split
        return True
    else:
        return False


def is_valid_move(block):
    x = block.x
    y = block.y
    x_split = block.x_split
    y_split = block.y_split
    status = block.status
    game_map = block.game_map
    # guard: not out of the board
    if x < 0 or y < 0 or x >= global_variables.col or y >= global_variables.row:
        return False
    else:
        if x_split is not None and y_split is not None:
            if x_split < 0 or y_split < 0 or x_split >= global_variables.col \
                    or y_split >= global_variables.row or game_map[y_split][x_split] == ".":
                return False

    if game_map[y][x] == ".":
        return False
    if status == "STAND":
        if game_map[y][x] == "=":  # can not stand on sort ground
            return False
    if status == "LIE_VERTICAL":
        if y >= global_variables.row - 1:
            return False
        if game_map[y+1][x] == '.':
            return False
    if status == "LIE_HORIZONTAL":
        if x >= global_variables.col - 1:
            return False
        if game_map[y][x+1] == '.':
            return False

    return True


def is_visited(block):
    if block.status != "SPLIT":
        for i in global_variables.previous:
            if i.x == block.x and i.y == block.y \
                    and i.status == block.status and i.game_map == block.game_map:
                return True
    else:
        for i in global_variables.previous:
            if i.x == block.x and i.y == block.y \
                    and i.x_split == block.x_split and i.y_split == block.y_split \
                    and i.status == block.status and i.game_map == block.game_map:
                return True
    return False


def check_win(block):
    x = block.x
    y = block.y
    status = block.status
    game_map = block.game_map
    #   if block is standing and its position is match with goal then return true
    if status == "STAND" and game_map[y][x] == "G":
        return True
    else:
        return False


def view_2d_solution(block):
    x = block.x
    y = block.y
    x_split = block.x_split
    y_split = block.y_split
    status = block.status
    game_map = block.game_map
    if status != "SPLIT":
        for i in range(len(game_map)):
            print("", end='  ')
            for j in range(len(game_map[i])):
                if (i == y and j == x and status == "STAND") \
                        or ((i == y and j == x) or (i == y and j == x + 1) and status == "LIE_HORIZONTAL") \
                        or ((i == y and j == x) or (i == y + 1 and j == x) and status == "LIE_VERTICAL"):

                    print("+", end=' ')

                elif game_map[i][j] == '.':
                    print(" ", end=' ')
                else:
                    print(game_map[i][j], end=' ')
            print("")
    else:
        for i in range(len(game_map)):
            print("", end='  ')
            for j in range(len(game_map[i])):
                if (i == y and j == x) or (i == y_split and j == x_split):
                    print("+", end=' ')
                elif game_map[i][j] == ".":
                    print(" ", end=' ')
                else:
                    print(game_map[i][j], end=' ')
            print("")


def solution_path(block):
    solution = [block]
    temp = block.prev
    while temp is not None:
        solution.append(temp)
        temp = temp.prev
    solution.reverse()
    return solution


def convert_solution_map(solution):
    for s in solution:
        if s.status == "STAND":
            s.game_map[s.y][s.x] = '+'
        elif s.status == "LIE_VERTICAL":
            s.game_map[s.y][s.x] = '+'
            if s.prev.status == "STAND":
                if s.y < s.prev.y:  # block was in stand state and moved up
                    s.game_map[s.y + 1][s.x] = '+'
                else:               # block was in stand state and moved down
                    s.game_map[s.y + 1][s.x] = '+'
            elif s.prev.status == "LIE_VERTICAL":
                if s.x < s.prev.x:  # block was in lie vertical state and moved left
                    s.game_map[s.y + 1][s.x] = '+'
                else:               # block was in lie vertical state and moved right
                    s.game_map[s.y + 1][s.x] = '+'
            elif s.prev.status == "SPLIT":
                s.game_map[s.y_split][s.x_split] = '+'
        elif s.status == "LIE_HORIZONTAL":
            s.game_map[s.y][s.x] = '+'
            if s.prev.status == "STAND":
                if s.x < s.prev.x:  # block was in stand state and moved to left
                    s.game_map[s.y][s.x + 1] = '+'
                else:
                    s.game_map[s.y][s.x + 1] = '+'
            elif s.prev.status == "LIE_HORIZONTAL":
                if s.y < s.prev.y:
                    s.game_map[s.y][s.prev.x + 1] = '+'
                else:
                    s.game_map[s.y][s.prev.x + 1] = '+'
            elif s.prev.status == "SPLIT":
                s.game_map[s.y_split][s.x_split] = '+'
        elif s.status == "SPLIT":
            s.game_map[s.y][s.x] = '+'
            s.game_map[s.y_split][s.x_split] = '+'


def add_move_ga(valid_dna_s, cnt, block):
    if process_state(block):
        valid_dna_s.append(block)
        cnt += 1
    return cnt


def add_move_fitness(block):
    if process_state(block):
        return True
    return False


# def check_win_dna(dna, block):
#     global_variables.previous = []
#     valid_dna_s = [block]
#     cnt = 0
#     for gene in dna.genes:
#         if gene == dna.U:
#             cnt = add_move_ga(valid_dna_s, cnt, valid_dna_s[cnt].move_up())
#         elif gene == dna.R:
#             cnt = add_move_ga(valid_dna_s, cnt, valid_dna_s[cnt].move_right())
#         elif gene == dna.D:
#             cnt = add_move_ga(valid_dna_s, cnt, valid_dna_s[cnt].move_down())
#         else:
#             cnt = add_move_ga(valid_dna_s, cnt, valid_dna_s[cnt].move_left())
#     for valid_dna in valid_dna_s:
#         if check_win(valid_dna):
#             return True
#     return False


# def ga_solution_reprocess(solution, block):
#     res = [block]
#     for direction in solution.genes:
#         if direction == "up":
#             block = block.move_up()
#             if add_move_fitness(block):
#                 res.append(block)
#             else:
#                 block = block.move_down()
#         elif direction == "right":
#             block = block.move_right()
#             if add_move_fitness(block):
#                 res.append(block)
#             else:
#                 block = block.move_left()
#         elif direction == "down":
#             block = block.move_down()
#             if add_move_fitness(block):
#                 res.append(block)
#             else:
#                 block = block.move_up()
#         else:
#             block = block.move_left()
#             if add_move_fitness(block):
#                 res.append(block)
#             else:
#                 block = block.move_right()
#         if check_win(block):
#             break
#     return res
# def distance_euclidean(pos1, pos2):
#     return sqrt((pos1[1] - pos2[1]) ** 2 + (pos1[0] - pos2[0]) ** 2)

# def compute_heuristic_costs(block, target_pos):
#     costs = dict()
#     num = 0
#     for y in range(len(block.game_map)):
#         for x in range(len(block.game_map[0])):
#             pos = (x, y)
#             if not is_off_map(pos,block):
#                 costs[num] = distance_euclidean(pos, target_pos)
#             else:
#                 costs[num] = inf
#             num += 1
#     return costs

# def min_h_cost(h_costs, node):
#         if node.block.status == "STAND":
#             index = node.block.y * global_variables.col + node.block.x
#             value=h_costs[index]
#             # print("Position: ", (node.block.x,node.block.y,node.block.status))
#             # print("Index: ", index)
#             # print("Hcost: ", value)
#             return value

#         if node.block.status  == "LIE_VERTICAL":
#             index1 = node.block.y * global_variables.col + node.block.x
#             index2 = (node.block.y + 1) * global_variables.col + node.block.x
#             value=min(h_costs[index1], h_costs[index2])
#             # print("Position: ", (node.block.x,node.block.y,node.block.status))
#             # print("Hcost: ", value)
#             return value

#         if node.block.status  == "LIE_HORIZONTAL":
#             index1 = node.block.y * global_variables.col + node.block.x
#             index2 = node.block.y * global_variables.col + (node.block.x + 1)
#             value=min(h_costs[index1], h_costs[index2])
#             # print("Position: ", (node.block.x,node.block.y,node.block.status))
#             # print("Hcost: ", value)
#             return value
        
# def get_cost_visited(pos, cost_visited: dict):
#     cost = namedtuple("cost", ['x', 'y', 'status'])
#     index = cost(x=pos[0], y=pos[1], status=pos[2])
#     print(index, cost_visited[index])
#     return cost_visited[index]

# def set_cost_visited(pos, value: int, cost_visited):
#     cost = namedtuple("cost", ['x', 'y', 'status'])
#     index = cost(x=pos[0], y=pos[1], status=pos[2])
#     cost_visited[index] = value

# def add_move_astar(expanded_nodes, block, cost_visited, heuristic_costs):
#     if process_state(block):
#         g_cost = get_cost_visited((block.prev.x,block.prev.y), cost_visited) + 1
#         if (block.x,block.y,block.status) not in  or g_cost < get_cost_visited((block.x,block.y), cost_visited):
#             new_node = TreeNode(block)
#             h_cost = min_h_cost(heuristic_costs, new_node)
#             new_node.f_cost = g_cost + h_cost
#             heappush(expanded_nodes, new_node)
#             print((block.prev.x,block.prev.y,block.prev.status))
#             print((block.x,block.y,block.status))
#             print(new_node.f_cost,g_cost,h_cost)
#             print("")
#             global_variables.previous.append(new_node.block)
#             return True
#         else:
#             return None
#     return False

# def is_off_map(pos,block):
#     if pos[0] < 0 or pos[1] < 0 or pos[0] >= global_variables.col or pos[1] >= global_variables.row or block.game_map[pos[1]][pos[0]] == '.':
#         return True
#     else:
#         return False
    