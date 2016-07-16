#!/usr/bin/env python3

# 2048 code originally from http://www.thetaranights.com/make-a-2048-game-in-python/
# there is a bug/missing logic that needs to be fixed where it will quit the game
# even if there is still a valid move left when the grid is completely full.
# but other than that it works.
# Originally this version used the Pimoroni UnicornHAT as the display. The source of
# which can be found at https://github.com/ukscone/unicornhat/blob/master/uni2048.py
# This version has been ported to use the Raspberry Pi SenseHAT as both the display
# and controls.

from sense_hat import SenseHat
from stick import SenseStick # This file is not in the pip'd SenseHAT install
                             # so include manually from running directory.

import random

sense = SenseHat()
sensestick = SenseStick()

KEY_UP = 103
KEY_LEFT = 105
KEY_RIGHT = 106
KEY_DOWN = 108
KEY_ENTER = 28

grid = [[0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]

index = {0:0,2:1,4:2,8:3,16:4,32:5,64:6,128:7,256:8,512:9,1024:10,2048:11}
colour=((0,0,0),(0,127,0),(0,255,0),(0,0,127),(0,0,255),(127,0,0),(255,0,0),
        (127,127,0),(127,127,127),(255,127,127),(255,255,127),(255,255,255))

def drawTile(y, x, value):
    rgb=colour[(index[value])]
    sense.set_pixel((x*2),(y*2),rgb[0],rgb[1],rgb[2])
    sense.set_pixel((x*2)+1,(y*2),rgb[0],rgb[1],rgb[2])
    sense.set_pixel((x*2),(y*2)+1,rgb[0],rgb[1],rgb[2])
    sense.set_pixel((x*2)+1,(y*2)+1,rgb[0],rgb[1],rgb[2])

def updateGrid(keypressed):
    if keypressed == KEY_UP:
        row=0
        for column in range(0,4):
            if grid[row][column]!=0 or grid[row+1][column]!=0 or grid[row+2][column]!=0 or grid[row+3][column]!=0:
                if grid[row][column]==0:
                    while grid[row][column]==0:
                        grid[row][column]=grid[row+1][column]
                        grid[row+1][column]=grid[row+2][column]
                        grid[row+2][column]=grid[row+3][column]
                        grid[row+3][column]=0
                if grid[row+1][column]==0 and (grid[row+2][column]!=0 or grid[row+3][column]!=0):
                    while grid[row+1][column]==0:

                        grid[row+1][column]=grid[row+2][column]
                        grid[row+2][column]=grid[row+3][column]
                        grid[row+3][column]=0
                if grid[row+2][column]==0 and (grid[row+3][column]!=0):
                    while grid[row+2][column]==0:
                        grid[row+2][column]=grid[row+3][column]
                        grid[row+3][column]=0
        row=0
        for column in range(0,4):
            if grid[row][column]==grid[row+1][column]:
                grid[row][column]=grid[row][column]+grid[row+1][column]
                grid[row+1][column]=grid[row+2][column]
                grid[row+2][column]=grid[row+3][column]
                grid[row+3][column]=0
            if grid[row+1][column]==grid[row+2][column]:
                grid[row+1][column]=grid[row+1][column]+grid[row+2][column]
                grid[row+2][column]=grid[row+3][column]
                grid[row+3][column]=0
            if grid[row+2][column]==grid[row+3][column]:
                grid[row+2][column]=grid[row+2][column]+grid[row+3][column]
                grid[row+3][column]=0



    elif keypressed == KEY_DOWN:
        row=0
        for column in range(0,4):
            if grid[row][column]!=0 or grid[row+1][column]!=0 or grid[row+2][column]!=0 or grid[row+3][column]!=0:
                if grid[row+3][column]==0:
                    while grid[row+3][column]==0:
                        grid[row+3][column]=grid[row+2][column]
                        grid[row+2][column]=grid[row+1][column]
                        grid[row+1][column]=grid[row][column]
                        grid[row][column]=0
                if grid[row+2][column]==0 and (grid[row+1][column]!=0 or grid[row][column]!=0):
                    while grid[row+2][column]==0:
                        grid[row+2][column]=grid[row+1][column]
                        grid[row+1][column]=grid[row][column]
                        grid[row][column]=0

                if grid[row+1][column]==0 and grid[row][column]!=0:
                    while grid[row+1][column]==0:
                        grid[row+1][column]=grid[row][column]
                        grid[row][column]=0
        row=0
        for column in range(0,4):
            if grid[row+3][column]==grid[row+2][column]:
                grid[row+3][column]=grid[row+3][column] + grid[row+2][column]
                grid[row+2][column]=grid[row+1][column]
                grid[row+1][column]=grid[row][column]
                grid[row][column]=0
            if grid[row+2][column]==grid[row+1][column]:
                grid[row+2][column]=grid[row+2][column]+grid[row+1][column]
                grid[row+1][column]=grid[row][column]
                grid[row][column]=0
            if grid[row+1][column]==grid[row][column]:
                grid[row+1][column]=grid[row+1][column]+grid[row][column]
                grid[row][column]=0

    elif keypressed == KEY_LEFT:
        column=0
        for row in range(0,4):

            if grid[row][column]!=0 or grid[row][column+1]!=0 or grid[row][column+2]!=0 or grid[row][column+3]!=0:
                if grid[row][column]==0:
                    while grid[row][column]==0:
                        grid[row][column]=grid[row][column+1]
                        grid[row][column+1]=grid[row][column+2]
                        grid[row][column+2] = grid[row][column+3]
                        grid[row][column+3]=0
                if grid[row][column+1]==0 and (grid[row][column+2]!=0 or grid[row][column+3]!=0):
                    while grid[row][column+1]==0:
                        grid[row][column+1]=grid[row][column+2]
                        grid[row][column+2]=grid[row][column+3]
                        grid[row][column+3]=0
                if grid[row][column+2]==0 and (grid[row][column+3]!=0):
                    while grid[row][column+2]==0:
                        grid[row][column+2]=grid[row][column+3]
                        grid[row][column+3]=0
        column=0
        for row in range(0,4):
            if grid[row][column]==grid[row][column+1]:
                grid[row][column]=grid[row][column]+grid[row][column+1]
                grid[row][column+1]=grid[row][column+2]
                grid[row][column+2]=grid[row][column+3]
                grid[row][column+3]=0
            if grid[row][column+1]==grid[row][column+2]:
                grid[row][column+1]=grid[row][column+1]+grid[row][column+2]
                grid[row][column+2]=grid[row][column+3]
                grid[row][column+3]=0
            if grid[row][column+2]==grid[row][column+3]:
                grid[row][column+2]=grid[row][column+2]+grid[row][column+3]
                grid[row][column+3]=0
    elif keypressed == KEY_RIGHT:
        column=0
        for row in range(0,4):
            if grid[row][column]!=0 or grid[row][column+1]!=0 or grid[row][column+2]!=0 or grid[row][column+3]!=0:
                if grid[row][column+3]==0:
                    while grid[row][column+3]==0:
                        grid[row][column+3]=grid[row][column+2]
                        grid[row][column+2]=grid[row][column+1]
                        grid[row][column+1]=grid[row][column]
                        grid[row][column]=0
                if grid[row][column+2]==0 and (grid[row][column+1]!=0 or grid[row][column]!=0):
                    while grid[row][column+2]==0:
                        grid[row][column+2]=grid[row][column+1]
                        grid[row][column+1]=grid[row][column]
                        grid[row][column]=0

                if grid[row][column+1]==0 and grid[row][column]!=0:
                    while grid[row][column+1]==0:
                        grid[row][column+1]=grid[row][column]
                        grid[row][column]=0
        column=0
        for row in range(0,4):
            if grid[row][column+3]==grid[row][column+2]:
                grid[row][column+3]=grid[row][column+3] + grid[row][column+2]
                grid[row][column+2]=grid[row][column+1]
                grid[row][column+1]=grid[row][column]
                grid[row][column]=0
            if grid[row][column+2]==grid[row][column+1]:
                grid[row][column+2]=grid[row][column+2]+grid[row][column+1]
                grid[row][column+1]=grid[row][column]
                grid[row][column]=0
            if grid[row][column+1]==grid[row][column]:
                grid[row][column+1]=grid[row][column+1]+grid[row][column]
                grid[row][column]=0


grid[random.choice([0,1,2,3])][random.choice([0,1,2,3])]=2

while True:
    for y in range(4):
        for x in range(4):
           drawTile(y,x,grid[y][x])

    keypressed=""
    while keypressed=="":
        keypressed  = sensestick.read()[1]
       # print keypressed 
        if (keypressed!=KEY_UP) and (keypressed!=KEY_DOWN) and (keypressed!=KEY_LEFT) and (keypressed!=KEY_RIGHT) and (keypressed!=KEY_ENTER):
            keypressed=""

    if keypressed!=KEY_ENTER:
        updateGrid(keypressed)
        listForRow = []
        listForColumnn = []
        count = 0
        for row in range(0,4):
            for column in range(0,4):
                if grid[row][column]==0:
                    count+=1
                    listForRow.append(row)
                    listForColumnn.append(column)
        if count > 0:
            if count > 1:
                randomIndex = listForRow.index(random.choice(listForRow))
                grid[listForRow[randomIndex]][listForColumnn[randomIndex]]=2
            else:
                grid[listForRow[0]][listForColumnn[0]]=2
        else:
            break
    else:
        break
sense.show_message("Game over")
