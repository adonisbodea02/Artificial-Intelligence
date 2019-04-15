from time import time

from Problem.Problem import Problem

class PriorityQueue:
    def __init__(self):
        self.__values = {}

    def isEmpty(self):
        return len(self.__values) == 0

    def pop(self):
        topPriority = None
        topObject = None
        for obj in self.__values:
            objPriority = self.__values[obj]
            if topPriority is None or topPriority > objPriority:
                topPriority = objPriority
                topObject = obj
        del self.__values[topObject]
        return topObject

    def add(self, obj, priority):
        self.__values[obj] = priority

    def contains(self, val):
        return val in self.__values

class Controller:

    def __init__(self, problem):
        self.__problem = problem

    def getProblem(self):
        return self.__problem

    def DFS(self):
        stack = [self.__problem.getInitialState()]
        while len(stack) != 0:
            currentState = stack.pop()
            if self.__problem.isSolution(currentState):
                self.__problem.setFinalState(currentState)
                return currentState
            stack += self.__problem.expand(currentState)

    def GBFS(self):
        p_queue = PriorityQueue()
        p_queue.add(self.__problem.getInitialState(), self.__problem.heuristic(self.__problem.getInitialState()))
        while not p_queue.isEmpty():
            currentState = p_queue.pop()
            if self.__problem.isSolution(currentState):
                self.__problem.setFinalState(currentState)
                return currentState
            for i in self.__problem.expand(currentState):
                p_queue.add(i, self.__problem.heuristic(i))

