import operator
from random import random, randint
from numpy import sin, mean, std, array
from matplotlib import pyplot

DEPTH_MAX = 5
terminals = ['Cement', 'Slag', 'Fly ash', 'Water', 'SP', 'Coarse Aggr', 'Fine Aggr', 'Slump', 'Flow']
functions = ['+', '-', '*', 'sin']
noFunctions = 4


class Chromosome:
    def __init__(self, d=DEPTH_MAX):
        self.max_depth = d
        self.representation = [0 for _ in range(2 ** (self.max_depth + 1) - 1)]
        self.fitness = 0
        self.size = 0

    def __str__(self):
        return str(self.representation)

    def grow_expression(self, pos=0, depth=0):
        """
        initialise randomly an expression
        """
        if (pos == 0) or (depth < self.max_depth):
            if random() < 0.5:
                self.representation[pos] = randint(1, len(terminals))
                self.size = pos + 1
                return pos + 1
            else:
                self.representation[pos] = -randint(1, noFunctions)
                final_first_child = self.grow_expression(pos + 1, depth + 1)
                final_second_child = self.grow_expression(final_first_child, depth + 1)
                return final_second_child
        else:
            # choose a terminal
            self.representation[pos] = randint(1, len(terminals))
            self.size = pos + 1
            return pos + 1

    def evaluate_expression(self, pos, current_data):
        """
        the expresion value for some specific terminals
        """
        if self.representation[pos] > 0:  # a terminal
            return current_data[self.representation[pos] - 1], pos
        elif self.representation[pos] < 0:  # a function
            if functions[-self.representation[pos] - 1] == '+':
                aux_first = self.evaluate_expression(pos + 1, current_data)
                aux_second = self.evaluate_expression(aux_first[1] + 1, current_data)
                return aux_first[0] + aux_second[0], aux_second[1]
            elif functions[-1 - self.representation[pos]] == '-':
                aux_first = self.evaluate_expression(pos + 1, current_data)
                aux_second = self.evaluate_expression(aux_first[1] + 1, current_data)
                return aux_first[0] - aux_second[0], aux_second[1]
            elif functions[-1 - self.representation[pos]] == '*':
                aux_first = self.evaluate_expression(pos + 1, current_data)
                aux_second = self.evaluate_expression(aux_first[1] + 1, current_data)
                return aux_first[0] * aux_second[0], aux_second[1]
            elif functions[-1 - self.representation[pos]] == 'sin':
                aux_first = self.evaluate_expression(pos + 1, current_data)
                return sin(aux_first[0]), aux_first[1]

    def compute_fitness(self, current_data, current_out, no_examples):
        """
        the fitness function
        """
        err = 0.0
        for d in range(no_examples):
            err += current_out[d] - self.evaluate_expression(0, current_data[d])[0]
        self.fitness = err

    def traverse(self, pos):
        """
        returns the next index where it begins the next
        branch in the tree from the same level
        """
        if self.representation[pos] > 0:  # terminal
            return pos + 1
        else:
            return self.traverse(self.traverse(pos + 1))


def crossover(parent1, parent2):
    off = Chromosome()
    while True:
        start_parent1 = randint(0, parent1.size - 1)
        end_parent1 = parent1.traverse(start_parent1)
        start_parent2 = randint(0, parent2.size - 1)
        end_parent2 = parent2.traverse(start_parent2)
        if len(off.representation) > end_parent1 + (end_parent2 - start_parent2 - 1) + (parent1.size - end_parent1 - 1):
            break
    index = -1
    for index in range(start_parent1):
        off.representation[index] = parent1.representation[index]
    for j in range(start_parent2, end_parent2):
        index = index + 1
        off.representation[index] = parent2.representation[j]
    for j in range(end_parent1, parent1.size):
        index = index + 1
        off.representation[index] = parent1.representation[j]
    off.size = index + 1
    return off


def mutation(c):
    off = Chromosome()
    pos = randint(0, c.size - 1)
    off.representation = c.representation[:]
    off.size = c.size
    if off.representation[pos] > 0:  # terminal
        off.representation[pos] = randint(1, len(terminals))
    else:  # function
        if off.representation[pos] != -4:
            off.representation[pos] = -randint(1, noFunctions-1)
    return off


class Individual:
    pass


class Population:

    def __init__(self,  current_data, current_output, no_examples, length=100, individuals=None):
        if individuals is None:
            self.individuals = [Chromosome() for _ in range(length)]
            for i in self.individuals:
                i.grow_expression()
        else:
            self.individuals = individuals
        self.current_data = current_data
        self.current_output = current_output
        self.no_examples = no_examples

    def get_individuals(self):
        return self.individuals

    def get_best_individual(self):
        for i in self.individuals:
            i.compute_fitness(self.current_data, self.current_output, self.no_examples)
        return min(self.individuals, key=operator.attrgetter('fitness'))

    def cdf(self):
        s = len(self.individuals)
        for i in self.individuals:
            i.compute_fitness(self.current_data, self.current_output, self.no_examples)
            s += i.fitness

        partial_cdf = []
        new_sum = 0
        for i in range(len(self.individuals)):
            partial = 1 + self.individuals[i].fitness
            partial_cdf.append(s / partial)
            new_sum += s / partial

        new_partial = 0
        cdf = [0]
        for i in range(len(partial_cdf)):
            new_partial += partial_cdf[i]
            cdf.append(new_partial / new_sum)
        return cdf

    def parent_selection(self):
        cdf = self.cdf()
        p1 = None
        p2 = None

        r = random()
        for i in range(len(cdf) - 1):
            if cdf[i + 1] > r >= cdf[i]:
                p1 = self.individuals[i]
                break

        r = random()
        for i in range(len(cdf) - 1):
            if cdf[i + 1] > r >= cdf[i]:
                p2 = self.individuals[i]
                break

        self.individuals.append(crossover(p1, p2))

    def survival_selection(self):
        s = len(self.individuals)
        sum = s * (s + 1) / 2
        cdf = [0]
        partial = 0
        for i in range(len(self.individuals)):
            self.individuals[i].compute_fitness(self.current_data, self.current_output, self.no_examples)
            partial += i + 1
            cdf.append(partial / sum)

        x = sorted(self.individuals, key=operator.attrgetter('fitness'))

        r = random()
        for i in range(len(cdf) - 1):
            if cdf[i + 1] > r >= cdf[i]:
                self.individuals.remove(x.pop(i))
                break

    def __str__(self):
        s = "Population " + str(id(self)) + "\n"
        for i in self.individuals:
            s += str(i) + "\n"
        return s


class Algorithm:
    def __init__(self, population_size, current_data, current_output, no_examples):
        self.popSize = population_size

        self.crtData = current_data
        self.crtOut = current_output
        self.noExamples = no_examples
        self.population = Population(current_data, current_output, no_examples, population_size)
        self.actualGeneration = 0

        self.bestIndividuals = []

    def iteration(self):
        self.population.parent_selection()
        mutation(self.population.get_individuals()[-1])
        self.population.survival_selection()

    def run(self):
        while not (self.actualGeneration == 1500):
            self.iteration()
            self.actualGeneration += 1
            self.bestIndividuals.append(self.population.get_best_individual().fitness)
        return self.population.get_best_individual().representation, self.population.get_best_individual().fitness

    def statistics(self, values):
        arr = array(values)
        print('mean', mean(arr))
        print('std', std(arr))

    def plot(self):
        pyplot.plot(self.bestIndividuals)
        pyplot.show()


def read_data(filename):
    u = []
    t = []
    data = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            row = []
            for n in range(1, len(line)):
                row.append(float(line[n]))
            data.append(row)
        data = normalise(len(data), len(data[0]), data)
        for row in data:
            u.append(row[:-1])
            t.append(row[-1])
    f.close()
    return u, t


def normalise(no_examples, no_features, data):
    for j in range(no_features):
        minn = min([data[i][j] for i in range(no_examples)])
        maxx = max([data[i][j] for i in range(no_examples)])
        for i in range(no_examples):
            data[i][j] = (data[i][j] - minn) / (maxx - minn)
    return data


def main():
    u, t = read_data("data.txt")
    alg = Algorithm(30, u, t, len(u))
    print(alg.run())
    alg.plot()


main()
