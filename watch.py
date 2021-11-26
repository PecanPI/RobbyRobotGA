import pygame
import collections
from pygame.locals import *
from game import Robby, Board, draw, breed, get_parents, WIN_HEIGHT, WIN_WIDTH


# genome that only cleans the outside of the board
# circle_genome = " 1 5 2 0 6 2 3 3 4 3 5 2 3 3 2 4 0 0 1 5 1 1 1 1 3 0 5 1 2 4 3 4 3 3 3 6 14 6 6 4 5 1 2 5 1 3 1 1 2 1 3 3 4 0 0 2 1 3 4 0 0 3 0 0 2 5 5 3 1 4 5 6 14 1 0 6 2 6 1 4 4 5 1 6 5 5 5 3 4 1 5 3 6 5 4 5 6 5 3 5 5 3 5 5 0 3 3 5 02 4 3 5 5 0 0 4 3 0 2 3 3 1 0 5 6 5 5 1 5 5 1 4 5 5 5 1 4 4 5 5 4 5 5 5 45 2 5 0 2 1 1 0 1 4 5 3 5 5 0 1 5 4 2 4 2 3 3 0 4 0 3 4 2 0 5 6 4 5 2 0 32 5 5 2 5 1 2 1 4 5 3 1 5 2 2 2 2 4 5 1 4 5 2 4 6 6 4 0 2 2 4 1 0 6 5 4 43 0 0 4 1 6 0 3 0 3 2 5 3 1 2 3 1 4 2 6 0".replace(' ','')

genome = "6 0 3 1 1 1 0 0 0 2 0 2 2 1 3 0 2 5 3 0 3 1 3 1 5 6 0 3 0 3 1 0 1 3 5 1 22 2 2 3 2 3 3 1 6 0 3 1 4 3 3 3 0 2 2 1 1 1 1 0 0 1 1 5 1 2 2 3 0 5 1 3 51 3 2 6 4 3 2 5 5 5 5 0 5 5 5 1 5 0 2 5 0 2 2 4 2 5 0 5 5 0 5 3 0 3 5 5 55 0 5 5 0 6 5 0 5 5 5 2 2 0 3 3 6 5 3 0 5 5 5 6 5 0 5 5 5 5 5 5 5 2 2 1 25 6 6 0 1 4 5 6 5 1 1 2 4 0 1 5 0 5 6 4 2 3 6 5 4 4 2 0 5 4 3 6 5 6 0 1 44 4 1 1 3 2 5 4 1 6 3 5 1 6 1 1 1 0 4 6 1 2 4 4 0 3 4 3 2 5 3 1 2 3 0 5 43 3 1 3 6 1 4 6 5 1 5 2 1 6 0 2 3 2 0 5 4".replace(' ','')
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

parent1 = Robby(0,0, test_board)
parent2  =Robby(0,0, test_board)
child1, child2  =breed(parent1, parent2)

board = Board(10)
# print(board.grid)
rob = Robby(0,0, board.grid)
rob.genome = g

# Test get parents
# robots = [i for i in range(-50, 50)]
# print(collections.Counter(get_parents(robots)))

#Test breed
# moms = [Robby(0,0,[]) for _ in range(5)]
# for mom in moms:
#     mom.genome = [4 for i in range(243)]
# dads = [Robby(0,0,[]) for _ in range(5)]
# for dad in dads:
#     dad.genome = [5 for i in range(243)]

# for mom, dad in zip(moms,dads):
#     child1, child2 = breed(mom, dad)
#     print(child1.genome, child2.genome, "\n")

pygame.init()
WINDOW_SIZE = [WIN_WIDTH, WIN_HEIGHT + 100]
win = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Robby')
clock = pygame.time.Clock()



run = True
start = False
while run:
    clock.tick(5)
    draw(win, rob.board, rob)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_SPACE:
                start=True
        #     if event.key == pygame.K_t:
        #         rob.move(4)
        #     if event.key == pygame.K_RIGHT:
        #         rob.move(3)
        #     if event.key == pygame.K_LEFT:
        #         rob.move(2)
        #     if event.key == pygame.K_DOWN:
        #         rob.move(1)
        #     if event.key == pygame.K_UP:
        #         rob.move(0)
        #     if event.key == pygame.K_r:
        #         rob.move(6)
    if rob.moves > 0 and start:
        rob.move(rob.find_move())
        #draw(win, rob.board, rob)
    else:
        pass

