import global_variables
from read_level_input import read_file
from block import Block
from algorithm import BFS
import time


def test():
    cnt_success = 0
    for level in range(1,34):
        path = './levels/lvl' + str(level) + '.txt'
        global_variables.init()
        global_variables.row, global_variables.col, global_variables.start_x, \
            global_variables.start_y, game_map, global_variables.objects = read_file(path)
        block = Block(global_variables.start_x, global_variables.start_y, "STAND", None, game_map)
        start_time = time.time()
        print("Testing level", level, " ..........")
        solution = BFS(block)
        if solution:
            cnt_success += 1
            # with open('test_result.txt', 'a') as f:
            #     print('success\n''Level ', str(level), ":     \
            #     Found solution in    ", round(time.time() - start_time, 9), '("s")', file=f)
            print("Level ", str(level), ":     Found solution in    ", round(time.time() - start_time, 9), ("s"))
        else:
            print("Failed to find solution :( ")
        print("===========================================")
    print(cnt_success ,"/33 level success")