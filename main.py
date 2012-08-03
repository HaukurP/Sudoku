import sys, sudoku, time


def testboard(board):
    """creates a test board"""
    print("test board activated")
    board.addfinal(9,0,1)
    board.addfinal(6,0,6)
    board.addfinal(3,0,8)
    board.addfinal(9,1,5)
    board.addfinal(5,1,8)
    board.addfinal(3,2,0)
    board.addfinal(2,2,1)
    board.addfinal(4,2,8)
    board.addfinal(3,3,1)
    board.addfinal(2,3,6)
    board.addfinal(5,3,7)
    board.addfinal(6,3,8)
    board.addfinal(9,4,1)
    board.addfinal(8,4,7)
    board.addfinal(2,5,0)
    board.addfinal(8,5,1)
    board.addfinal(5,5,2)
    board.addfinal(3,5,7)
    board.addfinal(3,6,0)
    board.addfinal(2,6,7)
    board.addfinal(4,6,8)
    board.addfinal(8,7,0)
    board.addfinal(7,7,3)
    board.addfinal(5,8,0)
    board.addfinal(9,8,2)
    board.addfinal(6,8,7)

def trymultiple(board):
    pass

def solve(board):
    board.printboard()
    trymore = board.trysolving()

    while trymore:
        trymore = board.trysolving()
        board.printboard()

    if board.issolved():
        print("Sudoku is solved")
        if stack:
            print("Finishing other solutions - depth",depth)
            solve(stack.pop())
    else:
        depth =+ 1
        print("Sudoku is not solved - attempting multiple solutions - depth:",depth)
        board.multiplesolutions()
        
    
start = time.clock()
depth = 0
board1 = sudoku.Board()
testboard(board1)
stack = [board1]
solve(stack.pop())

end = time.clock()-start
print("End of program - Runtime: {0:.4f} seconds".format(end))
