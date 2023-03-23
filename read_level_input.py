import json
def read_file(path):
    with open(path) as f:
        #  =====================  get level infomation =============
        first_line = f.readline()
        row, col, start_x, start_y = [int(x) for x in first_line.split()]
        #  ================= get level map =============
        game_map = []
        for i in range(row):
            map_line = f.readline().strip()
            list_map_line = map_line.split()
            game_map.append(list_map_line)
        #   =============== get level objects ==================
        number_of_object = int(f.readline())
        objects = []
        for i in range(number_of_object):
            lines = ""
            for k in range(5):
                line = f.readline().strip()
                lines += line
            obj = json.loads(lines)
            objects.append(obj)
        for x,line in enumerate(game_map):
            for y,char in enumerate(line):
                if (char=='G'):
                    goal_x=y
                    goal_y=x
        return row, col, start_x, start_y, game_map, objects, goal_x, goal_y
