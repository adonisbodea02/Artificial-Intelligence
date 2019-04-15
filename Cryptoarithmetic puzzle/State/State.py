class State:

    def __init__(self, letters=None, words=None, firstLetters=None, operation=""):
        if words is None:
            words = []
        if letters is None:
            letters = {}
        if firstLetters is None:
            firstLetters = []
        self.__letters = letters
        self.__words = words
        self.__operation = operation
        self.__firstLetters = firstLetters

    def __str__(self):
        return str(self.__letters)

    def getLetters(self):
        return self.__letters

    def getFirstLetters(self):
        return self.__firstLetters

    def getWords(self):
        return self.__words

    def getOperation(self):
        return self.__operation

    def setLetters(self, letters):
        self.__letters = letters

    def setFirstLetters(self, firstLetters):
        self.__firstLetters = firstLetters

    def setWords(self, words):
        self.__words = words

    def setOperation(self, operation):
        self.__operation = operation

    def getOperands(self):
        hexOperands = []
        for word in self.__words:
            index = len(word) - 1
            count = 1
            hexOperand = 0
            while index >= 0:
                hexOperand = self.__letters[word[index]] * count + hexOperand
                index -= 1
                count *= 16
            hexOperands.append(hexOperand)
        return hexOperands