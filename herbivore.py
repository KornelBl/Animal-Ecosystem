import random
import time
from animal import Animal
import math
from threading import Lock
    
class Herbivore(Animal):
    def __init__(self, x: int, y: int, fairyland_map: list, fairy_lock, ponds: list, trees: list, caves: list):
        super(Herbivore, self).__init__(x, y, fairyland_map, fairy_lock, ponds)
        self.trees = trees
        self.caves = caves
        self.lock = Lock()

    def run(self):

        while(self.alive):

            self.update_needs()

            if self.food < 50:
                self.look_for_food()
            elif self.water < 50:
                self.look_for_water()
            elif self.sleep < 50:
                self.look_for_cave()
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
                self.x = nearest_cave.x
                self.y = nearest_cave.y

                time.sleep(random.uniform(1.5, 3.0))

                self.sleep = 100

                nearest_cave.lock.release()






            







