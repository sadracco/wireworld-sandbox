import numpy as np
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import Qt


class CellGrid:
    def __init__(self, ysize, xsize):
        self.cellSize = 15
        self.S_HEIGHT = ysize
        self.S_WIDTH = xsize
        self.grid = np.zeros([xsize//self.cellSize,ysize//self.cellSize])
        self.brushes = {
                'con': QBrush(QColor(242,227,56)),
                'head': QBrush(QColor(66,135,245)),
                'tail': QBrush(QColor(242,56,65)),
                }
        self.pens = {
                'con': QPen(QColor(242,227,56), 1.5),
                'head': QPen(QColor(66,135,245), 1.5),
                'tail': QPen(QColor(242,56,65), 1.5),
                }

        self.panY = 0
        self.panX = 0
        self.scaleX = 1
        self.scaleY = 1

    def addCell(self, xx, yy, v):
        shape = self.grid.shape
        y, x = self.screenToGrid((yy,xx))
        x = x//self.cellSize
        y = y//self.cellSize
        print(f'addCell: screen({xx},{yy}), grid({x},{y})')
        if x >= shape[1]:
            self.expand(0,x-shape[1]+1)
            print(f'Cell grid expansion from ({shape[1]},{shape[0]}) to ({self.grid.shape[1]},{self.grid.shape[0]})')
        if y >= shape[0]:
            self.expand(y-shape[0]+1,0)
            print(f'Cell grid expansion from ({shape[1]},{shape[0]}) to ({self.grid.shape[1]},{self.grid.shape[0]})')

        self.grid[y,x] = v

    def render(self, qp):
        s = self.cellSize
        rSize = self.scaleX * self.cellSize
        for x, y in self.getConductors():
            qp.setBrush(self.brushes['con'])
            qp.setPen(self.pens['con'])
            x, y = self.gridToScreen((x*s, y*s))
            qp.drawRect(x, y, rSize, rSize)
        for x, y in self.getHeads():
            qp.setBrush(self.brushes['head'])
            qp.setPen(self.pens['head'])
            x, y = self.gridToScreen((x*s, y*s))
            qp.drawRect(x, y, rSize, rSize)
        for x, y in self.getTails():
            qp.setBrush(self.brushes['tail'])
            qp.setPen(self.pens['tail'])
            x, y = self.gridToScreen((x*s, y*s))
            qp.drawRect(x, y, rSize, rSize)

    def scale(self, mpos, v):
        bwx, bwy = self.screenToGrid(mpos)
        self.scaleX *= v
        self.scaleY *= v
        awx, awy = self.screenToGrid(mpos)
        print(f'Scale: scale({self.scaleX}, {self.scaleY}) before({bwx}, {bwy}) after({awx}, {awy}))')
        self.panX += (bwx - awx)
        self.panY += (bwy - awy)
        if self.panX < 0:
            self.panX = 0
        if self.panY < 0:
            self.panY = 0

    def gridToScreen(self, pos):
        return (int((pos[0]-self.panX) * self.scaleX),
                int((pos[1]-self.panY) * self.scaleY))

    def screenToGrid(self, pos):
        return (int(pos[0]/self.scaleX + self.panX),
                int(pos[1]/self.scaleY + self.panY))

    def getCellAtPos(self, x, y):
        s = self.cellSize
        x, y = self.screenToGrid((x, y))
        return self.grid[x//s, y//s]

    def drawGrid(self, qp):
        x, y = self.gridToScreen((0,0))
        qp.setPen(QPen(QColor(255,255,255,100), 3, Qt.DotLine))
        qp.drawLine(0,y,self.S_WIDTH,y)
        qp.drawLine(x,0,x,self.S_HEIGHT)
        qp.setPen(QPen(QColor(255,255,255,255), 0.05))
        s = self.cellSize * self.scaleX
        y = y%s
        while y < self.S_HEIGHT:
            qp.drawLine(0,y,self.S_WIDTH,y)
            y += s

        x = x%s
        while x < self.S_WIDTH:
            qp.drawLine(x,0,x,self.S_HEIGHT)
            x += s

    def expand(self, x, y):
        self.grid = np.pad(self.grid, [(0,x), (0,y)])

    def expandLeft(self, x, y):
        self.grid = np.pad(self.grid, [(x,0), (y,0)])

    def clear(self):
        self.grid = np.zeros(self.grid.shape)

    def resolve(self):
        tempGrid = np.copy(self.grid)
        for x, y in self.getHeads():
            tempGrid[x][y] = 3
        for x, y in self.getTails():
            tempGrid[x][y] = 1
        for x, y in self.getConductors():
            if 0<self.headNeigh((x,y))<3:
                tempGrid[x][y] = 2
        self.grid = tempGrid

    def headNeigh(self, a):
        s = 0
        offs = ((1,-1),(1,0),(1,1),
                (0,1),(-1,1),(-1,0),
                (-1,-1),(0,-1))

        for off in offs:
            try:
                if self.grid[a[0]+off[0], a[1]+off[1]] == 2:
                    s+=1
            except:
                pass
        return s

    def getConductors(self):
        return np.argwhere(self.grid==1)

    def getHeads(self):
        return np.argwhere(self.grid==2)

    def getTails(self):
        return np.argwhere(self.grid==3)

    def getAll(self):
        return np.argwhere(self.grid!=0)
