from collections import defaultdict
from collections import deque
import numpy as np

"""
# check the position
def isin(x, y, board):
    if 0 <= x <= len(board) - 1 and 0 <= y <= len(board[0]) - 1:
        return True
    else:
        return False
"""


# Find neighbors in 4 directions
def neighbors(path_list, x):
    r = x[0]
    c = x[1]
    nbs = []
    # ensure neighbors are within image boundaries
    if (r - 1, c) in path_list:
        nbs.append((r - 1, c))
    if (r, c - 1) in path_list:
        nbs.append((r, c - 1))
    if (r, c + 1) in path_list:
        nbs.append((r, c + 1))
    if (r + 1, c) in path_list:
        nbs.append((r + 1, c))
    return nbs


def random(space, init, goal):
    import random
    open = []
    closed = []
    expanded = []
    prev = {}
    open.append(init)
    print("Opened node: ", init)
    expanded.append(init)
    print("Expanded node: ", init)
    while len(open) != 0:
        x = random.choice(open)
        if x == goal:
            path = reconstruct_path(prev, x)
            print("Reach the goal.")
            break
        expanded.append(x)  # expanded node
        print("Expanded node: ", x)
        for y in neighbors(space, x):
            if y not in open and y not in closed:
                open.append(y)
                print("Opened node: ", y)
                prev[y] = x
        open.remove(x)
        closed.append(x)
        print("Closed node: ", x)
    return path, open, len(expanded)


def BFS(source, init, goal):
    open = []
    closed = []
    prev = {}
    expanded = []
    open.append(init)
    print("Opened node: ", init)
    expanded.append(init)
    print("Expanded node: ", init)
    while len(open) != 0:
        x = open[0]
        open.pop(0)  # from the front
        if x == goal:
            path = reconstruct_path(prev, x)
            print("Reach the goal.")
            break
        expanded.append(x)
        print("Expanded node: ", x)
        for y in neighbors(source, x):
            if y not in open and y not in closed:
                open.append(y)
                print("Opened node: ", y)
                prev[y] = x
        closed.append(x)
        print("Closed node: ", x)
    return path, open, len(expanded)


def DFS(source, init, goal):
    open = []  # stack
    closed = []
    prev = {}
    expanded = []
    open.append(init)
    print("Opened node: ", init)
    expanded.append(init)
    print("Expanded node: ", init)
    while len(open) != 0:
        x = open[-1]

        print("Expanded node: ", x)
        if x == goal:
            path = reconstruct_path(prev, x)
            print("Reach the goal.")
            break
        open.pop()  # delete from the last one
        expanded.append(x)  # expanded node
        for y in neighbors(source, x):
            if y not in open and y not in closed:
                open.append(y)
                print("Opened node: ", y)
                prev[y] = x
        closed.append(x)
        print("Closed node: ", x)
    return path, open, len(expanded)


'''
def dijkstra(source, init, goal):
    from queue import PriorityQueue
    inf = float('inf')
    Q = PriorityQueue()
    dist = {}
    prev = {}
    expanded = []
    expanded.append(init)
    source.remove(init)
    for s in source:
        Q.put((inf, s))
        dist[s] = inf
        prev[s] = None
    Q.put((0, init))
    dist[init] = 0
    while Q.not_empty:
        x = Q.get()[1]  # dequeue
        expanded.append(x)
        if x == goal:
            path = reconstruct_path(prev, x)
            break
        for y in neighbors(maze, x):
            tmp = dist[x] + 1
            if tmp < dist[y]:
                dist[y] = tmp
                prev[y] = x
    return path, open, len(expanded)
'''


def heuristic(s, init):
    return abs(s[0] - init[0]) + abs(s[1] - init[1])


def greedy(source, init, goal):
    from queue import PriorityQueue
    open = PriorityQueue()
    closed = []
    prev = {}
    expanded = []
    expanded.append(init)
    source.remove(init)
    open.put((heuristic(init, goal), init))
    opened = [init]
    print("Opened node: ", init)
    print("Expanded node: ", init)
    while open.not_empty:
        x = open.get()[1]  # dequeue

        if x == goal:
            print("Reach the goal.")
            path = reconstruct_path(prev, x)
            break
        expanded.append(x)
        print("Expanded node: ", x)
        for y in neighbors(source, x):
            h_y = heuristic(y, goal)
            if (h_y, y) not in open.queue and y not in closed:
                open.put((h_y, y))
                opened.append(y)
                print("Opened node: ", y)
                prev[y] = x
        closed.append(x)
        print("Closed node: ", x)
    return path, opened, len(expanded)


def a_star(source, init, goal):
    from queue import PriorityQueue
    open = PriorityQueue()
    dist = {}
    closed = []
    prev = {}
    expanded = []
    expanded.append(init)
    open.put((heuristic(init, goal), init))
    dist[init] = 0
    prev[init] = None
    opened = [init]
    print("Opened node: ", init)
    print("Expanded node: ", init)
    while open.not_empty:
        x = open.get()[1]
        if x == goal:
            print("Reach the goal.")
            path = reconstruct_path(prev, x)
            if init in path:
                path.remove(init)
            break
        expanded.append(x)
        print("Expanded node: ", x)
        for y in [a for a in neighbors(source, x) if a not in closed]:  # neighbors(source, x) - closed:
            d_prime = dist[x] + 1
            h_y = heuristic(y, goal)
            if (h_y, y) not in open.queue or d_prime < dist[y]:
                dist[y] = d_prime
                prev[y] = x
                if (h_y, y) not in open.queue:
                    open.put((d_prime + h_y, y))
                    opened.append(y)
                    print("Opened node: ", y)
                else:
                    open.get((h_y, y))
                    open.put((d_prime + h_y, y))
                    opened.append(y)
                    print("Opened node: ", y)
        closed.append(x)
        print("Closed node: ", x)
    return path, opened, len(expanded)


def reconstruct_path(prev, goal):
    x = goal
    path = []
    while x in prev.keys():
        path.append(x)
        x = prev[x]
    return path


# Choose a method
def search_method(option, path, start_point, end_point):
    if option == "1":
        return random(path, (start_point[1], start_point[0]), (end_point[1], end_point[0]))
    elif option == "2":
        return DFS(path, (start_point[1], start_point[0]), (end_point[1], end_point[0]))
    elif option == "3":
        return BFS(path, (start_point[1], start_point[0]), (end_point[1], end_point[0]))
    elif option == "4":
        return greedy(path, (start_point[1], start_point[0]), (end_point[1], end_point[0]))
    elif option == "5":
        return a_star(path, (start_point[1], start_point[0]), (end_point[1], end_point[0]))




file = "dataset/4.txt"

if __name__ == '__main__':
    # Open the file
    f = open(file, 'r')
    lines = f.readlines()
    new_lines = [line.strip('\n') for line in lines]
    maze = new_lines[:-2]
    # print(maze)
    # enumerate()
    path = [(i, j) for i, sublist in enumerate(maze) for j, x in enumerate(sublist) if x == " "]
    # print(path)
    start = new_lines[-2].replace('start', '')
    end = new_lines[-1].replace('end', '')
    start_point = list(map(int, start.split(', ')))
    end_point = list(map(int, end.split(', ')))
    print('from', start_point)
    print('to', end_point)
    # Close the file
    f.close()
    valid_options = ['1', '2', '3', '4', '5']
    content = "Please choose a method by number:\n1. Random Search\n2. Depth Search (DFS)\n3. Width Search (BFS)\n" \
              "4. Greedy Search\n5. A * algorithm\n"
    option = input(content)
    while option not in valid_options:
        print('Invalid option. Please try again.')
        option = input(content)
    path, opened, expanded_num = search_method(option, path, start_point, end_point)
    # path, opened, expanded_num = random(path, (start_point[1], start_point[0]), (end_point[1], end_point[0]))
    # Print
    maze = [list(row) for row in maze]
    for i in opened:
        maze[i[0]][i[1]] = '#'
    for point in path:
        x = point[0]
        y = point[1]
        maze[x][y] = 'O'
    maze[start_point[1]][start_point[0]] = 'S'
    maze[end_point[1]][end_point[0]] = 'E'
    for i in range(len(maze)):
        print(''.join(maze[i]))
    print("--------------\nS Start\nE End\n# Opened node\no Path\nX Wall\nspace Fresh node\n--------------")
    print('Nodes expanded:', expanded_num)
    print('Path length:', len(path))
