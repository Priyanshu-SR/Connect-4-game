import numpy as np
import pygame as pg
import sys
import math

# colours for the board and pieces
black = (0, 0, 0)
grey = (70, 70, 70)
b_red = (255, 75, 75)
cyan = (100, 255, 255)

# number of rows and columns in the board
noOfRows = 6
noOfColumns = 7


def game_board():
    # it creates the game board with certain number of rows and columns
    board = np.zeros((noOfRows, noOfColumns))
    return board


def drop(board, row, col, piece):
    # it place the pieces in the wanted circle,as the board is the form of a matrix so b[i][j] finds the correct position
    board[row][col] = piece


def check_entered_loc(board, col):
    # it simply returns if the pieces can be placed at the entered location or not
    return board[noOfRows - 1][col] == 0


def get_next_row(board, col):
    for r in range(noOfRows):
        if board[r][col] == 0:
            return r


def print__board(board):
    # here we are printing the board
    print(np.flip(board, 0))


def winning(board, piece):
    # check for horizontal winning
    for c in range(noOfColumns-3):
        for r in range(noOfRows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check for vertical winning
    for c in range(noOfColumns):
        for r in range(noOfRows-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # check for +ve slope diagonal
    for c in range(noOfColumns-3):
        for r in range(noOfRows-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # check for -ve slope diagonal
    for c in range(noOfColumns-3):
        for r in range(3, noOfRows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def board_design(board):
    # game board is designed 
    for c in range(noOfColumns):
        for r in range(noOfRows):
            pg.draw.rect(screen, grey, (c*sq_size, r*sq_size + sq_size, sq_size, sq_size), width=0)
            pg.draw.circle(screen, black, (int(c*sq_size + sq_size/2),int(r*sq_size + sq_size + sq_size/2)), radius=int(sq_size/2 - 5))
    # pieces are designed
    for c in range(noOfColumns):
        for r in range(noOfRows):
            if board[r][c] == 1:
                pg.draw.circle(screen, b_red, (int(c*sq_size + sq_size/2), Height-int(r*sq_size + sq_size/2)), radius=int(sq_size/2 - 5))
            elif board[r][c] == 2:
                pg.draw.circle(screen, cyan, (int(c*sq_size + sq_size/2), Height-int(r*sq_size + sq_size/2)), radius=int(sq_size/2 - 5))
    pg.display.update()


board = game_board()
print__board(board)
win = False
turns = 0

# initiating pygames
pg.init()
sq_size = 140             # size of screen in pixels
Width = noOfColumns * sq_size 
Height = (noOfRows+1) * sq_size
size = (Width, Height)
screen = pg.display.set_mode(size)
board_design(board)
pg.display.update()

# displaying player won
win_mess = pg.font.SysFont('times new roman', 90)

while not win:      # loop will run untill win is true i.e. someone wins it
    for event in pg.event.get():                # defining events in pygame
        if event.type == pg.QUIT:          # clicking on Quit button will exit from the game 
            sys.exit()
        if event.type == pg.MOUSEMOTION:     # it will track the movement of the mouse and decide in which column piece will fall
            pg.draw.rect(screen, black, (0, 0, Width, sq_size))
            pos_x = event.pos[0]
            if turns == 0:
                pg.draw.circle(screen, b_red, (pos_x, int(sq_size/2)), radius=int(sq_size/2 - 5))
            else:
                pg.draw.circle(screen, cyan, (pos_x, int(sq_size/2)), radius=int(sq_size/2 - 5))
            pg.display.update()
        if event.type == pg.MOUSEBUTTONDOWN:                # when clicked to particular column piece will fall directly at the bottom
            pg.draw.rect(screen, black, (0, 0, Width, sq_size))
            if turns == 0:
                # Taking input from the player 1
                pos_x = event.pos[0]
                Col = int(math.floor(pos_x/sq_size))
                if check_entered_loc(board, Col):
                    row = get_next_row(board, Col)
                    drop(board, row, Col, 1)
                    if winning(board, 1):
                        print__board(board)
                        label = win_mess.render("Player 1, wins the game...", True, b_red)     # Display Player 1 won
                        screen.blit(label, (30, 15))
                        win = True
            else:
                # Taking input from the player 2
                pos_x = event.pos[0]
                Col = int(math.floor(pos_x/sq_size))
                if check_entered_loc(board, Col):
                    row = get_next_row(board, Col)
                    drop(board, row, Col, 2)
                    if winning(board, 2):
                        print__board(board)
                        label = win_mess.render("Player 2, wins the game...", True, cyan)     # Display Player 2 won
                        screen.blit(label, (30, 15))
                        win = True
            print__board(board)
            board_design(board)
            turns += 1
            turns = turns % 2
            if win:
                pg.time.wait(5000)    # screen remains idle for 5 seconds after game's over
