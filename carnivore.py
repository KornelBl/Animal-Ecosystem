import random
import time
from animal import Animal

class Carnivore(Animal):
    def __init__(self, x: int, y: int, fairyland_map: list, fairy_lock):
        super(Carnivore, self).__init__(x, y, fairyland_map, fairy_lock)

    def run(self):
        while(self.alive):

            #Every 5 seconds a random localization is created. 
            #Animals are wandering aimlessy for now.
            if ((time.perf_counter() - self.time_s) > 5):
                self.random_x = random.randrange(0, 31)
                self.random_y = random.randrange(0, 17)
                self.time_s = time.perf_counter()

            self.move(self.random_x, self.random_y)
            time.sleep(1)
