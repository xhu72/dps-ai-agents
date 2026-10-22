import random, copy

ROWS, COLS = 6, 7
#  ---- board and moves -------------------------------------------
def new_board():
    board = []
    for r in range(ROWS):          # make 6 rows
        row = []
        for c in range(COLS):      # each row has 7 empty spots
            row.append('.')
        board.append(row)
    return board                   # board[0] is the BOTTOM row

def valid_moves(board):
    top_row = board[ROWS - 1]      # board[5] is the top row
    moves = []
    for c in range(COLS):          # check each column 0..6
        if top_row[c] == '.':      # top spot empty -> column not full
            moves.append(c)
    return moves

def drop(board, col, player):
    for r in range(ROWS):
        if board[r][col] == '.':
            board[r][col] = player
            return r          # return the row it landed in. later the win check needs to know exactly where the piece is

def show(board):
    for r in reversed(range(ROWS)):       # top row (5) is printed first, and the bottom row (0) last
        print(' '.join(board[r]))
    print('0 1 2 3 4 5 6')
    

"""    
# test    
b = new_board()
drop(b, 3, 'X'); 
drop(b, 3, 'O')
show(b)        
"""
# ----  win check ---------------------------------------------------
def is_win(board, row, col, player):
    # Check horizontal, vertical, and diagonal directions
    directions = [
        (0, 1),    # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]

    for row_step, col_step in directions:
        count = 1      # Count the piece at the current position
        
        for sign in (1, -1):      # Check both forward and backward
            r = row + sign * row_step
            c = col + sign * col_step

            # Continue while the position is valid
            # and contains the same player's piece
            while (0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player):
                count += 1
                r += sign * row_step
                c += sign * col_step

        if count >= 4:     # Four or more pieces in a row means a win
            return True

    return False      # No winning line was found
"""
# test
b = new_board()
for c in range(4):
    r = drop(b, c, 'X')
print(is_win(b, r, 3, 'X'))  
"""
# ---- random playout ---------------------------------------------- 
def other(p):       # switch turns after each move
    return 'O' if p == 'X' else 'X'

def random_playout(board, player):      # these drops are imaginary moves. Play random moves until the end. Returns 'X', 'O' or None (draw).
    b = copy.deepcopy(board)            # never change the real board
    while valid_moves(b):
        c = random.choice(valid_moves(b))
        r = drop(b, c, player)
        if is_win(b, r, c, player):
            return player               # winner
        player = other(player)
    return None                         # draw

