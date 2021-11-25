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
            self.move(np.random.randint(0, 4))
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

#breed given two robots returns two robots with crossover'd and mutated genomes
def breed(dad, mom):
    x = np.random.randint(162, size=(1))[0]
    child1 = Robby(0, 0, [])
    child2 = Robby(0, 0, [])
    child1.genome[:x] = dad.genome[:x]
    child1.genome[x:] = mom.genome[x:]
    child2.genome[:x] = mom.genome[:x]
    child2.genome[x:] = dad.genome[x:]
    # mutate
    child1 = mutate(child1)
    child2 = mutate(child2)
    return [child1, child2]

#mutates given robot genome.
#mutate chance of 0.01 = 1% chance to mutate
def mutate(robot):
    mutate_chance = 0.01
    for i in range(len(robot.genome)):
        if np.random.rand() < mutate_chance:
            robot.genome[i] = np.random.randint(7)
    return robot


def get_parents(robots):
 #Weighted Choice
    prob = [x.total_fitness for x in robots]
    #prob = [i for i in range(-50,50)]
    min_prob = min(min(prob), 0)
    #shift negative numbers
    shifted_prob = [i + abs(min_prob) for i in prob]
    #normalize
    sum_fit = sum(shifted_prob)
    norm_sum = [ float(i)/sum_fit for i  in shifted_prob]
    r = np.random.choice(robots, len(robots), p=norm_sum)
 #Random Chance, simpler parent selection
    # r = robots.copy()
    # np.random.shuffle(r)
    return r

#write writes stats to file and to terminal
def write(gen, highest_fit, avg_fit, genome):
    f = open("gen.txt", "a")
    f.write(f"Highest Fitness of gen {gen + 1} is {highest_fit}\n")
    f.write(f"Average Fitness is {avg_fit}\n")
    f.write(f"The best genome is :\n {genome}\n\n")
    print(f"Highest Fitness of gen {gen + 1} is {highest_fit}")
    print(f"Average Fitness is {avg_fit}")
    print(f"The best genome is :\n {genome}\n\n")


#draw, takes in pygame window, board, and robot
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
    #intialize population with random genes
    robots = [Robby(1, 1, []) for _ in range(population_size)]
    run = True
    f = open('gen.txt', "w")

    avg_fit = []
    highest_fit = []
    #run sim for generations
    for gen in range(generations):
        #generate random amount of boards
        boards = [Board(SIZE) for _ in range(cleaning_sessions)]
        for rob in robots:
            rob.total_fitness = 0
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
        #sort robots by total fitness,
        robots = sorted(robots, key=lambda x: x.total_fitness, reverse=True)
        
        #new_pop.append([np.array(r).ravel() for r in robots[:(int(len(robots)/2))]])
        avg_fit.append(sum([i.total_fitness for i in robots]) / len(robots))
        highest_fit.append(robots[0].total_fitness)

        write(gen, highest_fit[-1], avg_fit[-1], robots[0].genome)
        #get two lists of half the population size out of top 50% performing robots, the rest perish
        parents1 = get_parents(robots[:int(population_size/2)].copy())
        parents2 = get_parents(robots[:int(population_size/2)].copy())
    
        for i in range(int(population_size/2)):
            new_pop.append(breed(parents1[i], parents2[i]))
        new_pop = np.array(new_pop).ravel()
        #new_pop[175:] = robots[:25]
        robots = new_pop
    f.write(f"highest_fit: {highest_fit}")
    f.write(f"avg: {avg_fit}")
    f.close()

    pygame.quit()
    # breed(robots[0], robots[1])


