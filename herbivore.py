import random
import time
from animal import Animal
import math
    
class Herbivore(Animal):
    def __init__(self, x: int, y: int, fairyland_map: list, fairy_lock, trees: list):
        super(Herbivore, self).__init__(x, y, fairyland_map, fairy_lock)
        self.trees = trees

    def run(self):
        #rozwiazac zagadke
        x,y= random.randrange(0, 32),random.randrange(0, 18)
        while(self.alive):

            self.hunger()
            #Every 5 seconds a random localization is created. 
            #Animals are wandering aimlessy for now.
            if ((time.perf_counter() - self.time_s) > 5):
                x, y = random.randrange(0, 32), random.randrange(0, 18)
                self.time_s = time.perf_counter()
            if self.food < 50:
                x, y = self.get_food_pos()
            self.move(x, y)
            time.sleep(0.3)

    def get_food_pos(self) -> (int, int):
        dist = 10000
        for tree in self.trees:
            new_dist = self.calculate_distance(self.x,tree.x,self.y,tree.y)
            if new_dist < dist:
                dist = new_dist
                nearest_tree = tree
        return nearest_tree.x, nearest_tree.y

 





            







