from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal


class OnOffButton(QLabel, QObject):
    def __init__(self, master, onImage, offImage, func, defState=True, onColor='164,66,245,0.5', offColor='255,255,255,0.5'):
        QObject.__init__(self, master)
        self.master = master
        self.onPixmap = QPixmap(onImage)
        self.offPixmap = QPixmap(offImage)
        self.onStyle = f'background-color: rgba({onColor}); border-radius: 10px; max-width: 50px; max-height: 50px; margin: 1px'
        self.offStyle = f'background-color: rgba({offColor}); border-radius: 10px; max-width: 50px; max-height: 50px; margin: 1px'
        self.active = defState
        self.func = func
        self.setState(self.active)

    def setState(self, state):
        self.func()
        if state:
            self.setStyleSheet(self.onStyle)
            self.setPixmap(self.onPixmap)
        else:
            self.setStyleSheet(self.offStyle)
            self.setPixmap(self.offPixmap)

    def mousePressEvent(self, e):
        self.active = not self.active
        self.setState(self.active)
