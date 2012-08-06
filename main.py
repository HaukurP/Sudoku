import sys, sudoku, time


def testboard(board):
    """creates a test board"""
    # Use: board.testboard()
    # Before: board is a Board from sudoku
    # After: board is now configured by the initial input set in this function
    print("test board activated")
    #           board.add_final(number,box,square)
    board.add_final(9,0,1)
    board.add_final(6,0,6)
    board.add_final(3,0,8)
    board.add_final(9,1,5)
    board.add_final(5,1,8)
    board.add_final(3,2,0)
    board.add_final(2,2,1)
    board.add_final(4,2,8)
    board.add_final(3,3,1)
    board.add_final(2,3,6)
    board.add_final(5,3,7)
    board.add_final(6,3,8)
    board.add_final(9,4,1)
    board.add_final(8,4,7)
    board.add_final(2,5,0)
    board.add_final(8,5,1)
    board.add_final(5,5,2)
    board.add_final(3,5,7)
    board.add_final(3,6,0)
    board.add_final(2,6,7)
    board.add_final(4,6,8)
    board.add_final(8,7,0)
    board.add_final(7,7,3)
    board.add_final(5,8,0)
    board.add_final(9,8,2)
    board.add_final(6,8,7)


def solve(board):
    """attempts to solve a particular board"""
    # Use: solve(board)
    # Before: board is a Board
    # After: board has been solved or new boards have been created and put in a queue
    try_more = board.try_solving() #try_more checks if some possibilites were removed

    while try_more:
        try_more = board.try_solving()

    if board.is_solved():
        print("Sudoku is solved")
        solutions.append(board)
        
        if not stack:
            pass
        else:
            print("Finishing other attempts")
            solve(stack.pop())
    else:
        print("Sudoku is not solved - attempting multiple solutions")
        to_add_in_stack = board.multiple_solutions()
        for listboard in to_add_in_stack:
            boards = sudoku.Board()
            boards.import_data(listboard)
            stack.append(boards)    #adding multiple solutions to a queue
                      
    solve(stack.pop())      
    
def single_solutions(boards):
    """finds single solutions"""
    # Use: single_solutions_boards = single_solutions(boards)
    # Before: boards might contain the same solution often
    # After: single_solutions_boards is a list only containing single solutions
    single_solutions = []
    for board in boards:
        if board not in single_solutions:
            single_solutions.append(board)
    return single_solutions
        
    
start = time.clock()
board1 = sudoku.Board()
testboard(board1)
stack = [board1]
solutions = []
while stack:
    try:
        solve(stack.pop())
    except:
        pass
        print("No solution")

end = time.clock()-start
print("End of program - Time used to solve: {0:.4f} seconds".format(end))
single_solution = single_solutions(solutions)

for boards in single_solution:
    boards.print_board()
