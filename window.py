#!/usr/bin/python3

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QCursor
from PyQt5.QtCore import Qt, QTimer

from CellGrid import CellGrid

import sys


S_WIDTH = 1300
S_HEIGHT = 700


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initQP()
        self.timer = QTimer()
        self.timer.timeout.connect(self.animFrame)
        self.timer.setInterval(500)
        self.anim = False
        self.cells = CellGrid(S_HEIGHT, S_WIDTH)

    def initUI(self):
        self.setGeometry(0, 0, S_WIDTH, S_HEIGHT)
        self.setWindowTitle('Wire World')
        self.setStyleSheet('background-color: black')
        self.show()

    def initQP(self):
        self.qp = QPainter()
        
    def paintEvent(self, e):
        self.qp.begin(self)
        self.qp.setRenderHint(QPainter.Antialiasing)
        self.qp.setPen(QPen(QColor(0,0,0,0)))
        self.cells.render(self.qp)
       # self.qp.setPen(QPen(QColor(255,255,255,255), 0.1))
       # self.cells.drawGrid(self.qp)
        self.qp.end()

    def mousePressEvent(self, e):
        x, y = e.x(), e.y()
        if e.button() == Qt.LeftButton:
            self.addCell(x, y, 1)
        if e.button() == Qt.RightButton:
            if self.cells.getCellAtPos(x, y) == 2:
                self.addCell(x, y, 3)
            else:
                self.addCell(x, y, 2)
        if e.button() == Qt.MiddleButton:
            self.startPanX = x
            self.startPanY = y

        self.update()

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MiddleButton:
            x = e.x()
            y = e.y()
            self.cells.panX -= (x - self.startPanX)
            self.cells.panY -= (y - self.startPanY)
            if self.cells.panX > 0:
                self.cells.panX = 0
            if self.cells.panY > 0:
                self.cells.panY = 0
            self.startPanX = x
            self.startPanY = y
        self.update()

    def wheelEvent(self, e):
        mpos = (QCursor.pos().x(), QCursor.pos().y())
        d = e.angleDelta().y()
        if d > 0:
            self.cells.scale(mpos, 1 + d*0.0001)
        elif d < 0:
            self.cells.scale(mpos, 1 + d*0.0001)
        self.update()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.anim = not self.anim
            if self.anim:
                self.timer.start()
            else:
                self.timer.stop()
        elif e.key() == Qt.Key_C:
            self.cells.clear()
            self.update()

    def animFrame(self):
        self.cells.resolve()
        self.update()

    def addCell(self, x, y, v):
        self.cells.addCell(y, x, v)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
