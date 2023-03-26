import global_variables
from math import sqrt, inf
from collections import namedtuple
from treenode import TreeNode
from heapq import heappush, heappop
from functions import process_state, check_win, solution_path,is_visited

class Astar:
     def __init__(self):
          self.cost_visited=dict()
     
     def distance_euclidean(self, pos1, pos2):
          return sqrt((pos1[1] - pos2[1]) ** 2 + (pos1[0] - pos2[0]) ** 2)
     
     def compute_heuristic_costs(self, block, target_pos):
          costs = dict()
          num = 0
          for y in range(len(block.game_map)):
               for x in range(len(block.game_map[0])):
                    pos = (x, y)
                    if not self.is_off_map(pos,block):
                         costs[num] = self.distance_euclidean(pos, target_pos)
                    else:
                         costs[num] = inf
                    num += 1
          return costs
     
     def min_h_cost(self, h_costs, node):
          if node.block.status == "STAND":
               index = node.block.y * global_variables.col + node.block.x
               value=h_costs[index]
               # print("Position: ", (node.block.x,node.block.y,node.block.status))
               # print("Index: ", index)
               # print("Hcost: ", value)
               return value

          if node.block.status  == "LIE_VERTICAL":
               index1 = node.block.y * global_variables.col + node.block.x
               index2 = (node.block.y + 1) * global_variables.col + node.block.x
               value=min(h_costs[index1], h_costs[index2])
               # print("Position: ", (node.block.x,node.block.y,node.block.status))
               # print("Hcost: ", value)
               return value

          if node.block.status  == "LIE_HORIZONTAL":
               index1 = node.block.y * global_variables.col + node.block.x
               index2 = node.block.y * global_variables.col + (node.block.x + 1)
               value=min(h_costs[index1], h_costs[index2])
               # print("Position: ", (node.block.x,node.block.y,node.block.status))
               # print("Hcost: ", value)
               return value
        
     def get_cost_visited(self, pos):
          # cost = namedtuple("cost", ['x', 'y', 'status'])
          # index = cost(x=pos[0], y=pos[1], status=pos[2])
          cost = namedtuple("cost", ['x', 'y', 'status','map'])
          index = cost(x=pos[0], y=pos[1], status=pos[2], map=pos[3])
          # print(index, cost_visited[index])
          return self.cost_visited[index]

     def set_cost_visited(self, pos, value: int):
          # cost = namedtuple("cost", ['x', 'y', 'status'])
          # index = cost(x=pos[0], y=pos[1], status=pos[2])
          cost = namedtuple("cost", ['x', 'y', 'status','map'])
          index = cost(x=pos[0], y=pos[1], status=pos[2], map=pos[3])
          self.cost_visited[index] = value

     def add_move_astar(self, expanded_nodes, block, heuristic_costs):
          if process_state(block):
               g_cost = self.get_cost_visited((block.prev.x,block.prev.y,block.prev.status,block.prev.map)) + 1
               heuristic_costs = self.compute_heuristic_costs(block, (global_variables.goal_x,global_variables.goal_y))
               if ((block.x,block.y,block.status,block.map) not in self.cost_visited) or g_cost < self.get_cost_visited((block.x,block.y,block.status,block.map)):
                    new_node = TreeNode(block)
                    h_cost = self.min_h_cost(heuristic_costs, new_node)
                    new_node.f_cost = g_cost + h_cost
                    heappush(expanded_nodes, new_node)
                    print((block.prev.x,block.prev.y,block.prev.status,block.prev.map))
                    print((block.x,block.y,block.status,block.map))
                    print(new_node.f_cost,g_cost,h_cost)
                    print("")
                    global_variables.previous.append(new_node.block)
                    return True
               else:
                    return None
          return False

     def is_off_map(self, pos,block):
          if pos[0] < 0 or pos[1] < 0 or pos[0] >= global_variables.col or pos[1] >= global_variables.row or block.game_map[pos[1]][pos[0]] == '.':
               return True
          else:
               return False
     
     def solve_by_astar(self, block):
          target_pos = (global_variables.goal_x,global_variables.goal_y)
        
          heuristic_costs = self.compute_heuristic_costs(block, target_pos)
          head = TreeNode(block)
          head.f_cost = self.min_h_cost(heuristic_costs, head)
        
          self.set_cost_visited((block.x,block.y,block.status,block.map), 0)
          expanded_nodes = list()
          current = head

          global_variables.previous = [head.block]
          solution = []
          
          while True:
               if check_win(current.block):
                    print("Success!\nFound solution after", current.block.id, "steps:")
                    solution = solution_path(current.block)
                    break

               if current.block.status != "SPLIT":  # if this is a complete block then it can move 4 directions
                    self.add_move_astar(expanded_nodes, current.block.move_left(), heuristic_costs)
                    self.add_move_astar(expanded_nodes, current.block.move_right(), heuristic_costs)
                    self.add_move_astar(expanded_nodes, current.block.move_up(), heuristic_costs)
                    self.add_move_astar(expanded_nodes, current.block.move_down(), heuristic_costs)

               else:
                    self.add_move_astar(expanded_nodes, current.block.split_move_up(), heuristic_costs)
                    self.add_move_astar(expanded_nodes, current.block.split_move_right(), heuristic_costs)
                    self.add_move_astar(expanded_nodes, current.block.split_move_down(), heuristic_costs)
                    self.add_move_astar(expanded_nodes, current.block.split_move_left(), heuristic_costs)
                    
                    self.add_move_astar(expanded_nodes, current.block.split_move_up_other(), heuristic_costs)
                    self.add_move_astar(expanded_nodes, current.block.split_move_right_other(), heuristic_costs)
                    self.add_move_astar(expanded_nodes, current.block.split_move_down_other(), heuristic_costs)
                    self.add_move_astar(expanded_nodes, current.block.split_move_left_other(), heuristic_costs)
               current = heappop(expanded_nodes)
               # self.set_cost_visited((current.block.x,current.block.y,current.block.status), self.get_cost_visited((current.block.prev.x, current.block.prev.y,current.block.prev.status)) + 1)
               self.set_cost_visited((current.block.x,current.block.y,current.block.status,current.block.map), self.get_cost_visited((current.block.prev.x, current.block.prev.y,current.block.prev.status,current.block.prev.map)) + 1)
          return solution
