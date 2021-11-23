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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.fitness = 0
        self.genome = str(np.random.randint(7, size=(243)))
        self.color = BLUE

    def move(self, gene, board):
        print(f"gene: {gene}, type: {type(gene)}")
        if gene == '0':
            if self.y - 1 > 0:
                self.y -= 1 
            else:
                self.fitness -= 5
        elif gene == '1':
            if self.y  + 1 < 10:
                self.y += 1 
            else:
                self.fitness -= 5
           
        elif gene == '2':
            if self.x -  1 > 0:
                self.x -= 1 
            else:
                self.fitness -= 5
        
        elif gene == '3':
            if self.x  + 1 < 10:
                self.x += 1 
            else:
                self.fitness -= 5

        elif gene == '4':
            pass # do nothing
        elif gene == '5':
            #pick up
            if board[self.x][self.y] == 1:
                 board[self.x][self.y] = 0
            else:
                self.fitness -= 1
        elif gene == '6':
            #move random direction
            self.move(np.random.randint(0,5), board)

    def find_move(self, board):
        # up * 3^0 + down * 3^1 + left *3^2 + right * 3^3 + cur * 3^4 = index of gene
        #empty = 0, can = 1, wall = 2
        #up:
        if self.y - 1 < 0:
            up = 2
        elif board[self.x][self.y - 1] == 1:
            up = 1
        else:
            up = 0
        #down:
        if self.y + 1 > 9:
            down = 2
        elif board[self.x][self.y + 1] == 1:
            down = 1
        else:
            down = 0
        #left:
        if self.x - 1 < 0:
            left = 2
        elif board[self.x - 1][self.y] == 1:
            left = 1
        else:
            left = 0
        #right:
        if self.y + 1 > 9:
            right = 2
        elif board[self.x + 1][self.y] == 1:
            right = 1
        else:
            right = 0
        #current, cant be a wall so we ignore:
        if board[self.x][self.y - 1] == 1:
            cur = 1
        else:
            cur = 0

        move = int(down * pow(3,0) + up * pow(3,1) + left * pow(3,2) + right * pow(3,3) + cur * pow(3,4))
        print(move)
        print(self.genome[move])
        return self.genome[move]

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x * (WIDTH + MARGIN) + MARGIN + self.size/2, 
                         self.y * (HEIGHT + MARGIN) + MARGIN + self.size/2, 
                         self.size, self.size))


def create_board(size):
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


board = create_board(SIZE)
print(board)
clock = pygame.time.Clock()
rob = Robby(5, 5)
print(rob.genome)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    rob.move(rob.find_move(board), board)
    draw(win, board, rob)
    clock.tick(1)
    

pygame.quit()
