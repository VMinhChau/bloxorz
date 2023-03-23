import random
from functions import add_move_fitness, check_win
from math import sqrt
import copy
from block import Block
#  "up", "right", "down", "left" = [1,2,3,4]


class DNA:
    U = "up"
    R = "right"
    D = "down"
    L = "left"
    direction = [U, R, D, L]

    def __init__(self, no_of_moves):
        self.gene_length = no_of_moves
        self.genes = []
        self.fitness = 0.0
        self.done = False

        for i in range(no_of_moves):
            self.genes.append(random.choice(self.direction))

    def calculate_fitness(self, new_block, target):
        distance = sqrt((target[1][0] - new_block.x) ** 2 + (target[1][1] - new_block.y) ** 2)
        rate = 0.5
        blocked = 0
        open_space = 0  # Points for going into open spaces
        no_back_forth = 0  # Giving points for not going back and forth e.g DUDU...
        for i in range(len(self.genes) - 1):
            if self.genes[i] == self.U:
                new_block = new_block.move_up()
                if add_move_fitness(new_block):
                    open_space += 1
                    new_distance = sqrt((target[1][0] - new_block.x) ** 2 + (target[1][1] - new_block.y) ** 2)
                    self.fitness += (distance - new_distance) * rate
                else:
                    new_block = new_block.move_down()
                    blocked += 1
            elif self.genes[i] == self.R:
                new_block = new_block.move_right()
                if add_move_fitness(new_block):
                    open_space += 1
                    new_distance = sqrt((target[1][0] - new_block.x) ** 2 + (target[1][1] - new_block.y) ** 2)
                    self.fitness += (distance - new_distance) * rate
                else:
                    new_block = new_block.move_left()
                    blocked += 1
            elif self.genes[i] == self.D:
                new_block = new_block.move_down()
                if add_move_fitness(new_block):
                    open_space += 1
                    new_distance = sqrt((target[1][0] - new_block.x) ** 2 + (target[1][1] - new_block.y) ** 2)
                    self.fitness += (distance - new_distance) * rate
                else:
                    new_block = new_block.move_up()
                    blocked += 1
            else:
                new_block = new_block.move_left()
                if add_move_fitness(new_block):
                    open_space += 1
                    new_distance = sqrt((target[1][0] - new_block.x) ** 2 + (target[1][1] - new_block.y) ** 2)
                    self.fitness += (distance - new_distance) * rate
                else:
                    new_block = new_block.move_right()
                    blocked += 1
            if self.genes[i] != self.genes[i + 1]:
                if self.genes[i] in [self.U, self.D] and self.genes[i + 1] in [self.L, self.R]:
                    no_back_forth += 1
            if check_win(new_block):
                self.fitness += 10
                self.done = True
                return self.fitness

        self.fitness = open_space + no_back_forth - blocked
        return self.fitness

    def crossover(self, other_dna):
        child = DNA(self.gene_length)
        mid_point = random.randint(0, self.gene_length)

        for i in range(0, self.gene_length):
            if i < mid_point:
                child.genes[i] = other_dna.genes[i]
            else:
                child.genes[i] = self.genes[i]

        return child

    def mutate(self, rate):
        for i in range(self.gene_length):
            num = random.random()
            if num < rate:
                self.genes[i] = random.choice(self.direction)


class Population:
    def __init__(self, target, no_of_moves, mutation_rate, max_population):
        self.target = target
        self.mutation_rate = mutation_rate
        self.max_population = max_population
        self.generation = 0
        self.matingPool = []
        self.population = []
        self.finished = False
        self.got = None

        for i in range(max_population):
            self.population.append(DNA(no_of_moves))

    def calculate_fitness(self, new_block):
        for dna in self.population:
            dna.calculate_fitness(new_block, self.target)
            if dna.done:
                break

    def evaluate(self):
        for dna in self.population:
            # if check_win_dna(dna, new_block):
            #     self.finished = True
            #     self.got = dna
            #     break
            if dna.done:
                self.finished = True
                self.got = dna
                break

    def print_best_dna(self):
        max_fitness = 0
        best_dna = None
        for dna in self.population:
            if dna.fitness > max_fitness:
                max_fitness = dna.fitness
                best_dna = dna
        print(self.generation, "finess = ", max_fitness) #, best_dna.genes)

    def selection(self):
        self.matingPool = []
        max_fitness = 0
        for dna in self.population:
            if dna.fitness > max_fitness:
                max_fitness = dna.fitness
        fitness = 0
        for dna in self.population:
            if max_fitness != 0:
                fitness = dna.fitness / max_fitness
            n = int(round(fitness * 100))
            for i in range(n):
                self.matingPool.append(dna)

    def generate(self):
        if len(self.matingPool) != 0:
            for i in range(len(self.population)):
                a = random.randint(0, len(self.matingPool) - 1)
                b = random.randint(0, len(self.matingPool) - 1)
                dna_a = self.matingPool[a]
                dna_b = self.matingPool[b]

                new_dna = dna_a.crossover(dna_b)

                new_dna.mutate(self.mutation_rate)

                self.population[i] = new_dna

        self.generation += 1


def ga(block):
    start_x = block.x
    start_y = block.y
    g = [0, 0]
    for i, r in enumerate(block.game_map):
        if 'G' in r:
            g = [r.index('G'), i]
            break
    start_point = [start_x, start_y]
    target = [start_point, g]
    population_num = 50
    mutation_rate = 0.05
    no_of_moves = 20
    max_tries = 10000
    population = Population(target, no_of_moves, mutation_rate, population_num)
    while (not population.finished) and population.generation < max_tries:
        new_block = copy.copy(block)
        population.calculate_fitness(new_block)
        population.evaluate()
        population.print_best_dna()
        population.selection()
        population.generate()
    return population.got
