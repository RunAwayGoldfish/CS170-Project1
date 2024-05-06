import random
import numpy as np
import copy


class SlidingPuzzle:
    def __init__(self, size=3, setup=None, mode=0):
        self.size = size
        self.board = self.generateBoard()
        self.parent = None
        self.weight = 0 # f(n)
        self.distance = 0 # Steps from origin aka g(n)
        self.hueristic = 0 
        self.mode = mode

        
        if(setup == None):
            self.board = self.generateBoard()
        else:
            self.board = (np.array(setup).reshape((int(size), -1))).tolist()

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
                    if self.board[i][j] == '*':
                        continue
                    goal_i = int(int(self.board[i][j] - 1) / self.size)
                    goal_j = (int(self.board[i][j] - 1)) % self.size
                    score += goal_i - i + goal_j - j

        self.hueristic = score

    def applyWeight(self):
        self.weight = self.distance + self.hueristic

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
    [8,7,1,6,"*",2,5,4,3],
    [1,2,3,4,5,6,7,"*",8],
    ["*",1,2,4,5,3,7,8,6],
    [1,2,3,4,5,6,8,7,"*"] # Impossible
]

def getData():
    for i in cases:
        arr = i
        for j in range(3):
            print(arr)
            puzzle2 = SlidingPuzzle(3, arr, j)
            solvePuzzle(puzzle2)


def solvePuzzle(puzzle, mode=0):
    frontier = []
    visited = []
    frontier.append(puzzle)
    foundSolution = False

    nodesChecked = 0 # Note that this is unique nodes becuase I do not add duplicates to frontier

    while(len(frontier) != 0):
        currentPuzzle = frontier[0]
        visited.append(currentPuzzle.createID())
        nodesChecked +=1

        #currentPuzzle.printBoard()
        #print("=============================")

        if(currentPuzzle.isSolved()):
            if(mode >= 1):
                currentPuzzle.printChain()
            foundSolution = True
            break

        for i in currentPuzzle.createVariants():
            if(i.createID() not in visited):
                frontier.append(i)
                

        frontier = sorted(frontier, key=lambda x: x.weight) # Should be already sorted if not using a hueristic?

        frontier = frontier[1:]
        if(mode == 2):
            if(len(frontier)%100 == 0):
                print(len(frontier))

    print(foundSolution, nodesChecked)


#puzzle = SlidingPuzzle(size=3,setup=[1,2,3,4,5,6,7,8,"*"],mode=2)
#solvePuzzle(puzzle,1)
getData()