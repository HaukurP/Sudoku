import sys, copy

class Board:
    """creates a new board with all possibilities open"""
    # A Board has numeric values infront of a True or False value
    # A True value means that the numeric value infront is a solution
    # A False value means that the numeric value(s) are possible solutions
    # The data is set up, looking at sudoku as:
    #     0        1      2
    # | 0 1 2 | 1 2 3 | ....
    # | 3 4 5 | .....
    # | 6 7 8 | ....
    # ______________________
    # |   3   |   4     .
    # | ..... |         :
    
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

    def importdata(self,bdata):
        """imports data from a list to a Board"""
        self.data = copy.deepcopy(bdata)                                             

    def addfinal(self,number,i,j):
        """adds a number to a square, as an answer"""
        self.data[i][j] = [number, False]
        self.maketrue()

    def addnumbers(self,numbers,i,j):
        """adds a number to a square and checks if it's an answer"""
        #bæta við seinna?

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
        print("    horizontally")                                                    #Þarf þetta?
        for i in range(3):
            for j in range(3):
                m,k = i//3,j//3
                if removed:
                    dontcare = self.deduceline(self.whatsleftinline(m,k),m,k)
                else:
                    removed = self.deduceline(self.whatsleftinline(m,k),m,k)
        print("    vertically")                                                  #Þarf þetta?
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
        """returns true if sudoku is solved, else false"""
        solved = True
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] != True:
                    solved = False
                    break
        return solved

    def multiplesolutions(self):
        """returns multiple sudoku boards where a number has been picked"""
        i,j = self.findlowestamount()
        length = len(self.data[i][j])-1
        multipleboards = [None]*length
        for k in range(length):
            numbers = self.data[i][j][k]
            multipleboards[k] = copy.deepcopy(self.data)
            multipleboards[k][i][j] = [numbers,True]
            print("Guessing on",numbers,"in",i,j)
        return multipleboards

    def findlowestamount(self):
        """finds the lowest amount of options in a square on the whole board and returns the index of it"""
        counter = 3
        while counter <= 10:
            for i in range (9):
                for j in range(9):
                    if len(self.data[i][j]) <= counter and self.data[i][j][1] != True:
                        return [i,j]
            counter += 1

            
