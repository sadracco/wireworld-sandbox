from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal


class RadioButton(QLabel):
    def __init__(self, master, radioSet, image, func, defState=False, onColor='164,66,245,0.5', offColor='255,255,255,0.5'):
        QLabel.__init__(self)
        self.master = master
        self.radioSet = radioSet
        self.pixmap = QPixmap(image)
        self.setPixmap(self.pixmap)
        self.onStyle = f'background-color: rgba({onColor}); border-radius: 10px; max-width: 50px; max-height: 50px; margin: 1px'
        self.offStyle = f'background-color: rgba({offColor}); border-radius: 10px; max-width: 50px; max-height: 50px; margin: 1px'
        self.active = defState
        self.func = func
        self.setState(self.active)

    def mousePressEvent(self, e):
        self.radioSet.resetButtons()
        self.active = not self.active
        self.setState(self.active)

    def setState(self, state):
        if state:
            self.setStyleSheet(self.onStyle)
            self.func()
        else:
            self.setStyleSheet(self.offStyle)

    def reset(self):
        self.active = False
        self.setState(self.active)
