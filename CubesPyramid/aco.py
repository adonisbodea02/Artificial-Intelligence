from random import *
import copy
from statistics import mean, stdev
from matplotlib import pyplot


class Cube:
    def __init__(self, length, color):
        self.length = length
        self.color = color

    def __str__(self):
        return str(self.length) + "; " + self.color


class Ant:

    def __init__(self, cubes):
        self.solution = []
        self.cubes = cubes

    def next_cubes(self):
        if len(self.solution) == 0:
            return [i for i in range(len(self.cubes))]
        else:
            possible_cubes = []
            for i in range(len(self.cubes)):
                if self.cubes[i].color != self.cubes[self.solution[-1]].color and self.cubes[i].length < self.cubes[self.solution[-1]].length and i not in self.solution:
                    possible_cubes.append(i)
            return possible_cubes

    def next_cube_heuristic(self, cube_position):
        ant = Ant(self.cubes)
        ant.solution = copy.deepcopy(self.solution)
        ant.solution.append(cube_position)
        return len(self.cubes) + 1 - len(ant.next_cubes())

    def add_cube(self, trace, alpha, beta, probability):
        possible_next_cubes = self.next_cubes()
        if len(possible_next_cubes) == 0:
            return False
        next_cubes_fitness = []
        for i in possible_next_cubes:
            next_cubes_fitness.append(self.next_cube_heuristic(i))
        if len(self.solution) != 0:
            next_cubes_fitness = [(next_cubes_fitness[i]**beta)*(trace[self.solution[-1]][possible_next_cubes[i]]**alpha) for i in range(len(next_cubes_fitness))]
        else:
            next_cubes_fitness = [(next_cubes_fitness[i] ** beta) for i in range(len(next_cubes_fitness))]
        #print(next_cubes_fitness)

        if random() < probability:
            p = [[possible_next_cubes[i], next_cubes_fitness[i]] for i in range(len(next_cubes_fitness))]
            p = min(p, key=lambda a: a[1])
            self.solution.append(p[0])
        else:
            s = sum(next_cubes_fitness)
            if s == 0:
                return choice(possible_next_cubes)
            p = [next_cubes_fitness[i] / s for i in range(len(next_cubes_fitness))]
            p = [sum(p[0:i + 1]) for i in range(len(p))]
            r = random()
            i = 0
            while r > p[i]:
                i = i + 1
            self.solution.append(possible_next_cubes[i])
        #print(self.solution)
        return True

    def evaluate(self):
        return len(self.cubes) - len(self.solution) + 1


class Controller:

    def __init__(self, filename, cubes):
        self.population = []
        self.iterations = 0
        self.nr_of_ants = 0
        self.alpha = 0
        self.beta = 0
        self.degradation_coefficient = 0
        self.load_parameters(filename)
        self.cubes = cubes

    def load_parameters(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            self.nr_of_ants = int(lines[0])
            self.iterations = int(lines[1])
            self.alpha = float(lines[2])
            self.beta = float(lines[3])
            self.degradation_coefficient = float(lines[4])
        f.close()

    def iteration(self, trace, probability):
        self.population = [Ant(self.cubes) for i in range(self.nr_of_ants)]
        for i in range(len(self.cubes)):
            for i in range(len(self.population)):
                self.population[i].add_cube(trace, self.alpha, self.beta, probability)
        updated_trace = [1 / self.population[i].evaluate() for i in range(len(self.population))]

        for i in range(len(self.cubes)):
            for j in range(len(self.cubes)):
                trace[i][j] = (1 - self.degradation_coefficient) * trace[i][j]

        for i in range(len(self.population)):
            for j in range(len(self.population[i].solution) - 1):
                x = self.population[i].solution[j]
                y = self.population[i].solution[j+1]
                trace[x][y] = trace[x][y] + updated_trace[i]

        f = [[self.population[i].evaluate(), i] for i in range(len(self.population))]
        f = min(f, key=lambda a: a[0])
        return self.population[f[1]].solution

    def algorithm(self, probability):
        sol = []
        best_sol = []
        trace = [[1 for i in range(len(self.cubes))] for j in range(len(self.cubes))]
        print("Wait for the program to finish!")
        for i in range(self.iterations):
            sol = self.iteration(trace, probability)
            if len(sol) > len(best_sol):
                best_sol = sol.copy()
        print("Length of the biggest pyramid found: ", len(best_sol))
        print("Biggest pyramid found:")
        for i in best_sol:
            print(self.cubes[i])

    def algorithm_with_plot(self, probability):
        Xs = [i for i in range(self.iterations)]
        Ys = []
        sol = []
        best_sol = []
        trace = [[1 for i in range(len(self.cubes))] for j in range(len(self.cubes))]
        print("Wait for the program to finish!")
        for i in range(self.iterations):
            sol = self.iteration(trace, probability)
            Ys.append(len(sol))
            if len(sol) > len(best_sol):
                best_sol = sol.copy()
        pyplot.plot(Xs, Ys)
        pyplot.show()

    def algorithm_for_statistics(self, probability):
        sol = []
        best_sol = []
        trace = [[1 for i in range(len(self.cubes))] for j in range(len(self.cubes))]
        for i in range(self.iterations):
            sol = self.iteration(trace, probability)
            if len(sol) > len(best_sol):
                best_sol = sol.copy()
        return best_sol

    def statistics(self):
        print("Wait for the program to finish!")
        bests = []
        for i in range(30):
            bests.append(len(self.algorithm_for_statistics(0.5)))
        return mean(bests), stdev(bests)


class Problem:

    def __init__(self, filename):
        self.cubes = []
        self.load_cubes(filename)
        self.controller = Controller("parameters.txt", self.cubes)

    def load_cubes(self, filename):
        with open(filename, "r") as f:
            cubes = []
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                line = line.split(',')
                cubes.append(Cube(int(line[0]), line[1]))
            self.cubes = cubes
        f.close()


class UI:
    def __init__(self):
        self.problem = Problem("data.txt")

    def printMenu(self):
        s = "\n"
        s += "0. Exit\n"
        s += "1. Run\n"
        s += "2. Run with plot\n"
        s += "3. Statistics\n"
        print(s)

    def run_problem(self):
        self.problem.controller.algorithm(0.5)

    def run_with_plot(self):
        self.problem.controller.algorithm_with_plot(0.5)

    def statistics(self):
        r = self.problem.controller.statistics()
        print("Mean: ", r[0])
        print("Standard Deviation: ", r[1])

    def run(self):
        ok = True
        while ok:
            self.printMenu()
            try:
                command = int(input(">> "))
                if command == 0:
                    ok = False
                elif command == 1:
                    self.run_problem()
                elif command == 2:
                    self.run_with_plot()
                elif command == 3:
                    self.statistics()
            except:
                print('Invalid option')


ui = UI()
ui.run()




