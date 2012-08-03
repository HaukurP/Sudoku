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

def solve(board):
    board.printboard()
    trymore = board.trysolving()

    while trymore:
        trymore = board.trysolving()

    if board.issolved():
        print("Sudoku is solved")
        board.printboard()
        if not stack:
            pass
        else:
            print("Finishing other attempts")
            solve(stack.pop())
    else:
        depth =+ 1
        print("Sudoku is not solved - attempting multiple solutions")
        toaddinstack = board.multiplesolutions()
        for listboard in toaddinstack:
            boards = sudoku.Board()
            boards.importdata(listboard)
            stack.append(boards)
                      
    solve(stack.pop())      
    
        
    
start = time.clock()
board1 = sudoku.Board()
testboard(board1)
stack = [board1]
while stack:
    try:
        solve(stack.pop())
    except:
        print("No solution")

end = time.clock()-start
print("End of program - Runtime: {0:.4f} seconds".format(end))
