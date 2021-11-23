import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 20
HEIGHT = 20
MARGIN = 1
SIZE = 10

WIN_HEIGHT = (HEIGHT + MARGIN) * SIZE
WIN_WIDTH = (WIDTH + MARGIN) * SIZE


class Robby:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.size = 10
        self.moves = 200
        self.board = board
        self.fitness = 0
        self.total_fitness = 0
        self.genome = np.random.randint(7, size=(243))
        self.color = BLUE

    def move(self, gene):
        if gene == 0:
            if self.y - 1 > 0:
                self.y -= 1 
            else:
                self.fitness -= 5
        elif gene == 1:
            if self.y  + 1 < 10:
                self.y += 1 
            else:
                self.fitness -= 5
           
        elif gene == 2:
            if self.x -  1 > 0:
                self.x -= 1 
            else:
                self.fitness -= 5
        
        elif gene == 3:
            if self.x  + 1 < 10:
                self.x += 1 
            else:
                self.fitness -= 5

        elif gene == 4:
            pass # do nothing
        elif gene == 5:
            #pick up
            if self.board[self.x][self.y] == 1:
                 self.board[self.x][self.y] = 0
            else:
                self.fitness -= 1
        elif gene == 6:
            #move random direction
            self.move(np.random.randint(0,5))
        self.moves -= 1

    def find_move(self):
        # up * 3^0 + down * 3^1 + left *3^2 + right * 3^3 + cur * 3^4 = index of gene
        #empty = 0, can = 1, wall = 2
        #up:
        if self.y - 1 < 0:
            up = 2
        elif self.board[self.x][self.y - 1] == 1:
            up = 1
        else:
            up = 0
        #down:
        if self.y + 1 > 9:
            down = 2
        elif self.board[self.x][self.y + 1] == 1:
            down = 1
        else:
            down = 0
        #left:
        if self.x - 1 < 0:
            left = 2
        elif self.board[self.x - 1][self.y] == 1:
            left = 1
        else:
            left = 0
        #right:
        if self.x + 1 > 9:
            right = 2
        elif self.board[self.x + 1][self.y] == 1:
            right = 1
        else:
            right = 0
        #current, cant be a wall so we ignore:
        if self.board[self.x][self.y - 1] == 1:
            cur = 1
        else:
            cur = 0

        move = int(down * pow(3,0) + up * pow(3,1) + left * pow(3,2) + right * pow(3,3) + cur * pow(3,4))
        return self.genome[move]

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x * (WIDTH + MARGIN) + MARGIN + self.size/2, 
                         self.y * (HEIGHT + MARGIN) + MARGIN + self.size/2, 
                         self.size, self.size))


class Board():

    def __init__(self, size):
        self.size = size
        self.grid = self.make_grid(self.size)
    def make_grid(self, size):
        grid = np.empty(size*size)
        # Create grid of square size and randomly place cans over board
        for i in range(size*size):
            if i < 50:
                grid[i] = 0
            else:
                grid[i] = 1
        np.random.shuffle(grid)
        grid = grid.reshape(size, size)
        return grid

def breed(dad, mom):
    x,y = np.sort(np.random.randint(243, size=(2)))
    child1 = Robby(0,0,[])
    child2 = Robby(0,0,[])
    dad_genome = dad.genome
    mom_genome = mom.genome
    child1.genome[:x] = dad_genome[:x] 
    child1.genome[x:y] = mom_genome[x:y] 
    child1.genome[y:] =  dad_genome[y:]
    child2.genome[:x] = mom_genome[:x] 
    child2.genome[x:y] = dad_genome[x:y] 
    child2.genome[y:] =  mom_genome[y:]
    #mutate
    mutate(child1)
    mutate(child2)
    return child1, child2

def mutate(robot):
    mutate_chance = 0.05
    for i in range(len(robot.genome)):
        if np.random.rand < mutate_chance:
            robot.genome[i] = np.random.randint(7)
    
def get_parents(robots):
    robots = sorted(robots, key=lambda x:x.total_fitness, reverse=True)
    prob = [x.total_fitness for x in robots[:100]]
    prob = [i + abs(min(prob)) for i in prob]
    s = sum(prob)
    prob = [i/s for i in prob]
    r=[]
    r = np.random.choice(robots,100,p=prob)
    r = sorted(r, key=lambda x:x.total_fitness, reverse=True)
    return r


def draw(win, board, rob):
    win.fill(BLACK)
    
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == 1:
                color = RED
            else:
                color = WHITE
            pygame.draw.rect(win, color, ((x * (WIDTH + MARGIN)) +MARGIN, 
                                        (y*(HEIGHT + MARGIN))+MARGIN, WIDTH, HEIGHT))
    rob.draw(win)
    pygame.display.update()


pygame.init()
WINDOW_SIZE = [WIN_WIDTH, WIN_HEIGHT]
win = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Robby')
run = True


clock = pygame.time.Clock()

population_size = 20
cleaning_sessions= 5
boards = [Board(SIZE) for _ in range(cleaning_sessions)]
robots = [Robby(0,0, []) for _ in range(population_size)]



for rob in robots:
    for board in boards:
        rob.board = board.grid
        rob.moves = 200
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            print(rob.moves)
            if rob.moves > 0:
                rob.move(rob.find_move())
                draw(win, board.grid, rob)
            else:
                run = False
        rob.total_fitness += rob.fitness
        rob.fitness = 0
    rob.total_fitness /= population_size
        
            # clock.tick(30)
                        
def get_parents(robots):
    robots = sorted(robots, key=lambda x:x.total_fitness, reverse=True)
    prob = [x.total_fitness for x in robots[:100]]
    prob = [i + abs(min(prob)) for i in prob]
    s = sum(prob)
    prob = [i/s for i in prob]
    r=[]
    r = np.random.choice(robots,100,p=prob)
    r = sorted(r, key=lambda x:x.total_fitness, reverse=True)
    return r


# breed(robots[0], robots[1])

pygame.quit()
