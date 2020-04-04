from threading import Thread, Lock
from enum import Enum
from math import sqrt
import random
import time

class moves(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Animal(Thread):
    def __init__(self, x: int, y: int, fairyland: list, fairy_lock: Lock):
        Thread.__init__(self)

        self.alive = True

        self.x = x
        self.y = y

        self.fairyland = fairyland
        self.lock = fairy_lock

        self.time_s = time.perf_counter()
        self.random_x = random.randrange(0, 31)
        self.random_y = random.randrange(0, 17)

    def run(self):
        pass
            
        #Returning the current animal position. 
        #Used by the board to redraw their positions
    def get_position(self):
        return self.x, self.y

        #Searching for the fastest move to get to the x,y destination
    def move(self, x, y):    
        best_distance = None
        best_move = None 

        #Going right
        new_x = self.x+1
        new_y = self.y

        if (new_x >= 0 and new_x < 31) and (new_y >= 0 and new_y < 17):
            with self.lock:
                occupancy = self.fairyland[new_x, new_y]
            
            if occupancy == 0:
                going_right = self.calculate_distance(new_x, x, new_y, y)
                best_distance = going_right
                best_move = moves.RIGHT.name
        
        #Going left
        new_x = self.x-1
        new_y = self.y

        if (new_x >= 0 and new_x <= 31) and (new_y >= 0 and new_y <= 17):
            with self.lock:
                occupancy = self.fairyland[new_x, new_y]
            
            if occupancy==0:
                going_left = self.calculate_distance(new_x, x, new_y, y)
                if best_distance is None:
                    best_distance = going_left
                    best_move = moves.LEFT.name
                elif best_distance > going_left:
                        best_distance = going_left
                        best_move = moves.LEFT.name
        
        #Going up
        new_x = self.x
        new_y = self.y-1

        if (new_x >= 0 and new_x <= 31) and (new_y >= 0 and new_y <= 17):
            with self.lock:
                occupancy = self.fairyland[new_x, new_y]
            
            if occupancy==0:
                going_up = self.calculate_distance(new_x, x, new_y, y)
                if best_distance is None:
                    best_distance = going_up
                    best_move = moves.UP.name
                elif best_distance > going_up:
                        best_distance = going_up
                        best_move = moves.UP.name

        #Going down
        new_x = self.x
        new_y = self.y+1

        if (new_x >= 0 and new_x <= 31) and (new_y >= 0 and new_y <= 17):
            with self.lock:
                occupancy = self.fairyland[new_x, new_y]
            
            if occupancy==0:
                going_down = self.calculate_distance(new_x, x, new_y, y)
                if best_distance is None:
                    best_distance = going_down
                    best_move = moves.DOWN.name
                elif best_distance > going_down:
                        best_distance = going_down
                        best_move = moves.DOWN.name

        #Current position actualization
        if best_move is moves.RIGHT.name:
            self.x+=1
        elif best_move is moves.LEFT.name:
            self.x-=1
        elif best_move is moves.UP.name:
            self.y-=1
        elif best_move is moves.DOWN.name:
            self.y+=1

        #Pythagorean theorem
        #Usefull for calculating the fastest move
    def calculate_distance(self, x1, x2, y1, y2):
        return sqrt((x1-x2)**2 + (y1-y2)**2)

