import pygame
from game import Robby, Board, draw, WIN_HEIGHT, WIN_WIDTH


genome = "6 5 1 0 0 4 5 4 5 3 1 5 6 2 0 6 1 3 2 4 4 2 1 4 4 3 6 0 6 4 3 0 1 4 3 4 62 3 4 3 3 2 3 5 0 6 4 6 4 4 1 5 4 6 2 3 1 5 5 6 2 6 4 2 5 4 6 6 5 2 0 5 62 0 0 1 6 0 6 5 4 0 5 4 3 1 1 0 2 5 1 5 1 3 2 3 5 3 5 5 2 2 5 1 3 4 5 0 24 0 5 1 0 6 1 4 1 4 2 0 0 5 0 6 5 5 1 3 5 1 3 6 6 6 6 1 6 3 5 2 5 2 1 3 23 0 6 4 2 5 0 4 1 6 4 5 0 4 0 2 4 1 2 2 3 5 5 1 3 6 4 6 0 5 1 3 1 0 3 2 23 1 2 3 2 6 3 4 5 1 6 1 1 0 2 5 6 5 4 1 4 4 1 3 4 6 4 4 1 1 0 4 0 1 2 4 56 3 0 2 1 3 3 3 6 2 1 3 0 3 0 3 1 5 0 6 3".replace(' ','')
g = []
for i in genome:
    g.append(int(i))


test_board =[[1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0],]


board = Board(10)
print(board.grid)
rob = Robby(0,0, test_board)
rob.genome = [4 for _ in range(243)]
rob.genome[131] = 5
rob.genome[50] = 1
rob.genome[86] = 5
rob.genome[48] = 3
rob.genome[129] = 5


pygame.init()
WINDOW_SIZE = [WIN_WIDTH, WIN_HEIGHT + 100]
win = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Robby')
clock = pygame.time.Clock()



run = True
while run:
    clock.tick(.5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    if rob.moves > 0:
        rob.move(rob.find_move())
        draw(win, rob.board, rob)
    else:
        run = False

