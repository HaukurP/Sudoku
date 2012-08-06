import sys, copy

class Board:
    """creates a new board with all possibilities open"""
    # A Board has numeric values infront of a True or False value
    # A True value means that the numeric value infront is a solution
    # A False value means that the numeric value(s) are possible solutions
    # The data is set up, looking at sudoku as:
    #     0        1      2
    # | 0 1 2 | 0 1 2 | ....
    # | 3 4 5 | .....
    # | 6 7 8 | ....
    # ______________________
    # |   3   |   4     .
    # | 0 1 2 |  ....   :
    
    def __init__(self):
        self.data = [None]*9
        for i in range(9):
            self.data[i]=[None]*9
            for j in range(9):
                self.data[i][j] = [1,2,3,4,5,6,7,8,9,False]

    def print_board(self):
        """prints out the board, badly at start"""
        # Use: board.print_board()
        # Before: board is a Board
        # After: board has been print out
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

    def import_data(self,bdata):
        """imports data from a list to a Board"""
        # Use: board.import_data(bdata)
        # Before: board is a Board, bdata is a list that looks like a Board
        # After: bdata is now a Board
        self.data = copy.deepcopy(bdata)                                             

    def add_final(self,number,i,j):
        """adds a number to a square, as an answer"""
        # Use: board.add_final(number,box,square)
        # Before: board is a Board, number: 1-9, box: 0-8, square: 0-8
        # After: number has been added as an answer to the board
        self.data[i][j] = [number, False]
        self.make_true()

    def add_numbers(self,numbers,i,j):
        """adds a number to a square and checks if it's an answer"""
        #bæta við seinna?

    def check_horizontal(self):
        """checks what possibilities are not ok, horizontally"""
        # Use: board.check_horizontal()
        # Before: board is a Board
        # After: if there is a solution in a line that number has been removed as an option through the line
        removed = False     #removed is a bad solution for checking if something was removed from the board
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] == True:
                    m,k = i//3,j//3
                    removed |= self.remove_from_line(self.data[i][j][0],m,k)
        return removed

    def remove_from_line(self,number,m,k):
        """removes a number from a line in the board"""
        # Use: board.remove_from_line(number,m,k)
        # Before: board: Board, number: 1-9, m: 0-2, k: 0-2
        # After: number has been removed from a line denoted by m and k
        removed = False
        for i in range(3):
            for j in range(3):
                if self.data[i+m*3][j+3*k][1] != True:
                    if number in self.data[i+m*3][j+3*k]:
                        self.data[i+m*3][j+3*k].remove(number)
                        removed = True
        return removed

    def check_vertically(self):
        """checks what possibilities are not ok, vertically"""
        # Use: board.check_vertically()
        # Before: same as check_horizontal
        # After: same as checkhriz
        removed = False
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] == True:
                    m,k = i%3,j%3
                    removed |= self.remove_from_row(self.data[i][j][0],m,k)
        return removed

    def remove_from_row(self,number,m,k):
        """removes a number from a row in the board"""
        # Use: board.remove_from_row(number,m,k)
        # Before: same as remove from line
        # After: -||-
        removed = False
        for i in range(0,9,3):
            for j in range(0,9,3):
                if self.data[i+m][j+k][1] != True:
                    if number in self.data[i+m][j+k]:
                        self.data[i+m][j+k].remove(number)
                        removed = True
        return removed

    def check_box(self):
        """checks what possibilities are not ok, inside a box"""
        # Use: board.check_box()
        # Before: -||-
        # After: -||-
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

    def remove_options(self):
        """calls for the check* operations"""
        # Use: board.remove_options()
        # Before: board: Board
        # After: all the check operations have been executed
        removed = self.check_horizontal()
        if removed:
            self.make_true()
            dontcare = self.check_vertically()
        else:
            removed = self.check_vertically()
        if removed:
            self.make_true()
            dontcare = self.check_box()
        else:
            removed = self.check_box()
        return removed

    def what_is_left(self):
        """finds out what numbers are left and adds them as solutions"""
        # Use: left = board.what_is_left()
        # Before: board: Board
        # After: what_is_left* operations have been executed
        removed = False
        for i in range(3):
            for j in range(3):
                m,k = i//3,j//3
                removed |= self.deduce_line(self.what_is_left_in_line(m,k),m,k)
        for i in range(0,9,3):                                              
             for j in range(0,9,3):
                 m,k = i%3,j%3
                 removed |= self.deduce_row(self.what_is_left_in_row(m,k),m,k)                   
        for i in range(9):
            removed |= self.deduce_box(self.what_is_left_in_box(i),i)

        return removed

    def what_is_left_in_box(self,i):
        """finds out what numbers are left to solve in a box"""
        # Use: left = board.what_is_left_in_box(box)
        # Before: board: Board, box: 0-8
        # After: finds out what numbers are left to solve in a box
        left = [1,2,3,4,5,6,7,8,9]
        for j in range(9):
            if self.data[i][j][1] == True:
                left.remove(self.data[i][j][0])
                    
        return left
    
    def deduce_box(self,left,i):
        """finds what possibilites are the only ones left in a box and adds them"""
        # Use: board.deduce_box(left,box)
        # Before: board: Board, left: [], box: 0-8
        # After: given what numbers are left to solve in a box, checks what numbers only
        # appear once in a box and deduces that it must be a solution
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

    def what_is_left_in_line(self,m,k):
        """finds out what numbers are left to solve in a line"""
        # Use: left = board.what_is_left_in_line(m,k)
        # Before: board: Board, m: 0-2, k: 0-2
        # After: finds what numbers are left to solve in a line denoted by m and k
        left = [1,2,3,4,5,6,7,8,9]
        for i in range(3):
            for j in range(3):
                 if self.data[i+m*3][j+3*k][1] == True:
                      left.remove(self.data[i+m*3][j+3*k][0])
        return left

    def deduce_line(self,left,m,k):
        """finds what possibilites are the only ones left in a line and adds them"""
        # Use: board.deduce_line(left,m,k)
        # Before: board: Board, left: [], m: 0-2, k: 0-2
        # After: given what numbers are left to solve in a line, checks what numbers only
        # appear once in a line and deduces that it must be a solution
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

    def what_is_left_in_row(self,m,k):
        """finds out what numbers are left in the row"""
        # Use: left = board.what_is_left_in_row(m,k)
        # Before: board: Board, m: 0-2, k: 0-2
        # After: same as in what_is_left_in_line
        left = [1,2,3,4,5,6,7,8,9]
        for i in range(3):
            for j in range(3):
                 if self.data[i+m][j+k][1] == True:
                      left.remove(self.data[i+m][j+k][0])
        return left

    def deduce_row(self,left,m,k):
        """finds what possibilites are the only ones left in a row and adds them"""
        # Use: board.deduce_row(left,m,k)
        # Before: board: Board, left: [], m: 0-2, k: 0-2
        # After: same as in deduce_line
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

    def try_solving(self):
        """helping function"""
        # Use: board.try_solving()
        # Before: board: Board
        # After: calls for check* and what_is_left* operations
        removed = self.remove_options()
        removed |= self.make_true()
        removed |= self.what_is_left()
        return removed

    def make_true(self):
        """makes a square true if there is single possibilites (solves)"""
        # Use: board.make_true()
        # Before: board: Board
        # After: if a number was a single option but was False (not a solution) it is now True (a solution)
        madetrue = False
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] == False:
                    self.data[i][j][1] = True
                    madetrue = True
        return madetrue

    def is_solved(self):
        """returns true if sudoku is solved, else false"""
        # Use: is_board_solved = board.is_solved()
        # Before: board: Board
        # After: is_board_solved = True if the board is solved, False otherwise
        solved = True
        for i in range(9):
            for j in range(9):
                if self.data[i][j][1] != True:
                    solved = False
                    break
        return solved

    def multiple_solutions(self):
        """returns multiple sudoku boards where a number has been picked"""
        # Use: solutions = board.multiple_solutions()
        # Before: board: Board
        # After: solutions = [board1,board2,...]
        i,j = self.find_lowest_amount()
        length = len(self.data[i][j])-1
        multipleboards = [None]*length
        for k in range(length):
            numbers = self.data[i][j][k]
            multipleboards[k] = copy.deepcopy(self.data)
            multipleboards[k][i][j] = [numbers,True]
            #print("Guessing on",numbers,"in",i,j)
        return multipleboards

    def find_lowest_amount(self):
        """finds the lowest amount of options in a square on the whole board and returns the index of it"""
        # Use: i,j = board.finelowestamount()
        # Before: board: Board
        # After: i,j = box, square where the lowest amount of options are
        counter = 3
        while counter <= 10:
            for i in range (9):
                for j in range(9):
                    if len(self.data[i][j]) <= counter and self.data[i][j][1] != True:
                        return [i,j]
            counter += 1

            
