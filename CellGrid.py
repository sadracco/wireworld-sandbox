import numpy as np
from PyQt5.QtGui import QBrush, QColor, QPen, QCursor, QPainter
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject


class CellGrid(QObject):
    animSignal = pyqtSignal()

    def __init__(self, ysize, xsize, master):
        QObject.__init__(self, master)
        self.master = master
        self.qp = QPainter()

        self.gridOn = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.animFrame)
        self.speed = 500
        self.timer.setInterval(self.speed)
        self.anim = True

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

        self.tool = self.marker

        self.panY = 0
        self.panX = 0
        self.scaleX = 1
        self.scaleY = 1
        self.switchAnim()


    # Grid processing functions
    def addCell(self, yy, xx, v):
        shape = self.grid.shape
        y, x = self.screenToGrid((yy,xx))
        x = x//self.cellSize
        y = y//self.cellSize
        # print(f'addCell: screen({xx},{yy}), grid({x},{y})')
        if x >= shape[1]:
            self.expand(0,x-shape[1]+1)
            # print(f'Cell grid expansion from ({shape[1]},{shape[0]}) to ({self.grid.shape[1]},{self.grid.shape[0]})')
        if y >= shape[0]:
            self.expand(y-shape[0]+1,0)
            # print(f'Cell grid expansion from ({shape[1]},{shape[0]}) to ({self.grid.shape[1]},{self.grid.shape[0]})')

        self.grid[y,x] = v
        self.master.update()

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
        self.master.update()

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

    def expand(self, x, y):
        self.grid = np.pad(self.grid, [(0,x), (0,y)])

    def expandLeft(self, x, y):
        self.grid = np.pad(self.grid, [(x,0), (y,0)])

    def clear(self):
        if not self.anim:
            self.switchAnim()
        self.grid = np.zeros(self.grid.shape)
        self.master.update()


    # Rendering
    def render(self):
        self.qp.begin(self.master)
        self.qp.setRenderHint(QPainter.Antialiasing)
        self.drawCells(self.qp)
        if self.gridOn:
            self.drawGrid(self.qp)
        self.qp.end()

    def drawCells(self, qp):
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

    def drawGrid(self, qp):
        x, y = self.gridToScreen((0,0))
        '''
        qp.setPen(QPen(QColor(255,255,255,255), 3, Qt.DotLine))
        qp.drawLine(0,y,self.S_WIDTH,y)
        qp.drawLine(x,0,x,self.S_HEIGHT)
        '''
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

    def animFrame(self):
        self.resolve()
        self.master.update()

    def scale(self, mpos, v):
        bwx, bwy = self.screenToGrid(mpos)
        self.scaleX *= v
        self.scaleY *= v
        awx, awy = self.screenToGrid(mpos)
        # print(f'Scale: scale({self.scaleX}, {self.scaleY}) before({bwx}, {bwy}) after({awx}, {awy}))')
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

    def speedUp(self):
        self.changeSpeed(-20)

    def speedDown(self):
        self.changeSpeed(20)

    def changeSpeed(self, v):
        self.speed += v
        if self.speed > 5000:
            self.speed = 5000
        if self.speed < 10:
            self.speed = 10
        self.timer.setInterval(self.speed)



    # Events processing
    def processMouseMove(self, e):
        if e.buttons() == Qt.MiddleButton:
            x = e.x()
            y = e.y()
            self.panX -= (x - self.startPanX)
            self.panY -= (y - self.startPanY)
            if self.panX < 0:
                self.panX = 0
            if self.panY < 0:
                self.panY = 0
            self.startPanX = x
            self.startPanY = y
        self.master.update()

    def processMousePress(self, e):
        x, y = e.x(), e.y()
        self.tool(x,y,e.button())
        if e.button() == Qt.MiddleButton:
            self.startPanX = x
            self.startPanY = y

    def marker(self, x, y, b):
        if b == Qt.LeftButton:
            self.addCell(x, y, 1)
        if b == Qt.RightButton:
            if self.getCellAtPos(x, y) == 2:
                self.addCell(x, y, 3)
            else:
                self.addCell(x, y, 2)

    def eraser(self, x, y, b):
        if b == Qt.LeftButton:
            self.addCell(x, y, 0)

    def setToolMarker(self):
        self.tool = self.marker

    def setToolEraser(self):
        self.tool = self.eraser

    def triggerGrid(self):
        self.gridOn = not self.gridOn
        self.master.update()

    def processWheel(self, e):
        mpos = (QCursor.pos().x(), QCursor.pos().y())
        d = e.angleDelta().y()
        if d > 0:
            self.scale(mpos, 1 + d*0.0001)
        elif d < 0:
            self.scale(mpos, 1 + d*0.0001)
        self.master.update()


    # Other
    def switchAnim(self):
        self.animSignal.emit()
        self.anim = not self.anim
        if self.anim:
            self.timer.stop()
        else:
            self.timer.start()

    def getConductors(self):
        return np.argwhere(self.grid==1)

    def getHeads(self):
        return np.argwhere(self.grid==2)

    def getTails(self):
        return np.argwhere(self.grid==3)

    def getAll(self):
        return np.argwhere(self.grid!=0)
