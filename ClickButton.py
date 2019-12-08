from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal


class ClickButton(QLabel):
    def __init__(self, master, image, func, onColor='164,66,245,0.5', offColor='255,255,255,0.5'):
        QLabel.__init__(self)
        self.master = master
        self.pixmap = QPixmap(image)
        self.setPixmap(self.pixmap)
        self.onStyle = f'background-color: rgba({onColor}); border-radius: 10px; max-width: 50px; max-height: 50px; margin: 1px'
        self.offStyle = f'background-color: rgba({offColor}); border-radius: 10px; max-width: 50px; max-height: 50px; margin: 1px'
        self.active = False
        self.func = func
        self.setStyleSheet(self.offStyle)

    def mousePressEvent(self, e):
        self.setStyleSheet(self.onStyle)
        self.func()

    def mouseReleaseEvent(self, e):
        self.setStyleSheet(self.offStyle)
