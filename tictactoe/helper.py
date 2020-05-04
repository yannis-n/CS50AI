

def check_board(board):
    check = {'X':0, 'O':0, 'EMPTY':0}
    for row in board:
        for col in row:
            if col == "X":
                check['X'] += 1
            elif col == "O":
                check['O'] += 1
            else:
                check['EMPTY'] += 1
    return check
