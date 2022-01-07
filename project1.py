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

#############################################
# variables related to setting game windows #
#############################################
window_length = 4
squaresize = 100
radius = int(squaresize / 2 - 5)

width = columns * squaresize
height = (rows + 1) * squaresize
size = (width, height)
###############################################


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


def get_next_open_row(board, col):
    for r in range(rows):
        if board[r][col] == 0:
            return r


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


def draw_board(board):
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, blue, (c * squaresize, r *
                             squaresize + squaresize, squaresize, squaresize))
            pygame.draw.circle(screen, black, (
                int(c * squaresize + squaresize / 2), int(r * squaresize + squaresize + squaresize / 2)), radius)

    for c in range(columns):
        for r in range(rows):
            if board[r][c] == player_piece:
                pygame.draw.circle(screen, red, (
                    int(c * squaresize + squaresize / 2), height - int(r * squaresize + squaresize / 2)), radius)
            elif board[r][c] == ai_piece:
                pygame.draw.circle(screen, yellow, (
                    int(c * squaresize + squaresize / 2), height - int(r * squaresize + squaresize / 2)), radius)
    pygame.display.update()


# rows or columns of current game state are given to this function and it will update the score of the possible move accordinly.
def evaluate_window(window, piece):
    # The opponent player is by default set as the user(player)
    opponent_piece = player_piece

    # If the position is being evaluated from the user(player's) point of view than the AI(minimax) is the opponent
    if piece == player_piece:
        opponent_piece = ai_piece
    # Initial score is set to 0
    score = 0

    # If the positions are favourable increase the score variable
    if window.count(piece) == 4:
        score = score+100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score = score+5
    elif window.count(opponent_piece) == 2 and window.count(0) == 2:
        score = score+2

    # If the position is such as the opponent will be able to connect 3 dots then the score will be decreased
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score = score - 4

    return score

# calculating the overall attractiveness of the board after one move has been made
def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list[:, columns//2]]
    center_count = center_array.count(piece)
    score = score+center_count*6

    for r in range(rows):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(columns - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    for c in range(columns):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rows-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    for r in range(3, rows):
        for c in range(columns - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(3, rows):
        for c in range(3, columns):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# Shows the column in which we can drop the piece

def get_valid_locations(board):
    valid_locations = []
    for col in range(columns):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Select the best move by searching the scores of each move

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

board = create_board()
print_board(board)
game_over = False

pygame.init()

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(player, ai)

###################################
#         MAIN FUNCTION           #
###################################

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            posx = event.pos[0]
            if turn == player:
                pygame.draw.circle(
                    screen, red, (posx, int(squaresize / 2)), radius)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == player:
                posx = event.pos[0]
                col = int(math.floor(posx / squaresize))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, player_piece)

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

        if turn == ai and not game_over:

            col = pick_best_move(board, ai_piece)

            if is_valid_location(board, col):
                # pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, ai_piece)

                if winning_move(board, ai_piece):
                    label = myfont.render("Player 2 wins!!", 1, yellow)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)