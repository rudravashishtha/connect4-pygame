import numpy as np
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece    

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        
# def display_board(board):
#     print(np.flip(board, 0))
    
def winning_move(board, piece):
    # Check horizontal positions
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if (board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece):
                return True
            
    # Check vertical positions
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if (board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece):
                return True
            
    # Check Positively sloped diagnols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if (board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece):
                return True
    
    # Check Negatively sloped diagnols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece):
                return True
    

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                circle_center = (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2))
                pygame.draw.circle(screen, RED, circle_center, RADIUS)
                text_surface = myFont.render("1", True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.center = circle_center
                screen.blit(text_surface, text_rect)
            elif board[r][c] == 2:
                circle_center = (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2))
                pygame.draw.circle(screen, YELLOW, circle_center, RADIUS)
                text_surface = myFont.render("2", True, (0, 0, 0))
                text_rect = text_surface.get_rect()
                text_rect.center = circle_center
                screen.blit(text_surface, text_rect)
            
            
    pygame.display.update()

board = create_board()
# display_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 90

width = COLUMN_COUNT * (SQUARESIZE)
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)
myFont = pygame.font.Font(None, 40)


screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect4")
draw_board(board)

pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            
            pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    
                    if winning_move(board, turn+1):
                        label = myFont.render(f"Player {turn+1} Wins!! Congratulations!", True, RED)
                        screen.blit(label, (80, 35))
                        game_over = True
                
                
                
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    
                    if winning_move(board, turn+1):
                        label = myFont.render(f"Player {turn+1} Wins!! Congratulations!", True, YELLOW)
                        screen.blit(label, (80, 35))
                        game_over = True
                        
            # display_board(board)
            draw_board(board)
            
            turn += 1
            turn %= 2
            
            if game_over:
                pygame.time.wait(3000)
