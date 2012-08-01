import sys

class Board:
    """creates a new board with all possibilities open"""
    def __init__(self):
        print("creating sudoku")
        self.data = [None]*9
        for i in range(9):
            self.data[i]=[None]*9
            for j in range(9):
                self.data[i][j] = [1,2,3,4,5,6,7,8,9,False]

    def printboard(self):
        """prints out the board, badly at start"""
        print("_______________________________________")
        for m in range(3):
            for k in range(3):
                for i in range(3):
                    for j in range(3):
                        length = len(self.data[i+m*3][j+3*k])-1
                        print(self.data[i+3*m][j+3*k][:length],end="")
                    print(end="---")
                print()
        print("_______________________________________")

    def addfinal(self,number,i,j):
        """adds a number to a square, as an answer"""
        self.data[i][j] = [number, True]

    def realboard(self):
        """creates a test board"""
        print("real board activated")
        self.addfinal(9,0,1)
        self.addfinal(6,0,6)
        self.addfinal(3,0,8)
        self.addfinal(9,1,5)
        self.addfinal(5,1,8)
        self.addfinal(3,2,0)
        self.addfinal(2,2,1)
        self.addfinal(4,2,8)
        self.addfinal(3,3,1)
        self.addfinal(2,3,6)
        self.addfinal(5,3,7)
        self.addfinal(6,3,8)
        self.addfinal(9,4,1)
        self.addfinal(8,4,7)
        self.addfinal(2,5,0)
        self.addfinal(8,5,1)
        self.addfinal(5,5,2)
        self.addfinal(3,5,7)
        self.addfinal(3,6,0)
        self.addfinal(2,6,7)
        self.addfinal(4,6,8)
        self.addfinal(8,7,0)
        self.addfinal(7,7,3)
        self.addfinal(5,8,0)
        self.addfinal(9,8,2)
        self.addfinal(6,8,7)


    def checkhoriz(self):
        """checks what possibilities are not ok, horizontally"""
        removed = False
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] == True:
                    m,k = i//3,j//3
                    if removed:
                        dontcare = self.removefromline(self.data[i][j][0],m,k)
                    else:
                        removed = self.removefromline(self.data[i][j][0],m,k)
        return removed

    def removefromline(self,number,m,k):
        """removes a number from a line in the board"""
        removed = False
        for i in range(3):
            for j in range(3):
                if self.data[i+m*3][j+3*k][1] != True:
                    if number in self.data[i+m*3][j+3*k]:
                        self.data[i+m*3][j+3*k].remove(number)
                        removed = True
        return removed

    def checkvertic(self):
        """checks what possibilities are not ok, vertically"""
        removed = False
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] == True:
                    m,k = i%3,j%3
                    if removed:
                        dontcare = self.removefromrow(self.data[i][j][0],m,k)
                    else:
                        removed = self.removefromrow(self.data[i][j][0],m,k)
        return removed

    def removefromrow(self,number,m,k):
        """removes a number from a row in the board"""
        removed = False
        for i in range(0,9,3):
            for j in range(0,9,3):
                if self.data[i+m][j+k][1] != True:
                    if number in self.data[i+m][j+k]:
                        self.data[i+m][j+k].remove(number)
                        removed = True
        return removed

    def checkbox(self):
        """checks what possibilities are not ok, inside a box"""
        removed = False
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] == True:
                    number = self.data[i][j][0]
                    for k in range(9):
                        if self.data[i][k][1] != True:
                            if number in self.data[i][k]:
                                self.data[i][k].remove(number)
                                removed = True
        return removed

    def removeoptions(self):
        """calls for the check* operations"""
        print("removing possibilities from squares")
        removed = self.checkhoriz()
        print("    horizontally")
        if removed:
            self.maketrue()
            dontcare = self.checkvertic()
            print("    vertically")
        else:
            removed = self.checkvertic()
            print("    vertically")
        if removed:
            self.maketrue()
            dontcare = self.checkbox()
            print("    inside boxes")
        else:
            removed = self.checkbox()
            print("    inside boxes")
        return removed

    def whatsleft(self):
        """finds out what numbers are left and adds them as solutions"""
        print("checking for single possibilites")
        removed = False
        print("    horizontally")
        for i in range(3):
            for j in range(3):
                m,k = i//3,j//3
                if removed:
                    dontcare = self.deduceline(self.whatsleftinline(m,k),m,k)
                else:
                    removed = self.deduceline(self.whatsleftinline(m,k),m,k)
        print("    vertically")
        for i in range(0,9,3):
             for j in range(0,9,3):
                 m,k = i%3,j%3
                 if removed:
                     dontcare = self.deducerow(self.whatsleftinrow(m,k),m,k)
                 else:
                     removed = self.deducerow(self.whatsleftinrow(m,k),m,k)                   
        print("    inside boxes")
        for i in range(9):
            if removed:
                dontcare = self.deducebox(self.whatsleftinbox(i),i)
            else:
                removed = self.deducebox(self.whatsleftinbox(i),i)

        return removed

    def whatsleftinbox(self,i):
        """finds out what numbers are left to solve in a box"""
        left = [1,2,3,4,5,6,7,8,9]
        for j in range(9):
            if self.data[i][j][1] == True:
                left.remove(self.data[i][j][0])
        return left
    
    def deducebox(self,left,i):
        """finds what possibilites are the only ones left in a box and adds them"""
        removed = False
        for number in left:
            often = 0
            cordx,cordy = 0,0
            for j in range(9):
                if self.data[i][j][1] == True:
                    pass
                elif number in self.data[i][j]:
                    often += 1
                    cordx,cordy = i,j
                else:
                    pass
            if often == 1:
                self.data[cordx][cordy] = [number,True]
                removed = True
        return removed

    def whatsleftinline(self,m,k):
        """finds out what numbers are left to solve in a line"""
        left = [1,2,3,4,5,6,7,8,9]
        for i in range(3):
            for j in range(3):
                 if self.data[i+m*3][j+3*k][1] == True:
                      left.remove(self.data[i+m*3][j+3*k][0])
        return left

    def deduceline(self,left,m,k):
        """finds what possibilites are the only ones left in a line and adds them"""
        removed = False
        for number in left:
            often = 0
            cordx,cordy = 0,0
            for i in range(3):
                for j in range(3):
                    if self.data[i+m*3][j+3*k][1] == True:
                        pass
                    elif number in self.data[i+m*3][j+3*k]:
                        often += 1
                        cordx,cordy = i+m*3,j+3*k
                    else:
                        pass
            if often == 1:
                self.data[cordx][cordy] = [number,True]
                removed = True
                print("virkaði - line")
        return removed

    def whatsleftinrow(self,m,k):
        """finds out what numbers are left in the row"""
        left = [1,2,3,4,5,6,7,8,9]
        for i in range(3):
            for j in range(3):
                 if self.data[i+m][j+k][1] == True:
                      left.remove(self.data[i+m][j+k][0])
        return left

    def deducerow(self,left,m,k):
        """finds what possibilites are the only ones left in a row and adds them"""
        removed = False
        for number in left:
            often = 0
            cordx,cordy = 0,0
            for i in range(3):
                for j in range(3):
                    if self.data[i+m][j+k][1] == True:
                        pass
                    elif number in self.data[i+m][j+k]:
                        often += 1
                        cordx,cordy = i+m,j+k
                    else:
                        pass
            if often == 1:
                self.data[cordx][cordy] = [number,True]
                removed = True
                print("virkaði - row")
        return removed

    def trysolving(self):
        """helping function"""
        removed = self.removeoptions()
        if removed:
            dontcare = self.maketrue()
        else:
            removed = self.maketrue()
        if removed:
            print("some options were removed")
        if removed:
            dontcare = self.whatsleft()
        else:
            removed = self.whatsleft()
        return removed

    def maketrue(self):
        """makes a square true if there is single possibilites (solves)"""
        madetrue = False
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] == False:
                    self.data[i][j][1] = True
                    madetrue = True
        return madetrue

    def issolved(self):
        solved = True
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] != True:
                    solved = False
        if solved:
            return "Sudoku is solved"
        else:
            return "Sudoku is not solved"

    def multiplesolutions():
        pass

board = Board()
board.realboard()
board.printboard()
trymore = board.trysolving()

while trymore:
    trymore = board.trysolving()
    board.printboard()

print(board.issolved())
print("end of program")
