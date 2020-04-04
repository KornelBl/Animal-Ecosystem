import pygame
import sys
import random
import numpy as np
from pygame.locals import *
from herbivore import Herbivore
from carnivore import Carnivore
from threading import Lock

class Board:
    GREEN = (129, 187, 129)
    BLACK = (0, 0, 0)
    TREE_COLOR = (100, 220, 100)
    TREE_NUMBER = 5
    CAVE_COLOR = (0, 0, 0)
    CAVE_NUMBER = 5
    POND_COLOR = (0, 0, 255)
    POND_NUMBER = 5

    def __init__(self):
        spaces = list()
        rows = [n for n in range(40, 720, 40)]
        cols = [n for n in range(40, 1280, 40)]

        pygame.init()
        surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Rumiany Wschód')

        surface.fill(Board.GREEN)
        
        self.redraw_lines(rows, cols, surface)

        for row in rows:
            for col in cols:
                spaces.append((col-40, row-40))

        coords = random.sample(spaces, Board.TREE_NUMBER+Board.CAVE_NUMBER+Board.POND_NUMBER)

        self.redraw_resources(surface, coords)

        #Occupancy map with lock
        fairy_lock = Lock()
        fairyland_map = self.init_map(rows, cols, spaces, coords)

        #Creating the herbivore threads
        herbivores = [Herbivore(i, i, fairyland_map, fairy_lock) for i in range(5)]     

        #Creating the carnivore threads
        carnivores = [Carnivore(i+6, i+6, fairyland_map, fairy_lock) for i in range(5)]     

        for i in herbivores:
            i.start()

        for i in carnivores:
            i.start()

        herbivore_positions_list = []
        carnivore_positions_list = []

        while True:
            #Updating current herbivore positions
            herbivore_positions_list.clear()
            for i in herbivores:
                a, b = i.get_position() 
                herbivore_positions_list.append([a, b])

            #Updating current carnivore positions
            carnivore_positions_list.clear()
            for i in carnivores:
                a, b = i.get_position() 
                carnivore_positions_list.append([a, b])

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                    #Killing animals before exit
                    for i in herbivores:
                        i.alive = False
                    for i in carnivores:
                        i.alive = False
                    sys.exit()

            #Redrawing everything
            surface.fill(Board.GREEN)
            self.redraw_lines(rows, cols, surface)
            self.redraw_resources(surface, coords)
            self.redraw_herbivores(surface, herbivore_positions_list)
            self.redraw_carnivores(surface, carnivore_positions_list)
            pygame.display.update()


    def draw_me(self) -> None:
        pass

    def init_map(self, rows, cols, spaces, coords):
        land = np.zeros(shape=(len(cols), len(rows)))
        for n in spaces:
            if n in coords:
                a = int(n[0]/40)
                b = int(n[1]/40)
                land[a, b] = 1
        return land

    def redraw_lines(self, rows, cols, surface):
        for row in rows:
            pygame.draw.line(surface, Board.BLACK, (0, row), (1280, row))
        for col in cols:
            pygame.draw.line(surface, Board.BLACK, (col, 0), (col, 720))

    def redraw_resources(self, surface, coords):
        for i in range(Board.TREE_NUMBER):
            pygame.draw.rect(surface, Board.TREE_COLOR, [coords[i][0]+1, coords[i][1]+1, 39, 39])

        for i in range(Board.TREE_NUMBER ,Board.CAVE_NUMBER + Board.TREE_NUMBER):
            pygame.draw.rect(surface, Board.CAVE_COLOR, [coords[i][0]+1, coords[i][1]+1, 39, 39])

        for i in range(Board.CAVE_NUMBER + Board.TREE_NUMBER,Board.POND_NUMBER+Board.CAVE_NUMBER + Board.TREE_NUMBER):
            pygame.draw.rect(surface, Board.POND_COLOR, [coords[i][0]+1, coords[i][1]+1, 39, 39])        


    def redraw_herbivores(self, surface, herbivore_positions: list):
        for i in herbivore_positions:
            pygame.draw.circle(surface, (255, 182, 193), (i[0]*40+20, i[1]*40+20), 15, 1)

    def redraw_carnivores(self, surface, carnivore_positions: list):
        for i in carnivore_positions:
            pygame.draw.circle(surface, (255, 0, 0), (i[0]*40+20, i[1]*40+20), 15, 1)