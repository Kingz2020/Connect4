# -*- coding: utf-8 -*-
import numpy as np
"""
This is an attempt at connect 4, first without Pygames
and then when the concept is worked out I'll add the graphics.
This is based on a work on youtube by Keith Galli
"""

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    ''' creates the board
    '''
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def drop_piece(board, col, row, piece):
    board[row][col] = piece


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # horizontal combinations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c +
                                                 1] == piece and board[r][c +
                                                                          2] == piece and board[r][c +
                                                                                                   3] == piece:
                return True

    # vertical combinations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r +
                                              1][c] == piece and board[r +
                                                                       2][c] == piece and board[r +
                                                                                                3][c] == piece:
                return True

    # negatively slope diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r -
                                              1][c +
                                                 1] == piece and board[r -
                                                                       2][c +
                                                                          2] == piece and board[r -
                                                                                                3][c +
                                                                                                   3] == piece:
                return True

    # positively slope diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r +
                                              1][c +
                                                 1] == piece and board[r +
                                                                       2][c +
                                                                          2] == piece and board[r +
                                                                                                3][c +
                                                                                                   3] == piece:
                return True


board = create_board()
print_board(board)

turn = 0
game_over = False

while not game_over:
    # player 1 input
    if turn == 0:
        col = int(input("Player 1 type a number(0-6)"))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, col, row, 1)
            if winning_move(board, 1):
                print("Player 1 WINS!! ")
                game_over = True
    else:
        col = int(input("Player 2 type a number(0-6)"))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, col, row, 2)
            if winning_move(board, 2):
                print("Player 2 WINS!! ")
                game_over = True
    turn += 1
    turn = turn % 2
    print_board(board)
