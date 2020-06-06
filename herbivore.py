import random
import time
from animal import Animal, Moves
import math
from threading import Lock
import queue

class Herbivore(Animal):
    def __init__(self, x: int, y: int, occupancy_queue: queue, ponds: list, trees: list, caves: list):
        super(Herbivore, self).__init__(x, y, occupancy_queue, ponds)
        self.herbivores = None
        self.trees = trees
        self.caves = caves
        self.herbivore_lock = Lock()

    def run(self):

        while(self.alive):

            if not self.is_reproducing:

                self.update_needs()

                if self.food < 50:
                    self.look_for_food()
                elif self.water < 50:
                    self.look_for_water()
                elif self.sleep < 50:
                    self.look_for_cave()
                elif self.need_for_reproduction < 50:
                    self.reproduce()
                else:
                    self.wander()

            time.sleep(0.3)

    def get_food_pos(self):
        dist = 10000
        for tree in self.trees:
            new_dist = self.calculate_distance(self.x,tree.x,self.y,tree.y)
            if new_dist < dist:
                dist = new_dist
                nearest_tree = tree
        return nearest_tree

    def look_for_food(self):
        nearest_tree = self.get_food_pos()

        self.move(nearest_tree.x, nearest_tree.y)

        if self.calculate_distance(nearest_tree.x, self.x, nearest_tree.y, self.y) == 1:
            
            if nearest_tree.lock.acquire(True):

                self.update_occupancy_map(self.x, self.y, 0)

                self.x = nearest_tree.x
                self.y = nearest_tree.y

                time.sleep(random.uniform(1.5, 3.0))

                self.food = 100

                nearest_tree.lock.release()

    def get_cave_pos(self) -> (int, int):
        dist = 10000
        for cave in self.caves:
            new_dist = self.calculate_distance(self.x,cave.x,self.y,cave.y)
            if new_dist < dist:
                dist = new_dist
                nearest_cave = cave
        return nearest_cave

    def look_for_cave(self):
        nearest_cave = self.get_cave_pos()

        self.move(nearest_cave.x, nearest_cave.y)

        if self.calculate_distance(nearest_cave.x, self.x, nearest_cave.y, self.y) == 1:
            
            if nearest_cave.lock.acquire(True):

                self.update_occupancy_map(self.x, self.y, 0)

                self.x = nearest_cave.x
                self.y = nearest_cave.y

                time.sleep(random.uniform(1.5, 3.0))

                self.sleep = 100

                nearest_cave.lock.release()

    def get_herbivore_pos(self) -> Animal:
        dist = 10000
        nearest_herbivore = None
        for herbivore in self.herbivores:
            if herbivore.x != self.x and herbivore.y != self.y:
                new_dist = self.calculate_distance(self.x,herbivore.x,self.y, herbivore.y)
                if new_dist < dist:
                    dist = new_dist
                    nearest_herbivore = herbivore
        return nearest_herbivore

    def reproduce(self):
        nearest_herbivore = self.get_herbivore_pos()
        if nearest_herbivore is None:
            return

        self.move(nearest_herbivore.x, nearest_herbivore.y)

        if self.calculate_distance(nearest_herbivore.x, self.x, nearest_herbivore.y, self.y) == 1:

            if nearest_herbivore.herbivore_lock.acquire(False):

                self.update_occupancy_map(self.x, self.y, 0)

                self.x = nearest_herbivore.x
                self.y = nearest_herbivore.y

                nearest_herbivore.is_reproducing = True
                self.is_reproducing = True

                time.sleep(random.uniform(1.5, 3.0))

                self.ready_to_reproduce = True
                self.need_for_reproduction = 100
                nearest_herbivore.need_for_reproduction = 100

                nearest_herbivore.herbivore_lock.release()
            else:
                self.wander()

        nearest_herbivore.is_reproducing = False
        self.is_reproducing = False

    def move(self, x, y):    
        best_distance = None
        best_move = None 

        old_x = self.x
        old_y = self.y
        old_resource = 0

        #Going right
        new_x = self.x+1
        new_y = self.y

        occupancy_map = self.occupancy_queue.get(True)

        if occupancy_map[self.x, self.y] != 4:
            old_resource = occupancy_map[self.x, self.y]

        if (new_x >= 0 and new_x < 31) and (new_y >= 0 and new_y < 17): 
            occupancy = occupancy_map[new_x, new_y]  
            if occupancy == 0:
                going_right = self.calculate_distance(new_x, x, new_y, y)
                best_distance = going_right
                best_move = Moves.RIGHT.name
            
        #Going left
        new_x = self.x-1
        new_y = self.y

        if (new_x >= 0 and new_x < 31) and (new_y >= 0 and new_y < 17):
            occupancy = occupancy_map[new_x, new_y]  
                
            if occupancy==0:
                going_left = self.calculate_distance(new_x, x, new_y, y)
                if best_distance is None:
                    best_distance = going_left
                    best_move = Moves.LEFT.name
                elif best_distance > going_left:
                        best_distance = going_left
                        best_move = Moves.LEFT.name
            
        #Going up
        new_x = self.x
        new_y = self.y-1


        if (new_x >= 0 and new_x < 31) and (new_y >= 0 and new_y < 17):
            occupancy = occupancy_map[new_x, new_y]  
                
            if occupancy==0:
                going_up = self.calculate_distance(new_x, x, new_y, y)
                if best_distance is None:
                    best_distance = going_up
                    best_move = Moves.UP.name
                elif best_distance > going_up:
                        best_distance = going_up
                        best_move = Moves.UP.name

        #Going down
        new_x = self.x
        new_y = self.y+1

        if (new_x >= 0 and new_x < 31) and (new_y >= 0 and new_y < 17):
            occupancy = occupancy_map[new_x, new_y]  
                
            if occupancy==0:
                going_down = self.calculate_distance(new_x, x, new_y, y)
                if best_distance is None:
                    best_distance = going_down
                    best_move = Moves.DOWN.name
                elif best_distance > going_down:
                    best_distance = going_down
                    best_move = Moves.DOWN.name

        #Current position actualization
        if best_move is Moves.RIGHT.name:
            self.x+=1
        elif best_move is Moves.LEFT.name:
            self.x-=1
        elif best_move is Moves.UP.name:
            self.y-=1
        elif best_move is Moves.DOWN.name:
            self.y+=1

        occupancy_map[self.x, self.y] = 4
        occupancy_map[old_x, old_y] = old_resource
        self.occupancy_queue.put(occupancy_map)









