#!/usr/bin/python3

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt

from CellGrid import CellGrid

import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initQP()
        self.cells = CellGrid(700//20, 1300//20)
        self.scale = 10

    def initUI(self):
        self.setGeometry(0, 0, 1300, 700)
        self.setWindowTitle('Wire World')
        self.setStyleSheet('background-color: black')
        self.show()

    def initQP(self):
        self.qp = QPainter()
        self.cBrush = QBrush(QColor(242,227,56))
        self.ehBrush = QBrush(QColor(66,135,245))
        self.etBrush = QBrush(QColor(242,56,65))

    def paintEvent(self, e):
        self.qp.begin(self)
        self.qp.setRenderHint(QPainter.Antialiasing)
        self.qp.setPen(QPen(QColor(0,0,0,0)))
        self.drawCells()
        self.qp.end()

    def mousePressEvent(self, e):
        self.addCell(e.x()//self.scale, e.y()//self.scale)

    def drawCells(self):
        s = self.scale
        self.qp.setBrush(self.cBrush)
        for cell in self.cells.getConductors():
            self.qp.drawRect(cell[0]*s, cell[1]*s, s, s)

        self.qp.setBrush(self.ehBrush)
        for cell in self.cells.getHeads():
            self.qp.drawRect(cell[0]*s, cell[1]*s, s, s)

        self.qp.setBrush(self.etBrush)
        for cell in self.cells.getTails():
            self.qp.drawRect(cell[0]*s, cell[1]*s, s, s)

    def drawGrid(self):
        pass

    def addCell(self, x, y):
        self.cells.addCell(y,x)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
