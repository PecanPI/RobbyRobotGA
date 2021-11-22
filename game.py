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
        self.gene = str(np.random.randint(7, size=(243)))
        self.color = BLUE

    def move(self, gene, board):
        if gene == 0:
            self.y -= 1 #up
        elif gene == 1:
            self.y += 1 #down
        elif gene == 2:
            self.x -= 1 #left
        elif gene == 3:
            self.x += 1 #right
        elif gene == 4:
            pass # do nothing
        elif gene == 5:
            #pick up
            if board[self.x][self.y] == 1:
                 board[self.x][self.y] = 0
        elif gene == 6:
            #move random direvtion
            self.move(np.random.randint(0,5), board)


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
print(rob.gene)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    rob.move(np.random.randint(0,7), board)
    draw(win, board, rob)
    clock.tick(1)
    

pygame.quit()
