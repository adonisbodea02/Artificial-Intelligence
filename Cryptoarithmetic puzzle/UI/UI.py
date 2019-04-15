from time import time

from Controller.Controller import Controller
from Problem.Problem import Problem


class UI:

    def __init__(self):
        self.__controller = Controller(Problem())
        self.__controller.getProblem().readFromFile("../input2.txt")

    def printMenu(self):
        s = ""
        s += "0. Exit\n"
        s += "1. Choose an input equation\n"
        s += "2. Find the solution with DFS\n"
        s += "3. Find the solution with GBFS\n"
        print(s)

    def chooseInput(self):
        s = ""
        s += "1. SEND + MORE = MONEY\n"
        s += "2. TAKE + A + CAKE = KATE\n"
        s += "3. EAT + THAT = APPLE\n"
        s += "4. NEVER - DRIVE = RIDE\n"
        print(s)
        n = 3
        try:
            print("Input your option (by default TAKE + A + CAKE = KATE)")
            n = int(input(">> option = "))
        except:
            print("Invalid number, the implicit equation is still TAKE + A + CAKE = KATE")

        p = Problem()
        if n == 1:
            p.readFromFile("../input.txt")
        elif n == 2:
            p.readFromFile("../input2.txt")
        elif n == 3:
            p.readFromFile("../input3.txt")
        elif n == 4:
            p.readFromFile("../input4.txt")
        else:
            print("No such option! The implicit equation is still EAT + THAT = APPLE\n")

        self.__controller = Controller(p)

    def equationWithDFS(self):
        startClock = time()
        self.__controller.DFS()
        print(self.__controller.getProblem().getFinalState().getLetters())
        print()
        print(self.__controller.getProblem())
        print('\nexecution time = ', time() - startClock, " seconds\n")

    def equationWithGBFS(self):
        startClock = time()
        self.__controller.GBFS()
        print(self.__controller.getProblem().getFinalState().getLetters())
        print()
        print(self.__controller.getProblem())
        print('\nexecution time = ', time() - startClock, " seconds\n")

    def run(self):
        ok = True
        while ok:
            self.printMenu()
            try:
                command = int(input(">> "))
                if command == 0:
                    ok = False
                elif command == 1:
                    self.chooseInput()
                elif command == 2:
                    self.equationWithDFS()
                elif command == 3:
                    self.equationWithGBFS()
            except:
                print('Invalid option')

def main():
    ui = UI()
    ui.run()


main()
