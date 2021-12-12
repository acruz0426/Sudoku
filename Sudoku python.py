# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pygame
import numpy as np


class Square:

    def __init__(self, surface):
        self.color = (255,255,255)
        self.value = 0
        self.side = 50
        self.left = 0
        self.top = 0
        self.row = 0
        self.col = 0
        self.surface = surface
        self.font = pygame.font.SysFont('Arial', 20)


    def set_coord(self,left,top):
        self.left = left
        self.top = top

    def draw(self, hovered=False, error=False, complete=False):
        if hovered:
            pygame.draw.rect(self.surface, white_dark, pygame.Rect(self.left, self.top, self.side, self.side))

        else:
            pygame.draw.rect(self.surface, self.color, pygame.Rect(self.left, self.top, self.side, self.side))

        if error:
            pygame.draw.rect(self.surface, red, pygame.Rect(self.left, self.top, self.side, self.side))
        
        if complete:
            pygame.draw.rect(self.surface, (0,200,0), pygame.Rect(self.left, self.top, self.side, self.side))

        

        if self.value != 0:    
            self.surface.blit(self.font.render(str(self.value), True, (0,0,0)), (self.left+self.side/2-5, self.top+self.side/2-10))

    def get_value(self):
        return self.value
    
    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def get_position(self):
        return self.row, self.col
    
    def set_value(self, val):
        self.value = val
    
    def is_hover(self, mouseCoord):
        if self.left <= mouseCoord[0] <= self.left+self.side and self.top <= mouseCoord[1] <= self.top+self.side:
            return True
        else:
            return False

class Board:

    def __init__(self, surface):
        self.rows = 9
        self.cols = 9
        self.coord = (120, 120)
        self.surface = surface
        self.board_solution = [[0]*self.cols]*self.rows
        self.board = []
        self.font = pygame.font.SysFont('Arial', 20)

    def get_board_vals(self):
        return self.board
    
    def set_board_value(self, row, col, value):
        self.board[row][col].set_value(value)

    def get_board(self):
        return self.board

    def get_input(self, row, col):
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.KEYDOWN:
                    if evt.key == pygame.K_1:
                        return 1
                    elif evt.key == pygame.K_2:
                        return 2
                    elif evt.key == pygame.K_3:
                        return 3
                    elif evt.key == pygame.K_4:
                        return 4
                    elif evt.key == pygame.K_5:
                        return 5
                    elif evt.key == pygame.K_6:
                        return 6
                    elif evt.key == pygame.K_7:
                        return 7
                    elif evt.key == pygame.K_8:
                        return 8
                    if evt.key == pygame.K_9:
                        return 9
                    if evt.key == pygame.K_BACKSPACE:
                        return 0
    
    def find_empty_spot(self, start=[0,0]):
        for i in range(9):
            for j in range(9):
                if self.board[i][j].value == 0:
                    start = [i,j]
                    return True, start
        return False, start
    
    def backtrack(self, display=False):
        start = [0,0]
        empty, start = self.find_empty_spot(start)
        if (not empty):
            return True
        
        row = start[0]
        col = start[1]

        for i in range(1,10):

            if display:
                self.board[row][col].set_value(i)
                self.board[row][col].draw(complete=True)
                pygame.display.update()
                pygame.time.delay(50)
                self.board[row][col].set_value(0)

            if self.check_square_group(row, col, i) and self.check_row_and_col(row, col, i):
                self.board[row][col].set_value(i)

                #code to display backtrack algorithm
                if display:

                    if self.backtrack(display=True):
                        return True
                else:
                    if self.backtrack():
                        return True
                
                #Calls itself to check further down branch
                
                self.board[row][col].set_value(0)
                
        if display:
            self.board[row][col].draw(error=True)
            pygame.display.update()
            pygame.time.delay(50)          
        return False

    def initialize_board(self):
        
        row_off = 0
        for row in range(self.rows):
            col_off = 0
            inner = []

            if row == 3 or row == 6:
                    row_off += 1
            #loop to add Square to inner list
            for col in range(self.cols):
                s = Square(self.surface)
                s.set_position(row,col)
                
                if col == 3 or col == 6:
                    col_off += 1
                
                s.set_coord(self.coord[0]+col*(s.side+5)+5*col_off, self.coord[1]+row*(s.side+5)+5*row_off)
                inner.append(s)
            
            #appends list of squares to board list
            self.board.append(inner)
        
        for i in range(3):
            for j in range(3):
                while self.board[i][j].value == 0:
                    val = np.random.randint(1,10)
                    if self.check_square_group(i, j, val):
                        self.board[i][j].set_value(val)
        
        for i in range(3,6):
            for j in range(3,6):
                while self.board[i][j].value == 0:
                    val = np.random.randint(1,10)
                    if self.check_square_group(i,j,val):
                        self.board[i][j].set_value(val)
        
        for i in range(6,9):
            for j in range(6,9):
                while self.board[i][j].value == 0:
                    val = np.random.randint(1,10)
                    if self.check_square_group(i,j,val):
                        self.board[i][j].set_value(val)

        self.backtrack()

        for i in range(9):
            for j in range(9):
                prob = np.random.rand()
                self.board_solution[i][j] = self.board[i][j].value
                if prob <= 0.8:
                    self.board[i][j].set_value(0)



        

        



    def check_row_and_col(self, row, col, value):
        if value == 0:
            return True
        #check col
        for r in range(9):
            if r == row:
                continue
            if self.board[r][col].value == value:
                return False
        
        #check row
        for c in range(9):
            if c == col:
                continue
            if self.board[row][c].value == value:
                return False

        return True

    def check_square_group(self, row, col, value):
        r = 7
        c = 7
        if value == 0:
            return True
        if row >= 0 and row <= 2:
            r = 1
        elif row >= 3 and row <= 5:
            r = 4
        if col >= 0 and col <= 2:
            c = 1
        elif col >= 3 and col <= 5:
            c = 4

        for i in range(r-1,r+2):
            for j in range(c-1,c+2):
                if self.board[i][j].value == value:
                    return False

        return True

    def draw_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j].draw() #display board
                





pygame.init() #initializes the pygame constructor

#global variables
isMenu = True
isCompleted = False


#colors
white = (255,255,255)

red = (255,0,0)

white_light = (170,170,170)

white_dark = (100,100,100)

#font
font = pygame.font.SysFont('Arial', 20)

#create canvas
width = 720
height = 720
surface = pygame.display.set_mode((width,height))

#initialize menu buttons width, height, and distance from each other
rect_width = 120
rect_height = 80
padding = 60
#caption canvas
pygame.display.set_caption("Sudoku")

#initialize exit to false
exit = False

board = Board(surface)
board.initialize_board()
#main game loop
while not exit:
    #gets mouse coordinates and stores it into a tuple
    mouse = pygame.mouse.get_pos()

    #checks for events that occur in game
    for event in pygame.event.get():

        #this checks if the event type is pressing the red X at the top corner
        if event.type == pygame.QUIT:
            exit = True


        #This is the menu pathway
        if isMenu:

            #draw start game button
            pygame.draw.rect(surface, white, pygame.Rect(width/2-rect_width/2,height/2-rect_height/2-padding,rect_width,rect_height))
            surface.blit(font.render('Start Game', True, (0,0,0)), (width/2-rect_width/2+8, height/2-rect_height/2-padding/2-5))

            #draw quit button
            pygame.draw.rect(surface, white, pygame.Rect(width/2-rect_width/2,height/2-rect_height/2+padding,rect_width,rect_height))
            surface.blit(font.render('Quit', True, (255,0,0)), (width/2-rect_width/2+40, height/2+rect_height/2+padding/2-20))
            
            #draw start game when hovering
            if width/2-rect_width/2 <= mouse[0] <= width/2+rect_width/2 and height/2-rect_height/2-padding <= mouse[1] <= height/2+rect_height/2-padding:
                pygame.draw.rect(surface, white_dark, pygame.Rect(width/2-rect_width/2,height/2-rect_height/2-padding,rect_width,rect_height))
                surface.blit(font.render('Start Game', True, (0,0,0)), (width/2-rect_width/2+8, height/2-rect_height/2-padding/2-5))

            #draw quit button when hovering
            elif width/2-rect_width/2 <= mouse[0] <= width/2+rect_width/2 and height/2-rect_height/2+padding <= mouse[1] <= height/2+rect_height/2+padding:
                pygame.draw.rect(surface, white_dark, pygame.Rect(width/2-rect_width/2,height/2-rect_height/2+padding,rect_width,rect_height))
                surface.blit(font.render('Quit', True, (255,0,0)), (width/2-rect_width/2+40, height/2+rect_height/2+padding/2-20))

            #check when mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:

                #check if mouse coordinates within button
                if width/2-rect_width/2 <= mouse[0] <= width/2+rect_width/2 and height/2-rect_height/2-padding <= mouse[1] <= height/2+rect_height/2-padding:
                    isMenu = False
                elif width/2-rect_width/2 <= mouse[0] <= width/2+rect_width/2 and height/2-rect_height/2+padding <= mouse[1] <= height/2+rect_height/2+padding:
                    exit = True


        #This is the game pathway
        else:
            surface.fill((0,0,0))
            board.draw_board()
            empty, arr = board.find_empty_spot()

           

            if not empty and not isCompleted:
                pygame.draw.rect(surface, (0,0,0), pygame.Rect(width/2-100, height/2-50, 200, 100))
                surface.blit(font.render('You Win!!!', True, (0,255,0)), (width/2-50, height/2-25))
                continue
            
            for row in board.get_board():
                for square in row:

                    #draw the hovered square
                    square.draw(square.is_hover(mouse))

                    #check if square is clicked
                    if event.type == pygame.MOUSEBUTTONDOWN and square.is_hover(mouse):
                        r = square.get_row()
                        c = square.get_col()
                        val = board.get_input(r, c)
                        if board.check_row_and_col(r, c, val) and board.check_square_group(r, c, val):
                            square.set_value(val)
                        else:
                            square.draw(error=True)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.backtrack(display=True)
                    isCompleted = True 

    pygame.display.update()
pygame.quit()

