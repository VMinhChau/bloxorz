from block import Block
import global_variables
from functions import check_win, add_move, solution_path
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

# def solve_by_astar(block):
#         target_pos = (global_variables.goal_x,global_variables.goal_y)
        
#         heuristic_costs = compute_heuristic_costs(block, target_pos)
#         head = TreeNode(block)
#         head.f_cost = min_h_cost(heuristic_costs, head)
        
#         cost_visited = dict()
#         set_cost_visited((block.x,block.y,block.status), 0, cost_visited)

#         expanded_nodes = list()
#         current = head

#         global_variables.previous = [head.block]
#         solution = []
       
#         while True:
#             if check_win(current.block):
#                 print("Success!\nFound solution after", current.block.id, "steps:")
#                 solution = solution_path(current.block)
#                 break

#             if current.block.status != "SPLIT":  # if this is a complete block then it can move 4 directions
#                 add_move_astar(expanded_nodes, current.block.move_up(), cost_visited, heuristic_costs)
#                 add_move_astar(expanded_nodes, current.block.move_right(), cost_visited, heuristic_costs)
#                 add_move_astar(expanded_nodes, current.block.move_down(), cost_visited, heuristic_costs)
#                 add_move_astar(expanded_nodes, current.block.move_left(), cost_visited, heuristic_costs)

#             else:
#                 add_move_astar(expanded_nodes, current.block.split_move_up(), cost_visited, heuristic_costs)
#                 add_move_astar(expanded_nodes, current.block.split_move_right(), cost_visited, heuristic_costs)
#                 add_move_astar(expanded_nodes, current.block.split_move_down(), cost_visited, heuristic_costs)
#                 add_move_astar(expanded_nodes, current.block.split_move_left(), cost_visited, heuristic_costs)
                
#                 add_move_astar(expanded_nodes, current.block.split_move_up_other(), cost_visited, heuristic_costs)
#                 add_move_astar(expanded_nodes, current.block.split_move_right_other(), cost_visited, heuristic_costs)
#                 add_move_astar(expanded_nodes, current.block.split_move_down_other(), cost_visited, heuristic_costs)
#                 add_move_astar(expanded_nodes, current.block.split_move_left_other(), cost_visited, heuristic_costs)
#             current = heappop(expanded_nodes)
#             set_cost_visited((current.block.x,current.block.y,current.block.status), get_cost_visited((current.block.prev.x, current.block.prev.y,current.block.prev.status),cost_visited) + 1, cost_visited)
#         return solution