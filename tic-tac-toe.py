import pygame as pg, sys
import numpy as np

pg.init()

#declare constant 

WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = BOARD_ROWS
SQUARE_SIZE = WIDTH//BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE//3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE//4

#color
RED = (255,0,0)
BK_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200) 
CROSS_COLOR = (66, 66, 66)


#variable
player = 1
game_over = False

#Set Screen
screen = pg.display.set_mode((WIDTH, HEIGHT)) #set screen size
pg.display.set_caption("TIC-TAC-TOE") #set title of window
screen.fill(BK_COLOR) #set background color

#board
board = np.zeros((BOARD_ROWS,BOARD_COLS))



#Function to draw lines
def draw_lines():
    pg.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE),     (WIDTH, SQUARE_SIZE),     LINE_WIDTH) #First Horizontal line
    pg.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * 2), (WIDTH, SQUARE_SIZE * 2), LINE_WIDTH) #Second Horizontal line
    pg.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0),     (SQUARE_SIZE, HEIGHT),     LINE_WIDTH) #First Verticle line
    pg.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * 2, 0), (SQUARE_SIZE * 2, HEIGHT), LINE_WIDTH) #Second Verticle line
draw_lines()


# mark the row or col for the player
def mark_square(row, col, player):
    board[row][col] = player

#return True if the board is not marked else False
def available_square(row, col):
    return (board[row][col] == 0)


#Return True if the board is Full (i.e.  no place to mark) else False
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

# Add Circle and Cross on player click        
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1 :
                pg.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            if board[row][col] == 2 :
                pg.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pg.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

# Return True if the player won else False
def check_win(player):
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True
        
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True
    
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True
    
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True
    return False

#draw verticle line after winning
def draw_vertical_winning_line(col,player):
    posX = col * SQUARE_SIZE + 100
    if(player == 1):
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pg.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)

#draw horizontal line after winning
def draw_horizontal_winning_line(row,player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    if(player == 1):
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pg.draw.line(screen, color, (15, posY), ( WIDTH - 15,posY), 15)

#draw Ascending line after winning
def draw_asc_diagonal(player):
    if(player == 1):
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    pg.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)    

#draw Descending line after winning
def draw_desc_diagonal(player):
    color = CIRCLE_COLOR
    if player == 2:
        color = CROSS_COLOR
    pg.draw.line(screen, color, (15, 15), (HEIGHT - 15, WIDTH - 15), 15)   

# function to reset to start
def restart():
    screen.fill(BK_COLOR) #set background color
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

#MAIN LOOP
while True:
    #loop to check is any event is occured in the window
    for event in pg.event.get():
        #close th window if we click on close button
        if event.type == pg.QUIT:
            sys.exit()

        # checking and storing the coordinate of mouse click event
        if event.type == pg.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] #mouse X coordinate
            mouseY = event.pos[1] #mouse Y coordinate
            
            # get the row and column in which we clicked (ie. row and column)
            clicked_row = int(mouseX // SQUARE_SIZE)
            clicked_col = int(mouseY // SQUARE_SIZE)
            
            #mark if the box is available 
            if available_square(clicked_col, clicked_row):

                mark_square(clicked_col, clicked_row, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

            draw_figures()
            if is_board_full():
                print("TIE")

        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            restart()
            game_over = False
    pg.display.update()