# -*- coding: utf-8 -*-
import numpy as np
import pygame
import sys
import math
import random
"""
This is an attempt at connect 4, first without Pygames 
and then when the concept is worked out I'll add the graphics.
This is based on a work on youtube by Keith Galli 
"""

ROW_COUNT=6
COLUMN_COUNT=7

BLUE = (0,0,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
PLAYER = 0
AI = 1
WINDOW_LENGTH = 4
PLAYER_PIECE =1
AI_PIECE=2
EMPTY=0


def create_board():
    ''' creates the board
    '''
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col]==0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r 

def drop_piece(board, col, row, piece):
    #print("ok")
    board[row][col] = piece

def print_board(board):
    print(np.flip(board,0))
    
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, \
                                            r*SQUARESIZE+SQUARESIZE,\
                                            SQUARESIZE, SQUARESIZE ))
            pygame.draw.circle(screen, BLACK,(int(c*SQUARESIZE+RADIUS),\
                                              int(r*SQUARESIZE+SQUARESIZE+\
                                            SQUARESIZE/2)), int(RADIUS))                 
            
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==1:
                pygame.draw.circle(screen, RED,(int(c*SQUARESIZE+RADIUS),\
                                          height-int(r*SQUARESIZE+\
                                        SQUARESIZE/2)), int(RADIUS))
            elif board[r][c]==2:
                pygame.draw.circle(screen, YELLOW,\
                                   (int(c*SQUARESIZE+RADIUS),\
                                          height-int(r*SQUARESIZE+\
                                        SQUARESIZE/2)), int(RADIUS))
    pygame.display.update()
    
        
def winning_move(board, piece):
    #horizontal combinations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and \
                board[r][c+1] == piece and \
                board[r][c+2] == piece and \
                board[r][c+3] == piece:
                return True
     
    #vertical combinations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and \
                board[r+1][c] == piece and \
                board[r+2][c] == piece and \
                board[r+3][c] == piece:
                return True   
            
    #negatively slope diagonal 
    for c in range(COLUMN_COUNT-3):
         for r in range(3, ROW_COUNT):
             if board[r][c] == piece and \
                board[r-1][c+1] == piece and \
                board[r-2][c+2] == piece and \
                board[r-3][c+3] == piece:
                 return True   
             
     # positively slope diagonal
    for c in range(COLUMN_COUNT-3):
         for r in range(ROW_COUNT-3):
             if board[r][c] == piece and \
                board[r+1][c+1] == piece and \
                board[r+2][c+2] == piece and \
                board[r+3][c+3] == piece:
                 return True

def score_position(board, piece):
    # horizontal
    score=0
    for r in range(ROW_COUNT):
        row_array=[int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10
    # vertical
    for c in range(COLUMN_COUNT):
        column_array=[int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = column_array[r:r+WINDOW_LENGTH]
            
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10           
                
    # positive slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window=[board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10     
                
                
                
                
    return score
    
def get_valid_locations(board):
    valid_locations=[]
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
        
    return valid_locations
    
def pick_best_move(board,piece):
    valid_locations=get_valid_locations(board)
    best_col=random.choice(valid_locations)
    best_score=0
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, col, row, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
            
    return best_col
        

board = create_board()
print_board(board)
#turn=0
game_over=False
turn=random.randint(PLAYER, AI)
pygame.init()
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1)* SQUARESIZE
size= (width, height)
RADIUS=int(SQUARESIZE/2 -5)
screen= pygame.display.set_mode(size)
myFont=pygame.font.SysFont("monospace", 75)
draw_board(board)
pygame.display.update()

while not game_over:
    #new pygame code
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type== pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE ))
            posx= event.pos[0]
            if turn==0:
                pygame.draw.circle \
                    (screen, RED, (posx,int(SQUARESIZE/2)),RADIUS)
            else:
                pygame.draw.circle \
                    (screen, YELLOW, (posx,int(SQUARESIZE/2)),RADIUS)
            pygame.display.update()
             
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE ))
            if turn == PLAYER:
                posx= event.pos[0]
                col= int(math.floor(posx/SQUARESIZE))
                if is_valid_location(board, col):
                    row= get_next_open_row(board, col)
                    drop_piece(board, col, row, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        label=myFont.render("Player 1 wins!",1,RED)
                        screen.blit(label,(40,10))
                        game_over=True
                    turn+=1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)
                    
    if turn == AI and not game_over:
        #col=random.randint(0, COLUMN_COUNT-1)
        col=pick_best_move(board, AI_PIECE)
        if is_valid_location(board, col):
            pygame.time.wait(500)
            row= get_next_open_row(board, col)
            drop_piece(board, col, row, AI_PIECE)
            if winning_move(board, AI_PIECE):
                print("Player 2 WINS!! ")
                label=myFont.render("Player 2 wins!",1,YELLOW)
                screen.blit(label,(40,10))
                game_over=True                
            turn+=1
            turn = turn % 2
            print_board(board)
            draw_board(board)
    if game_over:
        pygame.time.wait(3000)
        pygame.quit()
                
        
        
    
