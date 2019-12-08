#!/usr/bin/python3

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QCursor, QPixmap
from PyQt5.QtCore import Qt, QTimer

from CellGrid import CellGrid
from OnOffButton import OnOffButton
from RadioButton import RadioButton
from RadioSet import RadioSet
from ClickButton import ClickButton

import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1300, 700)
        self.setWindowTitle('Wire World')
        self.setStyleSheet('background-color: black')

        self.grid = CellGrid(700, 1300, self)

        self.animMenu = QHBoxLayout()
        self.animMenu.addWidget(OnOffButton(self, 'assets/play.png', 'assets/pause.png', self.grid.switchAnim, defState=False))
        self.animMenu.addWidget(ClickButton(self, 'assets/rightArrow.png', self.grid.resolve))
        self.animMenu.addWidget(ClickButton(self, 'assets/upArrow.png', self.grid.speedUp))
        self.animMenu.addWidget(ClickButton(self, 'assets/downArrow.png', self.grid.speedDown))

        self.toolboxMenu = QVBoxLayout()

        self.toolboxRadioSet = RadioSet()
        marker = RadioButton(self, self.toolboxRadioSet, 'assets/marker.png', self.grid.setToolMarker, onColor='150, 255, 215, 0.5', defState=True)
        eraser = RadioButton(self, self.toolboxRadioSet, 'assets/eraser.png', self.grid.setToolEraser, onColor='150, 255, 215, 0.5')
        self.toolboxRadioSet.add(marker)
        self.toolboxRadioSet.add(eraser)

        grid = OnOffButton(self, 'assets/grid.png', 'assets/grid.png', self.grid.triggerGrid, onColor='150, 255, 215, 0.5')

        self.toolboxMenu.addWidget(marker)
        self.toolboxMenu.addWidget(eraser)
        self.toolboxMenu.addWidget(ClickButton(self, 'assets/broom.png', self.grid.clear, onColor='150, 255, 215, 0.5'))
        self.toolboxMenu.addWidget(grid)

        hbox = QHBoxLayout()
        hbox.addLayout(self.animMenu)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(self.toolboxMenu)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.show()
        
    def paintEvent(self, e):
        self.grid.render()

    def mousePressEvent(self, e):
        self.grid.processMousePress(e)

    def mouseMoveEvent(self, e):
        self.grid.processMouseMove(e)

    def wheelEvent(self, e):
        self.grid.processWheel(e)

    def resizeEvent(self, e):
        self.grid.S_WIDTH = self.frameGeometry().width()
        self.grid.S_HEIGHT = self.frameGeometry().height()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
