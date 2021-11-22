import pygame
import numpy as np

BLACK = (0,0,0)
WHITE = (255,255,255)

WIDTH = 20
HEIGHT = 20

WIN_HEIGHT=255
WIN_WIDTH =255

MARGIN = 5
SIZE = 10

grid = np.empty(SIZE*SIZE)

for i in range(SIZE*SIZE):
    if i < 50:
        grid[i] = 0
    else:
        grid[i] = 1
np.random.shuffle(grid)
grid = grid.reshape(SIZE,SIZE)



print(grid)
