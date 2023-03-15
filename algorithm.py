from block import Block
import global_variables
from functions import check_win, add_move, solution_path, compute_heuristic_costs, min_h_cost, set_cost_visited, get_cost_visited, heappush, heappop, add_move_astar
from genetic_algorithm import ga
from treenode import TreeNode


def BFS(block):
    global_variables.previous = [block]  # save previous states
    queue = [block]
    solution = []
    while queue:
        current = queue.pop(0)
        if check_win(current):
            print("Success!\nFound solution after", current.id, "steps:")
            solution = solution_path(current)
            break

        if current.status != "SPLIT":  # if this is a complete block then it can move 4 directions
            add_move(queue, current.move_up())
            add_move(queue, current.move_right())
            add_move(queue, current.move_down())
            add_move(queue, current.move_left())

        else:
            add_move(queue, current.split_move_up())
            add_move(queue, current.split_move_right())
            add_move(queue, current.split_move_down())
            add_move(queue, current.split_move_left())

            add_move(queue, current.split_move_up_other())
            add_move(queue, current.split_move_right_other())
            add_move(queue, current.split_move_down_other())
            add_move(queue, current.split_move_left_other())
    return solution


# def genetic_algorithm(block):
#     solution = ga(block)
#     ga_solution_path = ga_solution_reprocess(solution, block)
#     return ga_solution_path



def solve_by_astar( block):
        """
        Solve the Bloxorz problem using A* algorithm.
        :param head: head node.
        :param target_pos: target position for heuristic estimates.
        """

        # compute the heuristic cost from all valid positions to the target positions
        for y in range(0, global_variables.row):
            for x in range(0, global_variables.col):
                if block.game_map[y][x] == 'G':
                    target_pos = (y,x)
        heuristic_costs = compute_heuristic_costs(block, target_pos)
        head = TreeNode(block)
        head.f_cost = min_h_cost(heuristic_costs, head)
        cost_visited = dict()
        set_cost_visited((block.y,block.x), 0, cost_visited)

        expanded_nodes = list()
        # expanded_nodes.append(head)
        # steps = 0
        current = head
        

        # print("Step: {}, Depth: {}, Cost: {} - {}".format(
        #         steps, self.get_node_depth(head), self.get_cost_visited(head.brick.pos), str(head)))
        # self.show(head.brick)

        # while True:
        #     for next_pos, direction in next_valid_move(node, []):

        #         g_cost = get_cost_visited((node.block.y,node.block.x), cost_visited) + 1

        #         # if the node is not visited, add to expanded queue.
        #         # if the node is visited, but has lower actual cost than previously recorded, add to expanded queue.
        #         if next_pos not in cost_visited or g_cost < get_cost_visited(next_pos):
        #             # new node and estimated cost.
        #             new_node = TreeNode(Block(next_pos[0], next_pos[1], node.block.status, node.block, node.game_map, id=global_variables.block_id))
        #             h_cost = min_h_cost(heuristic_costs, new_node)

        #             new_node.f_cost = g_cost + h_cost
        #             # set current node's child pointer.
        #             # setattr(node, direction.name.lower(), new_node)     # node.{left|right|up|down} -> new_node

        #             # link new_node to the current node.
        #             new_node.block.prev = node.block
        #             # new_node.dir_from_parent = direction
        #             heappush(expanded_nodes, new_node)
        #         #     self.debug("{:10s}: {:21s} - {} [f_cost: {:.2f} = {} + {:.2f}] ".format(
        #         #         "added", "new | visited & cheap", str(new_node), new_node.f_cost, g_cost, h_cost))
        #         # else:
        #         #     self.debug("{:10s}: {:21s} - [hash(Parent): {}, Parent->{}] [Cost now: {}, earlier: {}]".format(
        #         #         "rejected", "visited & costly", hash(node), direction.name.lower(), g_cost,
        #         #         self.get_cost_visited(next_pos)))

        #     node = heappop(expanded_nodes)
        #     # self.debug("{:10s}: {:21s} - {}".format("removed", "frontier node", str(node)))

        #     # update cost of this node
        #     set_cost_visited((node.block.y,node.block.x), get_cost_visited((node.block.prev.y,node.block.prev.x)) + 1, cost_visited)

        #     steps += 1
        #     # print("Step: {}, Depth: {}, Cost: {} - {} [f_cost: {:.2f}]".format(
        #     #     steps, self.get_node_depth(node), self.get_cost_visited(node.brick.pos), str(node), node.f_cost))
        #     # self.show(node.brick)

        #     # if goal state is dequeued, mark the search as completed.
        #     if node.block.y == target_pos[0] & node.block.x == target_pos[1]:
        #         break

        global_variables.previous = [head.block]  # save previous states
        # queue = [head]
        solution = []
       
        while True:
            
            if check_win(current.block):
                print("Success!\nFound solution after", current.block.id, "steps:")
                solution = solution_path(current.block)
                break

            if current.block.status != "SPLIT":  # if this is a complete block then it can move 4 directions
                add_move_astar(expanded_nodes, current.block.move_up(), cost_visited, heuristic_costs)
                add_move_astar(expanded_nodes, current.block.move_right(), cost_visited, heuristic_costs)
                add_move_astar(expanded_nodes, current.block.move_down(), cost_visited, heuristic_costs)
                add_move_astar(expanded_nodes, current.block.move_left(), cost_visited, heuristic_costs)

            # else:
            #     add_move(queue, current.split_move_up())
            #     add_move(queue, current.split_move_right())
            #     add_move(queue, current.split_move_down())
            #     add_move(queue, current.split_move_left())

            #     add_move(queue, current.split_move_up_other())
            #     add_move(queue, current.split_move_right_other())
            #     add_move(queue, current.split_move_down_other())
            #     add_move(queue, current.split_move_left_other())
            current = heappop(expanded_nodes)
            print(current.block.x)
            set_cost_visited((current.block.y,current.block.x), get_cost_visited((current.block.prev.y, current.block.prev.x),cost_visited) + 1, cost_visited)
        return solution