import numpy as np


class CellGrid:
    def __init__(self, x, y):
        self.grid = np.zeros([x,y])
        self.grid[:5,:5] = 1
        self.grid[5:10,5:10] = 2
        self.grid[10:15,10:15] = 3

    def addCell(self, x, y):
        shape = self.grid.shape

        ex = 0
        ey = 0
        if x > shape[1]:
            ex = x - shape[1]
        if y > shape[0]:
            ey = y - shape[0]
        if ex or ey:
            self.expand(ey+1, ex+1)

        self.grid[y,x] = 1

    def expand(self, x, y):
        self.grid = np.pad(self.grid, [(0,x), (0,y)])

    def getConductors(self):
        return np.argwhere(self.grid==1)

    def getHeads(self):
        return np.argwhere(self.grid==2)

    def getTails(self):
        return np.argwhere(self.grid==3)
