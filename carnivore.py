import random
import time
from animal import Animal

class Carnivore(Animal):
    def __init__(self, x: int, y: int, fairyland_map: list, fairy_lock, ponds: list,herbivores: list):
        super(Carnivore, self).__init__(x, y, fairyland_map, fairy_lock, ponds)
        self.herbivores = herbivores
    def run(self):
        while(self.alive):

            while (self.alive):

                self.update_needs()

                if self.food < 50:
                    self.look_for_food()
                elif self.water < 50:
                    self.look_for_water()
                elif self.sleep < 50:
                    #-------------------------------------------------
                    self.wander()
                    self.sleep = 100
                else:
                    self.wander()

                time.sleep(0.3)

    def get_food_pos(self) -> Animal:
        dist = 10000
        nearest_herbivore = None
        for herbivore in self.herbivores:
            new_dist = self.calculate_distance(self.x,herbivore.x,self.y,herbivore.y)
            if new_dist < dist:
                dist = new_dist
                nearest_herbivore = herbivore
        return nearest_herbivore

    def look_for_food(self):
        nearest_herbivore = self.get_food_pos()
        if nearest_herbivore is None:
            return

        self.move(nearest_herbivore.x, nearest_herbivore.y)

        if self.calculate_distance(nearest_herbivore.x, self.x, nearest_herbivore.y, self.y) == 1:

            if nearest_herbivore.lock.acquire(False):
                self.x = nearest_herbivore.x
                self.y = nearest_herbivore.y
                nearest_herbivore.alive = False

                time.sleep(random.uniform(1.5, 3.0))

                self.food = 100

                nearest_herbivore.lock.release()
            else:
                self.wander()