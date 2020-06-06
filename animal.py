from threading import Thread, Lock
from enum import Enum
from math import sqrt
import random
import time
import queue

class Moves(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Animal(Thread):
    def __init__(self, x: int, y: int, occupancy_queue: queue, ponds: list):
        Thread.__init__(self)

        self.occupancy_queue = occupancy_queue

        self.alive = True

        self.food = 100
        self.water = 100
        self.sleep = 100
        self.need_for_reproduction = 100

        self.x = x
        self.y = y

        self.ponds = ponds

        self.is_reproducing = False
        self.ready_to_reproduce = False

        self.time_s = None
        self.random_x = random.randrange(0, 31)
        self.random_y = random.randrange(0, 17)

    def update_needs(self):
        self.food -= 2
        self.water -= 1
        self.sleep -= 1
        self.need_for_reproduction -= 2

        if self.food < 1 or self.water <1:
            #stań sie ciałem
            self.alive = False

            self.update_occupancy_map(self.x, self.y, 0)

        # if self.sleep < 1:
        #     time.sleep(1.5, 3.0)
        #     self.sleep = 200



    def get_position(self) -> (int, int):
        """Returning the current animal position.
        Used by the board to redraw their positions"""
        return self.x, self.y


    def wander(self):
        """Wanders aimlessy when all needs are fulfilled"""
        if self.time_s is None:
            self.random_x, self.random_y = random.randrange(0, 32), random.randrange(0, 18)
            self.time_s = time.perf_counter()

        elif (time.perf_counter() - self.time_s) > 5:
            self.random_x, self.random_y = random.randrange(0, 32), random.randrange(0, 18)
            self.time_s = time.perf_counter()

        self.move(self.random_x, self.random_y)


    def look_for_water(self):
        nearest_pond = self.get_pond_pos()

        self.move(nearest_pond.x, nearest_pond.y)

        if self.calculate_distance(nearest_pond.x, self.x, nearest_pond.y, self.y) == 1:
            
            if nearest_pond.lock.acquire(True):

                self.update_occupancy_map(self.x, self.y, 0)

                self.x = nearest_pond.x
                self.y = nearest_pond.y

                time.sleep(random.uniform(1.5, 3.0))

                self.water = 100

                nearest_pond.lock.release()

    def get_pond_pos(self):
        dist = 10000
        for pond in self.ponds:
            new_dist = self.calculate_distance(self.x, pond.x, self.y, pond.y)
            if new_dist < dist:
                dist = new_dist
                nearest_pond = pond
        return nearest_pond

    def update_occupancy_map(self, x: int, y: int, resource: int):
        occupancy_map = self.occupancy_queue.get(True)
        occupancy_map[x, y] = resource
        self.occupancy_queue.put(occupancy_map)

        #Searching for the fastest move to get to the x,y destination
    # def move(self, x, y):    
    #     best_distance = None
    #     best_move = None 

    #     #Going right
    #     new_x = self.x+1
    #     new_y = self.y

    #     with self.lock:
    #         occupancy_map = self.occupancy_queue.get()

    #         if (new_x >= 0 and new_x < 31) and (new_y >= 0 and new_y < 17): 
    #             occupancy = occupancy_map[new_x, new_y]  
    #             if occupancy == 0:
    #                 going_right = self.calculate_distance(new_x, x, new_y, y)
    #                 best_distance = going_right
    #                 best_move = Moves.RIGHT.name
            
    #         #Going left
    #         new_x = self.x-1
    #         new_y = self.y

    #         if (new_x >= 0 and new_x < 31) and (new_y >= 0 and new_y < 17):
    #             occupancy = occupancy_map[new_x, new_y]  
                
    #             if occupancy==0:
    #                 going_left = self.calculate_distance(new_x, x, new_y, y)
    #                 if best_distance is None:
    #                     best_distance = going_left
    #                     best_move = Moves.LEFT.name
    #                 elif best_distance > going_left:
    #                         best_distance = going_left
    #                         best_move = Moves.LEFT.name
            
    #         #Going up
    #         new_x = self.x
    #         new_y = self.y-1


    #         if (new_x >= 0 and new_x < 31) and (new_y >= 0 and new_y < 17):
    #             occupancy = occupancy_map[new_x, new_y]  
                
    #             if occupancy==0:
    #                 going_up = self.calculate_distance(new_x, x, new_y, y)
    #                 if best_distance is None:
    #                     best_distance = going_up
    #                     best_move = Moves.UP.name
    #                 elif best_distance > going_up:
    #                         best_distance = going_up
    #                         best_move = Moves.UP.name

    #         #Going down
    #         new_x = self.x
    #         new_y = self.y+1

    #         if (new_x >= 0 and new_x < 31) and (new_y >= 0 and new_y < 17):
    #             occupancy = occupancy_map[new_x, new_y]  
                
    #             if occupancy==0:
    #                 going_down = self.calculate_distance(new_x, x, new_y, y)
    #                 if best_distance is None:
    #                     best_distance = going_down
    #                     best_move = Moves.DOWN.name
    #                 elif best_distance > going_down:
    #                         best_distance = going_down
    #                         best_move = Moves.DOWN.name

    #         #Current position actualization
    #         if best_move is Moves.RIGHT.name:
    #             self.x+=1
    #         elif best_move is Moves.LEFT.name:
    #             self.x-=1
    #         elif best_move is Moves.UP.name:
    #             self.y-=1
    #         elif best_move is Moves.DOWN.name:
    #             self.y+=1

    #         if isinstance(self, Herbivore):
    #             occupancy_map[self.x, self.y] = 4

    #         elif isinstance(self, Carnivore):
    #             occupancy_map[self.x, self.y] = 4

    #         self.occupancy_queue.put(occupancy_map)

        #Pythagorean theorem
        #Usefull for calculating the fastest move
    def calculate_distance(self, x1, x2, y1, y2):
        return (x1-x2)**2 + (y1-y2)**2
