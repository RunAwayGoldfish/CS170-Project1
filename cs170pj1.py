import random
import numpy as np
import copy
from operator import attrgetter


class SlidingPuzzle:
    def __init__(self, size=3, hash=None, mode=0):
        self.size = size
        self.board = self.generateBoard()
        self.parent = None
        self.weight = 0 # f(n)
        self.distance = 0 # Steps from origin aka g(n)
        self.hueristic = 0 
        self.mode = mode

        
        if(hash == None):
            self.board = self.generateBoard()
        else:
            self.board = (np.array(hash).reshape((int(size), -1))).tolist()




    def generateBoard(self):
        numbers = list(range(1, self.size ** 2))
        numbers = [str(x) for x in numbers] + ["*"]
        random.shuffle(numbers)
        return [numbers[i:i+self.size] for i in range(0, len(numbers), self.size)]

    def printBoard(self):
        for row in self.board:
            print(" ".join(str(cell).rjust(2) for cell in row))

    def move(self, direction):
        row, col = self.findBlank()
        if direction == 'up' and row > 0:
            self.board[row][col], self.board[row-1][col] = self.board[row-1][col], self.board[row][col]
        elif direction == 'down' and row < self.size - 1:
            self.board[row][col], self.board[row+1][col] = self.board[row+1][col], self.board[row][col]
        elif direction == 'left' and col > 0:
            self.board[row][col], self.board[row][col-1] = self.board[row][col-1], self.board[row][col]
        elif direction == 'right' and col < self.size - 1:
            self.board[row][col], self.board[row][col+1] = self.board[row][col+1], self.board[row][col]
        else:
            return False
        return True

    def findBlank(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == "*":
                    return i, j

    def isSolved(self):
        return self.board[self.size-1][self.size-1] == "*" and self.secondCheck() 
            
    def secondCheck(self):
        for k in range(self.size * self.size - 1):
            i = int(k / self.size)
            j = k % self.size
            if(self.board[i][j] != str(i*self.size + j + 1)):
                return False
        return True

    def createVariants(self):
        variantList = []
        moves = ["up","down","left","right"]
        
        for i in moves:
            newPuzzle = copy.deepcopy(self)
            validMove = newPuzzle.move(i)
            if(validMove):
                newPuzzle.parent = self
                newPuzzle.distance = self.distance+1
                newPuzzle.applyHueristic()
                newPuzzle.applyWeight()
                variantList.append(newPuzzle)

        return variantList

    def duplicate(self):
        return copy.deepcopy(self)
    
    def createID(self):
        ID = ""
        for i in range(self.size):
            for j in range(self.size):
                ID += str(self.board[i][j])
        return ID

    def printChain(self):
        parent = self.parent
        self.printBoard()
        while(parent != None):
            print("====================")
            print(parent.weight, parent.distance, parent.hueristic)
            parent.printBoard()
            parent = parent.parent

    def applyHueristic(self):
        score = 0
        if(self.mode == 1):
            score = 0
            # misplaced tile hueristic
            for k in range(self.size * self.size - 1):
                i = int(k / self.size)
                j = k % self.size
                if(self.board[i][j] != str(i*self.size + j + 1)):
                    score +=1

        self.hueristic = score

    def applyWeight(self):
        self.weight = self.distance + self.hueristic

# Example usage:
#puzzle = SlidingPuzzle()
#puzzle.print_board()
size = 3
#puzzle = SlidingPuzzle(size, [1,2,3,4,5,6,7,"*",8])
#puzzle = SlidingPuzzle(size, [1,2,3,4,5,6,"*",7,8])
puzzle = SlidingPuzzle(size, mode=1)
puzzle.printBoard()
frontier = []
visited = []
frontier.append(puzzle)
foundSolution = False

while(len(frontier) != 0):
    currentPuzzle = frontier[0]
    visited.append(currentPuzzle.createID())

    #currentPuzzle.printBoard()
    #print("=============================")

    if(currentPuzzle.isSolved()):
        print(currentPuzzle.weight)
        currentPuzzle.printChain()
        foundSolution = True
        break

    for i in currentPuzzle.createVariants():
        if(i.createID() not in visited):
            frontier.append(i)

    frontier = sorted(frontier, key=lambda x: x.weight)

    frontier = frontier[1:]
    if(len(frontier)%100 == 0):
        print(len(frontier))





print(foundSolution)
'''
while(not puzzle.isSolved() and False):
    puzzle = SlidingPuzzle(size)
puzzle.printBoard()
print(puzzle.createID())
print("==========")
#puzzle.createVariants()
'''
'''
while not puzzle.isSolved():
    direction = input("Enter direction (up/down/left/right): ")
    puzzle.move(direction)
    puzzle.print_board()
print("Congratulations! You solved the puzzle!")
'''