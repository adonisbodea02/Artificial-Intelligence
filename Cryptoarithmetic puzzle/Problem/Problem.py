import copy
import math

from State.State import State


class Problem:

    def __init__(self):
        self.__initialState = State()
        self.__finalState = State()

    def getInitialState(self):
        return self.__initialState

    def getFinalState(self):
        return self.__finalState

    def setFinalState(self, state):
        self.__finalState = state

    def readFromFile(self, filename):

        with open(filename, "r") as f:
            lines = f.readlines()

            count = 0
            for line in lines:
                self.__initialState.getWords().append("")
                firstLetterFound = False
                for c in line:
                    if c .isalpha():
                        if firstLetterFound == False:
                            self.__initialState.getFirstLetters().append(c)
                            firstLetterFound = True
                        self.__initialState.getLetters()[c] = -1

                        self.__initialState.getWords()[count] += c

                    elif c == "+" or c == "-":
                        self.__initialState.setOperation(c)
                count += 1

        f.close()

    def isSolution(self, state):
        dict = state.getLetters()

        for v in dict.values():
            if v < 0:
                return False

        operation = state.getOperation()
        hexOperands = state.getOperands()

        if operation == "+":
            sum = 0
            for i in range(len(hexOperands)-1):
                sum += hexOperands[i]
            if sum == hexOperands[-1]:
                return True
        else:
            minuend = hexOperands[0]
            for i in range(1, len(hexOperands) - 1):
                minuend -= hexOperands[i]
            if minuend == hexOperands[-1]:
                return True

        return False

    def expand(self, state):
        myList = []
        dict = state.getLetters()
        c = ''
        for e in dict.keys():
            if dict[e] == -1:
                c = e
                break
        if c == '':
            return []
        numbers_left = [i for i in range(16)]
        if c in state.getFirstLetters():
            numbers_left.remove(0)
        for v in dict.values():
            if v in numbers_left:
                numbers_left.remove(v)
        for i in numbers_left:
            newState = copy.deepcopy(state)
            newState.getLetters()[c] = i
            myList.append(newState)

        return myList

    def heuristic(self, state):
        letters = state.getLetters()
        c = 0
        for i in letters.values():
            if i == -1:
                c += 1
        if c != 0:
            return 100**c
        h = 0
        dict = {}
        words = state.getWords()
        for i in words:
            dict[i] = len(i) - 1
        max_length = max(dict.values())
        if state.getOperation() == "+":
            while max_length >= 0:
                s = 0
                for i in range(len(words) - 1):
                    if dict[words[i]] >= 0:
                        s += letters[words[i][dict[words[i]]]]
                        dict[words[i]] -= 1
                max_length -= 1
                s = s%16
                s -= letters[words[len(words) -1][dict[words[len(words) -1 ]]]]
                dict[words[len(words) -1]] -= 1
                h += abs(s)
        else:
            while max_length >= 0:
                s = 0
                for i in range(1, len(words)):
                    if dict[words[i]] >= 0:
                        s += letters[words[i][dict[words[i]]]]
                        dict[words[i]] -= 1
                max_length -= 1
                s = s%16
                s -= letters[words[0][dict[words[0]]]]
                dict[words[0]] -= 1
                h += abs(s)
        return h


    def __str__(self):
        max_spaces = 0
        for i in self.__initialState.getWords():
            max_spaces = max(max_spaces, len(i))
        s = (max_spaces-len(self.__initialState.getWords()[0])) * " " + self.__initialState.getWords()[0] + self.__initialState.getOperation() + "\n"
        for i in range(1, len(self.__initialState.getWords()) - 2):
            s += (max_spaces-len(self.__initialState.getWords()[i])) * " " + self.__initialState.getWords()[i] + "\n"
        s += (max_spaces-len(self.__initialState.getWords()[len(self.__initialState.getWords()) - 2])) * " " + self.__initialState.getWords()[len(self.__initialState.getWords()) - 2] + "=\n"
        s += (max_spaces-len(self.__initialState.getWords()[len(self.__initialState.getWords()) - 1])) * " "  + self.__initialState.getWords()[len(self.__initialState.getWords()) - 1]

        s += "\n\n"

        s += str(format(self.__finalState.getOperands()[0], '06x')) + self.__finalState.getOperation() + "\n"
        for i in range(1, len(self.__finalState.getOperands()) - 2):
            s = s + str(format(self.__finalState.getOperands()[i], '06x')) + "\n"
        s += str(format(self.__finalState.getOperands()[len(self.__finalState.getOperands()) - 2], '06x')) + "=\n"
        s += str(format(self.__finalState.getOperands()[len(self.__finalState.getOperands()) - 1], '06x'))

        return s
