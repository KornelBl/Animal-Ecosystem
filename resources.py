import numpy as np
from threading import Lock



class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lock = Lock()

class Tree(Resource):
    COLOR = (100, 220, 100)
    def __init__(self,x,y):
        super(Tree,self).__init__(x,y)

