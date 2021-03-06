from constant import *
import pygame
from queue import PriorityQueue
import math
import random

def h(pos1, pos2):
    '''heuristic function for a* algo'''
    x1, y1 = pos1
    x2, y2 = pos2
    x = abs(x1 - x2)
    y = abs(y1 - y2)
    return x + y

def get_pos_from_mouse(pos):
    '''return row, col from mouse coordinate'''
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

def is_valid_pos(row, col):
    '''check if row, col is valid'''
    if 0 <= row < ROWS and 0 <= col < COLS:
        return True
    return False


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x, self.y = self.get_coordinate()
        self.colour = WHITE
        self.neighbours = []
        self.prev = None
        self.wall_visited = False  # for generate maze
        self.g = 0
        self.f = 0

    def get_prev(self):
        return self.prev

    def get_g(self):
        return self.g

    def get_f(self):
        return self.f

    def is_visited(self):
        return self.colour == RED

    def is_wall_visited(self):
        return self.wall_visited

    def get_coordinate(self):
        '''return (x, y) coordinate of node in window'''
        x = SQUARE_SIZE * self.col
        y = SQUARE_SIZE * self.row
        return x, y

    def get_neighbours(self):
        return self.neighbours

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.colour = WHITE

    def is_start(self):
        return self.colour == ORANGE

    def is_end(self):
        return self.colour == PURPLE

    def is_open(self):
        '''check if node in open set'''
        return self.colour == GREEN

    def is_closed(self):
        return self.colour == RED

    def is_wall(self):
        return self.colour == BLACK

    def is_path(self):
        return self.colour == BLUE

    def set_prev(self, node):
        self.prev = node

    def set_wall_visited(self, visit):
        self.wall_visited = visit

    def set_g(self, new_g):
        self.g = new_g

    def set_f(self, new_f):
        self.f = new_f

    def set_start(self):
        self.colour = ORANGE

    def set_end(self):
        self.colour = PURPLE

    def set_open(self):
        self.colour = GREEN

    def set_closed(self):
        self.colour = RED

    def set_wall(self):
        self.colour = BLACK

    def set_path(self):
        self.colour = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))

    def __repr__(self):
        if self.colour == BLACK:
            return 'W'
        if self.colour == ORANGE:
            return 'S'
        if self.colour == PURPLE:
            return 'E'
        return '0'

    def get_unvisited_wall_neighbours(self, graph):
        '''return adjacent nodes that are walls'''
        neighbours = []

        # right
        if is_valid_pos(self.row + 2, self.col):
            node = graph[self.row + 2][self.col]
            if node.is_wall() and not node.is_wall_visited():
                neighbours.append(node)

        # left
        if is_valid_pos(self.row - 2, self.col):
            node = graph[self.row - 2][self.col]
            if node.is_wall() and not node.is_wall_visited():
                neighbours.append(node)

        # up
        if is_valid_pos(self.row, self.col + 2):
            node = graph[self.row][self.col + 2]
            if node.is_wall() and not node.is_wall_visited():
                neighbours.append(node)

        # down
        if is_valid_pos(self.row, self.col - 2):
            node = graph[self.row][self.col - 2]
            if node.is_wall() and not node.is_wall_visited():
                neighbours.append(node)

        return neighbours


    def update_neighbours(self, graph):
        ''' update value of neighbours with adjacent nodes'''

        # right
        if is_valid_pos(self.row + 1, self.col):
            node = graph[self.row + 1][self.col]
            if not node.is_wall():
                self.neighbours.append(node)

        # left
        if is_valid_pos(self.row - 1, self.col):
            node = graph[self.row - 1][self.col]
            if not node.is_wall():
                self.neighbours.append(node)

        # up
        if is_valid_pos(self.row, self.col + 1):
            node = graph[self.row][self.col + 1]
            if not node.is_wall():
                self.neighbours.append(node)

        # down
        if is_valid_pos(self.row, self.col - 1):
            node = graph[self.row][self.col - 1]
            if not node.is_wall():
                self.neighbours.append(node)


class Graph:
    def __init__(self, win):
        self.graph = self.create_graph()
        self.win = win
        self.start = None
        self.end = None
        self.algo_choice = 0  # set a* to default algorithm

    def get_node(self, row, col):
        return self.graph[row][col]

    def update(self):
        clock = pygame.time.Clock()
        self.draw_graph()
        clock.tick(FPS)
        pygame.display.update()

    def update_node_neighbours(self):
        for row in self.graph:
            for node in row:
                node.update_neighbours(self.graph)

    def create_graph(self):
        graph = []
        for row in range(ROWS):
            curr_row = []
            for col in range(COLS):
                node = Node(row, col)
                curr_row.append(node)
            graph.append(curr_row)
        return graph

    def reset_graph(self):
        self.start = None
        self.end = None
        self.graph = self.create_graph()


    def start_vis(self):
        if self.start and self.end:  # ensure that start & end node has been selected
            if self.algo_choice == 0:
                self.a_star()
            elif self.algo_choice == 1:
                self.dijsktra()
            elif self.algo_choice == 2:
                self.dfs() 
            elif self.algo_choice == 3:
                self.bfs()

    def left_click(self, mouse_coordinate):
        # edit graph
        if mouse_coordinate[1] < HEIGHT:
            row, col = get_pos_from_mouse(mouse_coordinate)
            node = self.get_node(row, col)

            if not self.start and node != self.end:
                node.set_start()
                self.start = node

            elif not self.end and node != self.start:
                node.set_end()
                self.end = node

            elif node != self.start and node != self.end:
                node.set_wall()

        # select algo choice
        else:
            x = mouse_coordinate[0]
            self.algo_choice = x // BOX_WIDTH


    def right_click(self, mouse_coordinate):
        row, col = get_pos_from_mouse(mouse_coordinate)
        node = self.get_node(row, col)
        node.reset()

        if node == self.start:
            self.start = None

        elif node == self.end:
            self.end = None


    def generate_maze(self):
        # http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
        # Recursive Backtracking (DFS)

        # 1) Set all nodes to wall
        for row in self.graph:
            for node in row:
                node.set_wall()

        # 2) Choose a starting point in the field
        start_row = random.randint(0, ROWS - 1)
        start_col = random.randint(0, COLS - 1)
        start_node = self.graph[start_row][start_col]

        # 3) Randomly choose a wall at that point and carve a passage through to the adjacent cell, 
        #    but only if the adjacent cell has not been visited yet. This becomes the new current cell.
        stack = [start_node]
        flag = False
        while len(stack) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            curr_node = stack[-1]
            curr_node.set_open()
            self.update()
            curr_node.reset()

            if curr_node == start_node and flag:
                self.update()
                break

            flag = True
            unvisisted_wall_neighbours = curr_node.get_unvisited_wall_neighbours(self.graph)

            # 4) If all adjacent cells have been visited, back up to the last cell that has uncarved walls and repeat.
            if len(unvisisted_wall_neighbours) == 0: 
                stack.pop()

            else:
                next_node = unvisisted_wall_neighbours[random.randint(0, len(unvisisted_wall_neighbours) - 1)]
                stack.append(next_node)
                curr_node.reset()

                # create path by removing wall b/w 2 nodes
                d_row = curr_node.row - next_node.row
                d_col = curr_node.col - next_node.col
                wall_row, wall_col = curr_node.row, curr_node.col

                if d_row > 0:
                    wall_row -= 1
                elif d_row < 0:
                    wall_row += 1

                if d_col > 0:
                    wall_col -= 1
                elif d_col < 0:
                    wall_col += 1

                wall_node = self.graph[wall_row][wall_col]
                wall_node.set_open()
                self.update()
                wall_node.reset()

        for row in self.graph:
            for node in row:
                if node.is_open():
                    node.reset()
                


    def a_star(self):
        '''visualise a* path finding algorithm on grid / graph'''
        self.update_node_neighbours()
        i = 0
        open_set = PriorityQueue()
        open_set.put((0, i, self.start))  # insert first / start node into open set
        open_set_list = {self.start}  # check if node in p queue as python p queue doens't have method to check

        for row in self.graph:
            for node in row:
                node.set_g(math.inf)
                node.set_f(math.inf)

        self.start.set_g(0)
        self.start.set_f(h(self.start.get_pos(), self.end.get_pos()))

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            curr_node = open_set.get()[2]
            open_set_list.remove(curr_node)

            # reach the end - create path
            if curr_node == self.end:
                self.display_path()
                return True


            for neighbour in curr_node.get_neighbours():
                temp_g_score = curr_node.get_g() + 1  # since all nodes are +1 away from prev visited node
                if temp_g_score < neighbour.get_g():
                    neighbour.set_prev(curr_node)
                    neighbour.set_g(temp_g_score)
                    neighbour.set_f(temp_g_score + h(neighbour.get_pos(), self.end.get_pos()))

                    if neighbour not in open_set_list:
                        i += 1
                        open_set.put((neighbour.get_f(), i, neighbour))
                        open_set_list.add(neighbour)
                        if neighbour != self.end:  # ensure that end node does not change colour (user can see end node)
                            neighbour.set_open()

            self.update()

            # update nodes that have been visited (except start & end node to retain original colour)
            if curr_node != self.start:
                curr_node.set_closed()

        return False

    
    def dijsktra(self):
        '''
        visualise dijkstra path finding algorithm on grid / graph
        similar to a*, however dijkstra does not consider f score
        '''
        self.update_node_neighbours()
        i = 0
        open_set = PriorityQueue()
        open_set.put((0, i, self.start))  # insert first / start node into open set
        open_set_list = {self.start}  # check if node in p queue as python p queue doens't have method to check

        for row in self.graph:
            for node in row:
                node.set_g(math.inf)

        self.start.set_g(0)

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            curr_node = open_set.get()[2]
            open_set_list.remove(curr_node)

            # reach the end - create path
            if curr_node == self.end:
                self.display_path()
                return True


            for neighbour in curr_node.get_neighbours():
                temp_g_score = curr_node.get_g() + 1  # since all nodes are +1 away from prev visited node
                if temp_g_score < neighbour.get_g():
                    neighbour.set_prev(curr_node)
                    neighbour.set_g(temp_g_score)

                    if neighbour not in open_set_list:
                        i += 1
                        open_set.put((neighbour.get_g(), i, neighbour))
                        open_set_list.add(neighbour)
                        if neighbour != self.end:  # ensure that end node does not change colour (user can see end node)
                            neighbour.set_open()

            self.update()

            # update nodes that have been visited (except start & end node to retain original colour)
            if curr_node != self.start:
                curr_node.set_closed()


    def dfs(self):
        ''' visualise dfs path finding algorithm '''
        self.update_node_neighbours()
        stack = [self.start]

        while len(stack) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            curr_node = stack.pop()
            if curr_node == self.end:
                self.display_path()
                return True

            if not curr_node.is_visited():
                if curr_node != self.start and curr_node != self.end:
                    curr_node.set_open()
                self.update()

            if curr_node != self.start and curr_node != self.end:
                curr_node.set_closed()

            for neighbour in curr_node.get_neighbours():
                if neighbour.get_prev() == None:
                    neighbour.set_prev(curr_node)

                if not neighbour.is_visited():
                    stack.append(neighbour)
                    if neighbour != self.start and neighbour != self.end:
                        neighbour.set_open()
                        self.update()


    def bfs(self):
        ''' 
        visualise bds path finding algortihm, 
        similar to dijkstra but bfs uses a queue instead of priority queue 
        '''
        self.update_node_neighbours()
        queue = [self.start]

        while len(queue) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            curr_node = queue.pop(0)
            for neighbour in curr_node.get_neighbours():
                if neighbour.get_prev() == None:
                    neighbour.set_prev(curr_node)

                if not neighbour.is_visited():
                    queue.append(neighbour)
                    if neighbour != self.start and neighbour != self.end:
                        neighbour.set_open()

                # found node, show path
                if neighbour == self.end:
                    self.update()
                    self.display_path()
                    return True

            self.update()

            if curr_node != self.start:
                curr_node.set_closed()

                
    def display_path(self):
        '''change selected node to blue colour to show path created by algorithm'''
        path = []
        curr_node = self.end
        while True:
            prev_node = curr_node.get_prev()
            if prev_node == self.start:
                break
            path.append(prev_node)
            curr_node = prev_node

        path.reverse()
        for node in path:
            node.set_path()
            pygame.display.update()


    def print_graph(self):
        print(self.graph)

    def draw_grid(self):
        '''draw horizontal & vertical line on board / checkerboard'''
        for y in range(0, HEIGHT + SQUARE_SIZE, SQUARE_SIZE):
            pygame.draw.line(self.win, GREY, (0, y), (WIDTH, y))

        for x in range(0, WIDTH, SQUARE_SIZE):
            pygame.draw.line(self.win, GREY, (x, 0), (x, HEIGHT))

    def draw_algo_choice(self):
        '''draw algorithm chocie at bottom'''

        # highlight algo choice
        x = self.algo_choice * BOX_WIDTH
        pygame.draw.rect(self.win, YELLOW, (x, HEIGHT, BOX_WIDTH, ALGO_CHOICE_HEIGHT))

        # draw line seperating algo choice
        for x in range(0, WIDTH, BOX_WIDTH):
            pygame.draw.line(self.win, GREY, (x, HEIGHT), (x, TOTAL_HEIGHT))

        # draw names of different algorithm
        algos = ['A*', 'Dijkstra', 'DFS', 'BFS']
        for i, algo in enumerate(algos):
            x = i * BOX_WIDTH
            center_x = x + (BOX_WIDTH // 2)
            center_y = HEIGHT + (ALGO_CHOICE_HEIGHT // 2)
            draw_center_text(algo, center_x, center_y, BLACK, self.win)

    def draw_nodes(self):
        for row in self.graph:
            for node in row:
                node.draw(self.win)

    def draw_graph(self):
        '''draw grid and nodes on window'''
        self.win.fill(WHITE)
        self.draw_nodes()
        self.draw_algo_choice()
        self.draw_grid()

