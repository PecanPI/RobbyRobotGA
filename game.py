import pygame
import numpy as np
import matplotlib.pyplot as plt

pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

STAT_FONT = pygame.font.SysFont("comicsans", 20)

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
            if self.y - 1 >= 0:
                self.y -= 1
            else:
                self.fitness -= 5
        elif gene == 1:
            if self.y + 1 < 10:
                self.y += 1
            else:
                self.fitness -= 5

        elif gene == 2:
            if self.x - 1 >= 0:
                self.x -= 1
            else:
                self.fitness -= 5

        elif gene == 3:
            if self.x + 1 < 10:
                self.x += 1
            else:
                self.fitness -= 5

        elif gene == 4:
            pass
        elif gene == 5:
            # pick up
            if self.board[self.y][self.x] == 1:
                self.board[self.y][self.x] = 0
                self.fitness += 10
            else:
                self.fitness -= 1
        elif gene == 6:
            # move random direction
            self.moves += 1
            self.move(np.random.randint(0, 5))
        self.moves -= 1

    def find_move(self):
        # up * 3^0 + down * 3^1 + left *3^2 + right * 3^3 + cur * 3^4 = index of gene
        # empty = 0, can = 1, wall = 2
        # up:
        if self.y - 1 < 0:
            up = 2
        elif self.board[self.y - 1][self.x] == 1:
            up = 1
        else:
            up = 0
        # down:
        if self.y + 1 > 9:
            down = 2
        elif self.board[self.y + 1][self.x] == 1:
            down = 1
        else:
            down = 0
        # left:
        if self.x - 1 < 0:
            left = 2
        elif self.board[self.y][self.x - 1] == 1:
            left = 1
        else:
            left = 0
        # right:
        if self.x + 1 > 9:
            right = 2
        elif self.board[self.y][self.x + 1] == 1:
            right = 1
        else:
            right = 0
        # current, cant be a wall so we ignore:
        if self.board[self.y][self.x] == 1:
            cur = 1
        else:
            cur = 0
        
        move = int(up * pow(3, 0) + down * pow(3, 1) + left *
                   pow(3, 2) + right * pow(3, 3) + cur * pow(3, 4))
        #print(move)
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
        grid = grid.reshape(size, size).astype(int)
        return grid


def breed(dad, mom):
    x = np.sort(np.random.randint(162, size=(1)))
    child1 = Robby(0, 0, [])
    child2 = Robby(0, 0, [])
    dad_genome = dad.genome
    mom_genome = mom.genome
    child1.genome[:x] = dad_genome[:x]
    child1.genome[x:] = mom_genome[x:]
    child2.genome[:x] = mom_genome[:x]
    child2.genome[x:] = dad_genome[x:]
    # mutate
    child1 = mutate(child1)
    child2 = mutate(child2)
    return [child1, child2]


def mutate(robot):
    mutate_chance = 0.05
    for i in range(len(robot.genome)):
        if np.random.rand() < mutate_chance:
            robot.genome[i] = np.random.randint(7)
    return robot


def get_parents(robots):
 #Weighted Choice
        # prob = [x.total_fitness for x in robots[:len(robots)]]
        # prob = [i + abs(min(prob)) for i in prob]
        # s = sum(prob)
        # prob = [i/s for i in prob]
        # r = []
        # r = np.random.choice(robots, len(robots), p=prob)
    r = robots.copy()
    np.random.shuffle(r)
    return r


def draw(win, board, rob):
    win.fill(BLACK)

    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == 1:
                color = RED
            else:
                color = WHITE
            pygame.draw.rect(win, color, ((y * (WIDTH + MARGIN)) + MARGIN,
                                          (x*(HEIGHT + MARGIN))+MARGIN, WIDTH, HEIGHT))
    rob.draw(win)
    text = STAT_FONT.render("fitness: "+str(rob.fitness), 1, (255, 255, 255))
    win.blit(text, (10,WIN_HEIGHT-5  ))
    text = STAT_FONT.render("moves left: "+str(rob.moves), 1, (255, 255, 255))
    win.blit(text, (10,WIN_HEIGHT+20  ))
    text = STAT_FONT.render("move: "+str(rob.find_move()), 1, (255, 255, 255))
    win.blit(text, (10,WIN_HEIGHT+40  ))
    text = STAT_FONT.render("total fitness: "+str(rob.total_fitness), 1, (255, 255, 255))
    win.blit(text, (10,WIN_HEIGHT+60  ))

    pygame.display.update()

if __name__ == "__main__":
    generations = 1000
    population_size = 200  # must be even
    cleaning_sessions = 100
    
    robots = [Robby(1, 1, []) for _ in range(population_size)]
    run = True

    f = open('gen.txt', "x")
    f.close()
    avg_fit = []
    highest_fit = []

    # pygame.init()
    # WINDOW_SIZE = [WIN_WIDTH, WIN_HEIGHT + 100]
    # win = pygame.display.set_mode(WINDOW_SIZE)
    # pygame.display.set_caption('Robby')

    # clock = pygame.time.Clock()

    for gen in range(generations):
        boards = [Board(SIZE) for _ in range(cleaning_sessions)]
        for rob in robots:
            for board in boards:
                rob.board = board.grid.copy()
                rob.x, rob.y = 0,0
                rob.fitness = 0
                rob.moves = 200
                #
                run = True
                while run:
                    if rob.moves > 0:
                        rob.move(rob.find_move())
                    else:
                        run = False
                rob.total_fitness += rob.fitness
            rob.total_fitness /= cleaning_sessions

        new_pop = []

        robots = sorted(robots, key=lambda x: x.total_fitness, reverse=True)
        avg_fit.append(sum([i.total_fitness for i in robots]) / len(robots))
        highest_fit.append(robots[0].total_fitness)
        f = open("gen.txt", "a")
        f.write(f"Highest Fitness of gen {gen + 1} is {highest_fit[-1]}\n")
        f.write(f"Average Fitness is {avg_fit[-1]}\n")
        f.write(f"The best genome is :\n {robots[0].genome}\n\n")
        f.close()
        print(f"Highest Fitness of gen {gen + 1} is {highest_fit[-1]}")
        print(f"Average Fitness is {avg_fit[-1]}")
        print(f"The best genome is :\n {robots[0].genome}\n\n")
        
        parents = get_parents(robots[:int(population_size/2)].copy())
    

        for i in range(int(population_size/2)):
            new_pop.append(breed(robots[i], parents[i]))
        robots = np.array(new_pop).ravel()
        
    f.open("gen.txt", 'a')
    f.write(f"highest_fit: {highest_fit}")
    f.write(f"avg: {avg_fit}")



    pygame.quit()
    # breed(robots[0], robots[1])


