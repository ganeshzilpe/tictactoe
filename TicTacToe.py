#-------------------------------------------------------------------------------
# Name:        TicTacToe
# Purpose:     To learn making of the game in python with pygame and tkinter
#
# Author:      Ganesh Zilpe
#
# Created:     08/06/2015
# Copyright:   (c) Dev1 2015
# Licence:     Freely Available
#-------------------------------------------------------------------------------

import random, pygame, sys
import Tkinter as tk
import os

import tkMessageBox
from pygame.locals import *



computer = 'o'
player = 'x'
WINDOWWIDTH = 540 # size of window's width in pixels
WINDOWHEIGHT = 380
BOARDWIDTH = 3
BOARDHEIGHT = 3
BOXSIZE = 60 # size of box height & width in pixels
GAPSIZE = 10
#assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)


 #            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE


root = tk.Tk()
root.title("TicTacToe")
embed = tk.Frame(root, width=WINDOWWIDTH, height=WINDOWHEIGHT)
embed.pack()

    # Tell pygame's SDL window which window ID to use
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

    # The wxPython wiki says you might need the following line on Windows
    # (http://wiki.wxpython.org/IntegratingPyGame).
    #os.environ['SDL_VIDEODRIVER'] = 'windib'

    # Show the window so it's assigned an ID.
root.update()
pygame.display.init()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))



def convetXYtoPosition(x,y):
    if x == 0 and y == 0:
        return 1
    elif x == 0 and y == 1:
        return 2
    elif x == 0 and y == 2:
        return 3
    elif x == 1 and y == 0:
        return 4
    elif x == 1 and y == 1:
        return 5
    elif x == 1 and y == 2:
        return 6
    elif x == 2 and y == 0:
        return 7
    elif x == 2 and y == 1:
        return 8
    elif x == 2 and y == 2:
        return 9

def convetPositiontoXY(position):
    if position==1:
        return (0, 0)
    elif position==2:
        return (0, 1)
    elif position==3:
        return (0, 2)
    elif position==4:
        return (1, 0)
    elif position==5:
        return (1, 1)
    elif position==6:
        return (1, 2)
    elif position==7:
        return (2, 0)
    elif position==8:
        return (2, 1)
    elif position==9:
        return (2, 2)


def getNewBoard():
     # Creates a brand new, blank board data structure.
     board = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
     return board

def getDuplicateSnapshot(snapshot):
    snapshot1 =[]
    for i in snapshot:
        snapshot1.append(i)
    return snapshot1

def isPositionAvailable(snapshot, position):
    if(snapshot[position] == ' '):
        return True
    else:
        return False

def chooseCornerMoves(snapshot):
    moves = []
    corner_list = [1,3,7,9]
    for i in corner_list:
        if isPositionAvailable(snapshot, i):
            moves.append(i)
    if len(moves) != 0:
        return random.choice(moves)
    else:
        return None

def chooseSideMoves(snapshot):
    moves = []
    corner_list = [2,4,6,8]
    for i in corner_list:
        if isPositionAvailable(snapshot, i):
            moves.append(i)
    if len(moves) != 0:
        return random.choice(moves)
    else:
        return None

def makeMove(snapshot, turn, position):
    snapshot[int(position)] = turn

def turnSelection():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def winnnerDecision(snapshot, turn):
    if (snapshot[7]== turn and snapshot[8]== turn and snapshot[9]== turn) or \
    (snapshot[4]== turn and snapshot[5]== turn and snapshot[6]== turn) or \
    (snapshot[1]== turn and snapshot[2]== turn and snapshot[3]== turn) or \
    (snapshot[7]== turn and snapshot[4]== turn and snapshot[1]== turn) or \
    (snapshot[8]== turn and snapshot[5]== turn and snapshot[2]== turn) or \
    (snapshot[9]== turn and snapshot[6]== turn and snapshot[3]== turn) or \
    (snapshot[7]== turn and snapshot[5]== turn and snapshot[3]== turn) or \
    (snapshot[9]== turn and snapshot[5]== turn and snapshot[1]== turn) :
        return True
    else:
        return False

def makeComputerMove(snapshot):
    i=1
    #check computer win with this move
    while i < 10:
        snapshot1= getDuplicateSnapshot(snapshot)
        if isPositionAvailable(snapshot1, i):
            makeMove(snapshot1, computer, i)
            if winnnerDecision(snapshot1, computer):
                return i
        i += 1

    i=1
    #check player win with next move, if yes then block the move
    while i < 10:
        snapshot1= getDuplicateSnapshot(snapshot)
        if isPositionAvailable(snapshot1, i):
            makeMove(snapshot1, player, i)
            if winnnerDecision(snapshot1, player):
                return i
        i += 1
    move = chooseCornerMoves(snapshot)
    if move != None:
        return move

    if isPositionAvailable(snapshot, 5):
        return 5
    return chooseSideMoves(snapshot)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def leftTopCoordsOfBox(boxx, boxy):
     # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def drawBoard(board):
     # Draws all of the boxes in their covered or revealed state.
     i=1
     for i in range(1,10):
        boxx, boxy = convetPositiontoXY(i)
        left, top = leftTopCoordsOfBox(boxx, boxy)
        if board[i] ==' ':
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
        elif board[i] =='x':
            # Draw the (revealed) icon.
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.line (DISPLAYSURF, BLACK, (left, top), (left+BOXSIZE, top+BOXSIZE), 3)
            pygame.draw.line (DISPLAYSURF, BLACK, (left, top+BOXSIZE), (left+BOXSIZE, top), 3)
        else:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.circle(DISPLAYSURF, BLACK, (left+BOXSIZE/2, top+BOXSIZE/2), BOXSIZE/4, 0)

def isBoardFull(board):
     # Return True if every space on the board has been taken. Otherwise return False.
     for i in range(1, 10):
         if isPositionAvailable(board, i):
             return False
     return True

def main():


    DISPLAYSURF.fill(BGCOLOR)
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    turn = turnSelection()
    mouseClicked = False

    mainBoard = getNewBoard()
    print mainBoard
    drawBoard(mainBoard)
    pygame.display.update()
    root.update()

    while True:
        if turn == 'player':
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            if boxx != None and boxy != None:
                if mouseClicked:
                    position = convetXYtoPosition(boxx, boxy)
                    makeMove(mainBoard, 'x', position)
                    mouseClicked = False
                    if winnnerDecision(mainBoard, 'x'):
                        #drawBoard(mainBoard)
                        print('The player won.')
                        gameIsPlaying = False
                        drawBoard(mainBoard)
                        pygame.display.update()
                        root.update()
                        result = tkMessageBox.askquestion("Result", "Player won !!!!\n Do you want to play again?", icon='warning')
                        if result == 'yes':
                            main()
                        else:
                            root.destroy();
                            sys.exit()
                        break;
                    else:
                        if isBoardFull(mainBoard):
                            #drawBoard(mainBoard)
                            print('The game is a tie!')
                            drawBoard(mainBoard)
                            pygame.display.update()
                            result = tkMessageBox.askquestion("Result", "It is tie. \n Do you want to play again?", icon='warning')
                            if result == 'yes':
                                main()
                            else:
                                root.destroy();
                                sys.exit()
                                break
                        else:
                            turn = 'computer'

        else:
            position = makeComputerMove(mainBoard)
            makeMove(mainBoard, 'o', position)
            if winnnerDecision(mainBoard, 'o'):
                #drawBoard(mainBoard)
                print('The Computer won.')
                gameIsPlaying = False
                drawBoard(mainBoard)
                pygame.display.update()
                root.update()
                result = tkMessageBox.askquestion("Result", "Computer won !!!!\n Do you want to play again?", icon='warning')
                if result == 'yes':
                    main()
                else:
                    root.destroy();
                    sys.exit()
                break
            else:
                if isBoardFull(mainBoard):
                    #drawBoard(mainBoard)
                    print('The game is a tie!')
                    drawBoard(mainBoard)
                    pygame.display.update()
                    root.update()
                    result = tkMessageBox.askquestion("Result", "It is tie. \n Do you want to play again?", icon='warning')
                    if result == 'yes':
                        main()
                    else:
                        root.destroy();
                        sys.exit()
                    break
                else:
                    turn = 'player'
        drawBoard(mainBoard)
        pygame.display.update()
        root.update()

        #sys.exit()


main()
