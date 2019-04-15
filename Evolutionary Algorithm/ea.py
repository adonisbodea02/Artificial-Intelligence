from random import randint, random
from math import cos, pi, e
from statistics import mean, stdev
import operator
from matplotlib import pyplot

class Individual:

    def __init__(self, x = None, y = None):
        if x is None:
            self.__x = 10 * random() - 5
        else:
            self.__x = x
        if y is None:
            self.__y = 10 * random() - 5
        else:
            self.__y = y

        self.fitness = self.__computeFitness()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_fitness(self):
        return self.fitness

    def __computeFitness(self):
        return -20 * (e ** (-0.2 * (0.5*(self.__x ** 2 + self.__y ** 2))**(1/2))) - \
               e ** (0.5 * (cos(2*pi*self.__x) + cos(2*pi*self.__y))) + e + 20

    def mutate(self, mutation_probability):
        if mutation_probability >= random():
            if random() > 0.5:
                self.__x = 10 * random() - 5
            else:
                self.__y = 10 * random() - 5

    def crossover(self, parent1, parent2):
        r = random()
        return Individual(r * (parent1.get_x() + parent2.get_x()) / 2, r * (parent1.get_y() + parent2.get_y()) / 2)

    def __str__(self):
        return "(x = " + str(self.__x) + "; y = " + str(self.__y) + "; f(x,y) = " + str(self.fitness) + ")"


class Population:

    def __init__(self, length = 100, individuals = None):
        if individuals is None:
            self.__individuals = [Individual() for _ in range(length)]
        else:
            self.__individuals = individuals

    def get_individuals(self):
        return self.__individuals

    def get_best_individual(self):
        return min(self.__individuals, key=operator.attrgetter('fitness'))

    def cdf(self):
        s = len(self.__individuals)
        for i in self.__individuals:
            s += i.get_fitness()

        partial_cdf = []
        new_sum = 0
        for i in range(len(self.__individuals)):
            partial = 1 + self.__individuals[i].get_fitness()
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
            if cdf[i+1] > r >= cdf[i]:
                p1 = self.__individuals[i]
                break

        r = random()
        for i in range(len(cdf) - 1):
            if cdf[i + 1] > r >= cdf[i]:
                p2 = self.__individuals[i]
                break

        self.__individuals.append(p1.crossover(p1, p2))

    def survival_selection(self):
        s = len(self.__individuals)
        sum = s * (s + 1) / 2
        cdf = [0]
        partial = 0
        for i in range(len(self.__individuals)):
            partial += i + 1
            cdf.append(partial/sum)

        x = sorted(self.__individuals, key=operator.attrgetter('fitness'))

        r = random()
        for i in range(len(cdf) - 1):
            if cdf[i + 1] > r >= cdf[i]:
                self.__individuals.remove(x.pop(i))
                break


    def __str__(self):
        s = "Population " + str(id(self)) + "\n"
        for i in self.__individuals:
            s += str(i) + "\n"
        return s


class Algorithm:

    def __init__(self, filename, population = None):
        self.__length = 0
        self.__mp = 0
        self.__iterations = 0

        self.readParameters(filename)

        if population == None:
            self.__population = Population(self.__length)
        else:
            self.__population = population


    def iteration(self, mutation_probability):
        self.__population.parent_selection()
        self.__population.get_individuals()[-1].mutate(mutation_probability)
        self.__population.survival_selection()


    def readParameters(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            self.__mp = float(lines[0])
            self.__length = int(lines[1])
            self.__iterations = int(lines[2])
        f.close()

    def run(self):
        self.__population = Population(self.__length)
        for _ in range(self.__iterations):
            self.iteration(self.__mp)
        return self.__population.get_best_individual()

    def statistics(self):
        bests = []
        for i in range(30):
            bests.append(self.run().fitness)
        return mean(bests), stdev(bests)

    def run_with_plot(self):
        Xs = [i for i in range(self.__iterations)]
        Ys = []
        for _ in range(self.__iterations):
            self.iteration(self.__mp)
            Ys.append(self.__population.get_best_individual().get_fitness())
        pyplot.plot(Xs, Ys)
        pyplot.show()


class UI:
    def __init__(self):
        self.algorithm = Algorithm("params1.txt")

    def printMenu(self):
        s = ""
        s += "0. Exit\n"
        s += "1. Run\n"
        s += "2. Run with plot\n"
        s += "3. Statistics\n"
        print(s)

    def run_problem(self):
        print(self.algorithm.run())

    def run_with_plot(self):
        self.algorithm.run_with_plot()

    def statistics(self):
        r = self.algorithm.statistics()
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
