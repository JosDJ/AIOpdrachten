import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]


def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0


def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]


def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value


def h(node, goal):
    h_value = (math.sqrt((goal[0] - node[0])**2 + (goal[1] - node[1])**2)) #pythagoras
    return h_value


def get_neighbors(node):
    neighbors = []
    x = node[0]
    y = node[1]
    # left
    if x-1 >= 0 and (x-1,y):
        neighbors.append( (x-1,y) )
    # right
    if x+1 < cf.SIZE and (x+1,y):
        neighbors.append( (x+1,y) )
    # top
    if y-1 >= 0 and (x,y-1):
        neighbors.append( (x,y-1) )
    # bottom
    if y+1 < cf.SIZE and (x,y+1):
        neighbors.append( (x,y+1) )
    return neighbors


def print_path(app, path):
    for p in range(len(path)-1):
        app.plot_line_segment(path[p][0], path[p][1], path[p+1][0], path[p+1][1], color=cf.FINAL_C)
        app.pause()



def search(app, start, goal):
    pq = PriorityQueue()
    pq.put(start,0)
    visited_nodes = [start]
    path = {start: [start]}
    g_score = {start:0}
    f_score = {start: h(start, goal)}

    while not pq.empty():
        current = pq.get()
        if current == goal:
            print_path(app, path[current])
            return path
        neighbors = get_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in g_score.keys():
                g_score[neighbor] = 999
            if neighbor not in f_score.keys():
                f_score[neighbor] = 999
            if get_grid_value(neighbor) != "b" and neighbor not in visited_nodes and g_score[neighbor] > g_score[current] + 1:
                g_score[neighbor] = g_score[current] + 1
                f_score[neighbor] = g_score[current] + h(neighbor, goal)

                pq.put(neighbor, f_score[neighbor])
                visited_nodes.append(neighbor)

                path[neighbor] = path[current].copy()
                path[neighbor].append(neighbor)

                app.plot_node(neighbor, color=cf.PATH_C)
                app.pause()

