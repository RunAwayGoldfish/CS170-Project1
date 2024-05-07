import random
import numpy as np
import copy
import time
import math
import bisect

class SlidingPuzzle:
    maxDist = 0
    def __init__(self, size=3, setup=None, mode=0):
        self.size = size
        self.board = self.generateBoard()
        self.parent = None
        self.weight = 0 # f(n)
        self.distance = 0 # Steps from origin aka g(n)
        self.hueristic = 0 
        self.mode = mode
        self.step = ""
        self.blank_i = -1
        self.blank_j = -1
        
        if(setup == None):
            self.board = self.generateBoard()
        else:
            self.board = (np.array(setup).reshape((int(size), -1))).tolist()

        self.blank_i, self.blank_j = self.findBlank()

    def generateBoard(self):
        numbers = list(range(1, (self.size ** 2)))
        numbers = [str(x) for x in numbers] + ["*"]
        random.shuffle(numbers)
        return [numbers[i:i+self.size] for i in range(0, len(numbers), self.size)]

    def printBoard(self):
        padding = int(math.log10(self.size * self.size)+1)
        for row in self.board:
            print(" ".join(str(cell).rjust(padding) for cell in row))

    def move(self, direction):
        row, col = self.blank_i, self.blank_j

        if direction == 'up' and row > 0:
            self.board[row][col], self.board[row-1][col] = self.board[row-1][col], self.board[row][col]
            self.blank_i -= 1
        elif direction == 'down' and row < self.size - 1:
            self.board[row][col], self.board[row+1][col] = self.board[row+1][col], self.board[row][col]
            self.blank_i += 1
        elif direction == 'left' and col > 0:
            self.board[row][col], self.board[row][col-1] = self.board[row][col-1], self.board[row][col]
            self.blank_j -= 1
        elif direction == 'right' and col < self.size - 1:
            self.board[row][col], self.board[row][col+1] = self.board[row][col+1], self.board[row][col]
            self.blank_j += 1
        else:
            return False
        self.step = direction
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

                if(newPuzzle.distance > self.__class__.maxDist):
                    self.__class__.maxDist = newPuzzle.distance


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
        expansion = []
        moveSolution = []
        

        position = self
        #self.printBoard()
        while(position != None):
            #print("====================")
            #print(parent.weight, parent.distance, parent.hueristic)
            expansion.insert(0, position)
            moveSolution.insert(0, position.move)

            position = position.parent

        print("Optimal solution is as follows:")
        for i in range(len(expansion)):
            if(i == 0):
                print("Starting Position")
                expansion[i].printBoard()
                continue
            print("The optimal move is next optimal move is '{0}': which yields the state below:".format(expansion[i].step))
            expansion[i].printBoard()

        print("Solved!")
            
        
    def printBoardv2(self):
        if(self.distance == 0):
            print("Initial State: ")
        else:
            print("The best expansion is: g(n) = {0} and h(n) = {1}".format(self.distance, self.hueristic))

        self.printBoard()
        print()



    def applyHueristic(self):
        score = 0
        if(self.mode == 1): # misplaced tile hueristic
            score = 0
            for k in range(self.size * self.size - 1):
                i = int(k / self.size)
                j = k % self.size
                if(self.board[i][j] != str(i*self.size + j + 1)):
                    score +=1

        if(self.mode == 2): #Euclidian? Using manhattan because it seems like that's what it's meant to be:
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == "*":
                        continue

                    goal_i = (int(self.board[i][j]) - 1) // self.size
                    goal_j = (int(self.board[i][j]) - 1) % self.size
                    # Basically converts position (value in the cell) between 2d and 1d array

                    score += abs(goal_i - i) + abs(goal_j - j)

        self.hueristic = score

    def applyWeight(self):
        self.weight = self.distance + self.hueristic

    def resetMaxDist(self):
        self.__class__.maxDist = 0

# Example usage:
#puzzle = SlidingPuzzle()
#puzzle.print_board()
size = 3
#puzzle = SlidingPuzzle(size, [1,2,3,4,5,6,7,"*",8])
#puzzle = SlidingPuzzle(size, [1,2,3,4,5,6,"*",7,8])


#puzzle = SlidingPuzzle(size, setup=[1,2,"*",4,5,3,7,8,6],mode=0)


# "Oh Boy"
#puzzle = SlidingPuzzle(size, setup=[8,7,1,6,"*",2,5,4,3],mode=0)    # True 
#puzzle = SlidingPuzzle(size, setup=[8,7,1,6,"*",2,5,4,3],mode=1)   # True | 10720 visited

#puzzle = SlidingPuzzle(size, setup=[1,2,3,4,5,6,8,7,"*"],mode=0) 

cases = [
    [1,2,3,4,5,6,7,8,"*"], # Trivial
    [1,2,"*",4,5,3,7,8,6], #
    [1,2,3,4,5,6,7,"*",8],
    ["*",1,2,4,5,3,7,8,6],
    [8,7,1,6,"*",2,5,4,3],
    [1,2,3,4,5,6,8,7,"*"] # Impossible
]

def getData():
    for i in cases:
        arr = i
        for j in range(3):
            print(arr)
            puzzle2 = SlidingPuzzle(3, arr, j)
            solvePuzzle(puzzle2,mode=0)
            puzzle2.resetMaxDist()

def bisectionSort(arr, element):
    bisect.insort(arr, element, key=lambda x: -x.weight)


def solvePuzzle(puzzle, mode=0):
    frontier = []
    visited = set()
    frontier.append(puzzle)
    foundSolution = False
    startTime = time.time()
    nodesChecked = 0 # Note that this is unique nodes becuase I do not add duplicates to frontier
    maxDist = 0
    SolDepth = 0
    queueSize = 1
    maxQueueSize = 1
    currentPuzzle = None

    while(len(frontier) != 0):
        currentPuzzle = frontier.pop()
        visited.add(currentPuzzle.createID())
        nodesChecked +=1
        currentPuzzle.printBoardv2()

        
        if(currentPuzzle.isSolved()):
            SolDepth = currentPuzzle.distance
            print("Solved!")
            print()
            foundSolution = True
            break

        for i in currentPuzzle.createVariants():
            if(not (i.createID() in visited)):
                bisectionSort(frontier,i)
                queueSize+=1

        if(queueSize > maxQueueSize):
            maxQueueSize = queueSize        

        #frontier = sorted(frontier, key=lambda x: x.weight) # Should be already sorted if not using a hueristic

        queueSize-=1

        if(mode == 2):
            if(len(frontier)%100 == 0):
                print(len(frontier), currentPuzzle.maxDist)
       
    if(foundSolution):
        currentPuzzle.printChain()
    else:
        print("No solution")
        
    if(mode > 1):
        endTime = time.time()
        print(foundSolution, nodesChecked, endTime - startTime, currentPuzzle.maxDist, SolDepth, queueSize)

    


#puzzle = SlidingPuzzle(size=3,setup=[8,7,1,6,"*",2,5,4,3],mode=2)
#solvePuzzle(puzzle,2)
#getData()

def main():
    print("Enter integers separated by spaces with 0 to indicate the space: ")
    print("for example entering: \"1 2 3 4 5 6 7 8 0\" creates:")
    testPuzzle = SlidingPuzzle(3, setup=[1,2,3,4,5,6,7,"*",8],mode=0)
    testPuzzle.printBoard()
    user_input = input("Enter your values here: ")
    

    
    arr = user_input.split()
    arrSize = len(arr)
    
    for x in range(len(arr)):
        if arr[x] == "0":
            arr[x] = "*"
    
    print(arr)
    
    print("Enter the number for the corresponding algorithm you wish to run:")
    print("1 - Uniform Cost Search")
    print("2 - A* with the Misplaced Tile heuristic")
    print("3 - A* with the Euclidean distance heuristic")
    user_input = int(input()) - 1
    

    Puzzle = SlidingPuzzle(size=int(len(arr) ** 0.5), setup=arr, mode = user_input)
    solvePuzzle(Puzzle, mode=0)


main()