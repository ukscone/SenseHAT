#!/usr/bin/env python

from sense_hat import SenseHat
from stick import SenseStick
import random, time, colorsys, threading
import numpy as np

KEY_UP = 103
KEY_LEFT = 105
KEY_RIGHT = 106
KEY_DOWN = 108
KEY_ENTER = 28

sense = SenseHat()
joystick = SenseStick()

sense.low_light = True

road = [[0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]]


carX=0
carY=6
score=0
crashed=False

class obstacles(threading.Thread):

    def __init__(self):
        self._stopevent = threading.Event( )
        self._sleepperiod = 0.5
        threading.Thread.__init__(self)

    def run(self):
      global crashed
      while not self._stopevent.isSet( ):
          self.move()
          self.check()
          self.add()
          self.draw()
          self._stopevent.wait(self._sleepperiod)

    def join(self, timeout=None):
          self._stopevent.set( )
          threading.Thread.join(self, timeout)

    def draw(self):
        for y in range(8):
            for x in range(8):
                sense.set_pixel(x,y,0,road[y][x],0)
        sense.set_pixel((carX),(carY),0,0,64 )
        sense.set_pixel((carX)+1,(carY),0,0,64 )
        sense.set_pixel((carX),(carY)+1,0,0,64 )
        sense.set_pixel((carX)+1,(carY)+1,0,0,64)

    def add(self):
        r=random.randrange(0,5)
        if r==1:
            road[0][random.randrange(0,8)]=64

    def move(self):
        for y in range(7,-1,-1):
            for x in range(8):
                road[y][x]=road[y-1][x]

    def crash(self):
      for z in range(10):
        rand_mat = np.random.rand(8,8)
        for y in range(8):
            for x in range(8):
                 h = 0.1 * rand_mat[x, y]
                 s = 0.8
                 v = rand_mat[x, y]
                 rgb = colorsys.hsv_to_rgb(h, s, v)
                 r = int(rgb[0]*255.0)
                 g = int(rgb[1]*255.0)
                 b = int(rgb[2]*255.0)
                 sense.set_pixel(x, y, r, g, b)
        time.sleep(0.01)


    def check(self,timeout=None):
        global carX
        global carY
        global crashed
        global score
        if (road[carY][carX]==64) or (road[carY+1][carX]==64) or (road[carY][carX+1]==64) or (road[carY+1][carX+1]==64):
            self.crash()
            sense.show_message("Game Over\nCrashed")
            sense.show_message("Score: "+str(score))
            self._stopevent.set( )
            crashed=True
        else:
          score=score+1


thread1=obstacles()
thread1.daemon = True
thread1.start()

while True:
    if crashed==True:
      break
    user_input = joystick.read()[1]
    if user_input==KEY_LEFT:
       carX=carX-1
       if carX < 0:
           carX=0
    elif user_input==KEY_RIGHT:
        carX=carX+1
        if carX > 6:
             carX=6
    elif user_input==KEY_ENTER:
        print "exiting"
        break
    else:
        pass

print "exit"
