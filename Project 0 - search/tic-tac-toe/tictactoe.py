"""
Tic Tac Toe Player
"""

import math
import copy
import pandas as pd

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
    amount_of_empty = 0
    
    
    for i in range(3):
        amount_of_empty += board[i].count(EMPTY)
            
    return O if amount_of_empty % 2 == 0 else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_acctions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_acctions.add((i, j))
                
    return possible_acctions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    x, y = action
    current_player = player(board)
    next_board = copy.deepcopy(board)
    next_board[x][y] = current_player
    
    return next_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
            
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
            
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
        
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
        
    return EMPTY

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != EMPTY:
        return True
    
    for i in range(3):
        if EMPTY in board[i]:
            return False
        
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    
    return 1 if game_winner == X else -1 if game_winner == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    ai_winner = player(board)
    
    optimal_move = EMPTY
    
    if terminal(board):
        return optimal_move    

    print( actions(board))
    
    beta = math.inf
    alpha = -math.inf
    
    if ai_winner == X:
        best_score = -math.inf
        for action in actions(board):
            score = min_value(result(board, action),alpha, beta)
            if score > best_score:
                best_score = score
                optimal_move = action
            if score == 1:
                return optimal_move
    else:
        best_score = math.inf
        for action in actions(board):
            score = max_value(result(board, action), alpha, beta)
            if score < best_score:
                best_score = score
                optimal_move = action
            if score == -1:
                return optimal_move
        
    return optimal_move
    
    
def max_value(board, alpha, beta):
    """
    Returns the best score that the maximizing player can guarantee.
    """
    if terminal(board):
        return utility(board)
    
    max_value = -math.inf
    
    for action in actions(board):
        max_value = max(max_value, min_value(result(board, action), alpha, beta))
        if max_value >= beta:
            return max_value
        alpha = max(alpha, max_value)
    return max_value
    
def min_value(board, alpha, beta):
    """
    Returns the best score that the minimizing player can guarantee.
    """
    if terminal(board):
        return utility(board)
    
    min_value = math.inf
    
    for action in actions(board):
        min_value = min(min_value, max_value(result(board, action), alpha, beta))
        if min_value <= alpha:
            return min_value
        beta = min(beta, min_value)        
    return min_value
    
    
    
            
    

