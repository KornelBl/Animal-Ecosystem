import pygame
import sys
import random
import numpy as np
from pygame.locals import *
from herbivore import Herbivore
from carnivore import Carnivore
from threading import Lock
from enum import Enum
from resources import Tree,Cave,Pond

class Resources(Enum):
    TREE = 1
    CAVE = 2
    POND = 3
    HERBIVORE = 4
    CARNIVORE = 5

class Board:
    GREEN = (129, 187, 129)
    BLACK = (0, 0, 0)
    TREE_NUMBER = 5
    CAVE_NUMBER = 5
    POND_NUMBER = 5

    def __init__(self):
        trees = list()
        caves = list()
        ponds = list()
        herbivores = list()
        carnivores = list()

        spaces = list()

        rows = [n for n in range(0, 17, 1)]
        cols = [n for n in range(0, 31, 1)]

        pygame.init()
        surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Rumiany Wschód')

        surface.fill(Board.GREEN)
        
        self.redraw_lines(rows, cols, surface)

        for row in rows:
            for col in cols:
                spaces.append((col, row))

        coords = random.sample(spaces, Board.TREE_NUMBER+Board.CAVE_NUMBER+Board.POND_NUMBER)

        for i in range(Board.TREE_NUMBER):
            a, b = coords[i]
            trees.append(Tree(a, b))
        for i in range(Board.TREE_NUMBER, Board.CAVE_NUMBER + Board.TREE_NUMBER):
            a, b = coords[i]
            caves.append(Cave(a, b))
        for i in range(Board.CAVE_NUMBER + Board.TREE_NUMBER,
                       Board.POND_NUMBER + Board.CAVE_NUMBER + Board.TREE_NUMBER):
            a, b = coords[i]
            ponds.append(Pond(a, b))

        self.redraw_resources(surface, coords)

        #Occupancy map with lock
        occupancy_map_lock = Lock()
        occupancy_map = self.init_map(rows, cols, spaces, coords)
        
        #Creating the herbivore threads
        herbivores = [Herbivore(i, i, occupancy_map, occupancy_map_lock, ponds, trees, caves) for i in range(10)]

        #Creating the carnivore threads
        carnivores = [Carnivore(i+6, i+6, occupancy_map, occupancy_map_lock, ponds, herbivores) for i in range(5)]

        for i in herbivores:
            i.start()

        for i in carnivores:
            i.start()

        herbivore_positions_list = []
        carnivore_positions_list = []

        while True:
            occupancy_map_lock.acquire(True)

            #Updating current herbivore positions
            herbivore_positions_list.clear()
            for i in herbivores:
                if i.alive:
                    a, b = i.get_position() 
                    herbivore_positions_list.append([a, b])
                else:
                    herbivores.remove(i)

            #Updating current carnivore positions
            carnivore_positions_list.clear()
            for i in carnivores:
                if i.alive:
                    a, b = i.get_position() 
                    carnivore_positions_list.append([a, b])

            #Updating the occupancy map
            occupancy_map = self.init_map(rows, cols, spaces, coords)
            self.update_occupancy_list(occupancy_map,
                                           herbivore_positions_list, 
                                           carnivore_positions_list)

            occupancy_map_lock.release()

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


    def redraw(self) -> None:
        pass

    def init_map(self, rows, cols, spaces, coords):
        land = np.zeros(shape=(len(cols), len(rows)))
        for i in range(Board.TREE_NUMBER):
            a = coords[i][0]
            b = coords[i][1]
            land[a, b] = Resources.TREE.value

        for i in range(Board.TREE_NUMBER, Board.CAVE_NUMBER + Board.TREE_NUMBER):
            a = coords[i][0]
            b = coords[i][1]
            land[a, b] = Resources.CAVE.value

        for i in range(Board.CAVE_NUMBER + Board.TREE_NUMBER,
                       Board.POND_NUMBER + Board.CAVE_NUMBER + Board.TREE_NUMBER):
            a = coords[i][0]
            b = coords[i][1]
            land[a, b] = Resources.POND.value

        return land

    def update_occupancy_list(self, occupancy_map,
                              herbivore_positions, carnivore_positions):
            for herbivore_pos in herbivore_positions:
                occupancy_map[herbivore_pos[0], herbivore_pos[1]] = Resources.HERBIVORE.value
            
            for carnivore_pos in carnivore_positions:
                occupancy_map[carnivore_pos[0], carnivore_pos[1]] = Resources.CARNIVORE.value



    def redraw_lines(self, rows, cols, surface):
        for row in rows:
            pygame.draw.line(surface, Board.BLACK, (0, row*40+40), (1280, row*40+40))
        for col in cols:
            pygame.draw.line(surface, Board.BLACK, (col*40+40, 0), (col*40+40, 720))

    def redraw_resources(self, surface, coords):
        for i in range(Board.TREE_NUMBER):
            pygame.draw.rect(surface, Tree.COLOR, [coords[i][0]*40+1, coords[i][1]*40+1, 39, 39])

        for i in range(Board.TREE_NUMBER ,Board.CAVE_NUMBER + Board.TREE_NUMBER):
            pygame.draw.rect(surface, Cave.COLOR, [coords[i][0]*40+1, coords[i][1]*40+1, 39, 39])

        for i in range(Board.CAVE_NUMBER + Board.TREE_NUMBER,Board.POND_NUMBER+Board.CAVE_NUMBER + Board.TREE_NUMBER):
            pygame.draw.rect(surface, Pond.COLOR, [coords[i][0]*40+1, coords[i][1]*40+1, 39, 39])


    def redraw_herbivores(self, surface, herbivore_positions: list):
        for i in herbivore_positions:
            pygame.draw.circle(surface, (255, 182, 193), (i[0]*40+20, i[1]*40+20), 15, 1)

    def redraw_carnivores(self, surface, carnivore_positions: list):
        for i in carnivore_positions:
            pygame.draw.circle(surface, (255, 0, 0), (i[0]*40+20, i[1]*40+20), 15, 1)

