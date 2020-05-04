"""
Tic Tac Toe Player
"""
from helper import *
import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    check = check_board(board)

    if check['EMPTY'] == 9 or check['X'] == check['O']:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            if col is None:
                possible_actions.add((x,y))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("This action is not permitted")
    result = copy.deepcopy(board)
    result[i][j] = player(board)

    return result



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for x, row in enumerate(board):
        ttt_horizontal = 0
        if board[x][0] == EMPTY:
            continue
        player = board[x][0]
        for y in range(1,3):
            if player != board[x][y]:
                break
            else:
                ttt_horizontal += 1
                if ttt_horizontal == 2:
                    return player


    ttt_diagonal = 0
    for i in range(1,3):
        if board[0][0] == EMPTY:
            continue
        player_diagonal = board[0][0]
        if board[i][i] != player_diagonal:
            break
        else:
            ttt_diagonal += 1
            if ttt_diagonal == 2:
                return player_diagonal

    ttt_reverse_diagonal = 0
    for i in range(1,3):
        if board[2][0] == EMPTY:
            continue
        player_reverse_diagonal = board[2][0]
        if board[2-i][i] != player_reverse_diagonal:
            break
        else:
            ttt_reverse_diagonal += 1
            if ttt_reverse_diagonal == 2:
                return player_reverse_diagonal

    for y in range (0,3):
        if board[0][y] == EMPTY:
            continue
        ttt_vertical = 0
        player = board[0][y]
        for x in range(1,3):
            if player != board[x][y]:
                break
            else:
                ttt_vertical += 1
                if ttt_vertical == 2:
                    return player
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    if check_board(board)['EMPTY'] == 0:
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is None:
        return 0
    elif winner(board) == X:
        return 1
    else:
        return -1

def max_value(board, v):
    if terminal(board):
        return utility(board)
    value = float("-inf")
    for action in actions(board):
        v_new = min_value(result(board, action), value)

        if v_new > value:
            value = v_new
        if value > v:
            break
        if value == 1:
            break
    return value

def min_value(board,v):
    if terminal(board):
        return utility(board)
    value = float("inf")
    for action in actions(board):
        v_new = max_value(result(board, action), value)

        if v_new < value:
            value = v_new
        if value < v:
            break
        if value == -1:
            break
    return value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    optimal = None

    if player(board) == X:
        v = float("-inf")
        for action in actions(board):
            v_new = min_value(result(board, action), v)
            if v_new == 1:
                optimal = action
                break
            if v_new > v:
                v = v_new
                optimal = action
    else:
        v = float("inf")
        for action in actions(board):
            v_new = max_value(result(board, action), v)
            if v_new == -1:
                optimal = action
                break
            if v_new < v:
                v = v_new
                optimal = action

    return optimal
