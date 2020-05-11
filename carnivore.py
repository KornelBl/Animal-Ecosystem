import random
import time
from animal import Animal

class Carnivore(Animal):
    def __init__(self, x: int, y: int, fairyland_map: list, fairy_lock, ponds: list):
        super(Carnivore, self).__init__(x, y, fairyland_map, fairy_lock, ponds)

    def run(self):
        while(self.alive):
    
            self.wander()

            time.sleep(0.3)


    def get_herbivore_pos(self):
        pass