import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WIDTH = 20
HEIGHT = 20
MARGIN = 1
SIZE = 10

WIN_HEIGHT = (HEIGHT + MARGIN) * SIZE
WIN_WIDTH = (WIDTH + MARGIN) * SIZE


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


def draw(win, board):
    win.fill(BLACK)
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == 1:
                color = RED
            else:
                color = WHITE
            pygame.draw.rect(win, color, ((x * (WIDTH + MARGIN)) +
                             MARGIN, (y*(HEIGHT + MARGIN))+MARGIN, WIDTH, HEIGHT))
    pygame.display.update()


pygame.init()
WINDOW_SIZE = [WIN_WIDTH, WIN_HEIGHT]
win = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Robby')
run = True


board = create_board(SIZE)
print(board)
clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw(win, board)
    clock.tick(1)


pygame.quit()
