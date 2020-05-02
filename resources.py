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


class Cave(Resource):
    COLOR = (0, 0, 0)

    def __init__(self,x,y):
        super(Cave,self).__init__(x,y)


class Pond(Resource):
    COLOR = (0, 0, 255)

    def __init__(self,x,y):
        super(Pond,self).__init__(x,y)

