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
                        block.map = ''.join(''.join(l) for l in block.game_map)
                    else:
                        block.game_map[bridge_y][bridge_x] = '.'
                        block.map = ''.join(''.join(l) for l in block.game_map)
                elif obj["type"] == "open":
                    block.game_map[bridge_y][bridge_x] = '#'
                    block.map = ''.join(''.join(l) for l in block.game_map)
                elif obj["type"] == "close":
                    block.game_map[bridge_y][bridge_x] = '.'
                    block.map = ''.join(''.join(l) for l in block.game_map)
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
                        block.map = ''.join(''.join(l) for l in block.game_map)
                    else:
                        block.game_map[bridge_y][bridge_x] = '.'
                        block.map = ''.join(''.join(l) for l in block.game_map)
                elif obj["type"] == "open":
                    block.game_map[bridge_y][bridge_x] = '#'
                    block.map = ''.join(''.join(l) for l in block.game_map)
                elif obj["type"] == "close":
                    block.game_map[bridge_y][bridge_x] = '.'
                    block.map = ''.join(''.join(l) for l in block.game_map)
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
            # elif game_map[y-1][x] == 'o':
            #     sort_switch(block, x, y - 1)
            elif game_map[y+1][x] == 'o':
                sort_switch(block, x, y + 1)
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
    