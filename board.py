import pygame
import sys
import random
import numpy as np
from pygame.locals import *


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
        for row in rows:
            pygame.draw.line(surface, Board.BLACK, (0, row), (1280, row))
        for col in cols:
            pygame.draw.line(surface, Board.BLACK, (col, 0), (col, 720))

        for row in rows:
            for col in cols:
                spaces.append((col-40, row-40))

        coords = random.sample(spaces, Board.TREE_NUMBER+Board.CAVE_NUMBER+Board.POND_NUMBER)

        for i in range(Board.TREE_NUMBER):
            pygame.draw.rect(surface, Board.TREE_COLOR, [coords[i][0]+1, coords[i][1]+1, 39, 39])

        for i in range(Board.TREE_NUMBER ,Board.CAVE_NUMBER + Board.TREE_NUMBER):
            pygame.draw.rect(surface, Board.CAVE_COLOR, [coords[i][0]+1, coords[i][1]+1, 39, 39])

        for i in range(Board.CAVE_NUMBER + Board.TREE_NUMBER,Board.POND_NUMBER+Board.CAVE_NUMBER + Board.TREE_NUMBER):
            pygame.draw.rect(surface, Board.POND_COLOR, [coords[i][0]+1, coords[i][1]+1, 39, 39])

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    def draw_me(self) -> None:
        pass
