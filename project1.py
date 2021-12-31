import numpy as np  # To create games board
import random  # To get random probability
import pygame  # To use GUI/Graphics
import sys
import math

# RGB for colors
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 0, 0)

# Number of rows and columns in our board
rows = 6
columns = 7

# Identity of Player and Ai
player = 0
ai = 1

empty = 0
player_piece = 1
ai_piece = 2
window_length = 4

# To create game board


def create_board():
    board = np.zeros((rows, columns))
    return board

# To drop/put/mark our selected position


def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Checking if our position is valid or not


def is_valid_location(board, col):
    return board[rows-1][col] == 0

# If postion selected is not valid then the next closest postion will be marked


def get_next_open_position(board, col):
    for i in range(rows):
        if board[i][col] == 0:
            return i

# Printing the board by flipping it along 0-axis


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Checking if 4 pieces are connected horizontally
    for c in range(columns-3):
        for r in range(rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Vertical check
    for c in range(columns):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(columns-3):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Checking negative sloped diagonals
    for c in range(columns-3):
        for r in range(3, rows):
    	    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
    		    return True

    # # Check positively sloped diaganols
    # for c in range(COLUMN_COUNT-3):
    # 	for r in range(ROW_COUNT-3):
    # 		if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
    # 			return True


print("Jawad")



print("Some new changes....")