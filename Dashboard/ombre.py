import sys
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDialog)
os.environ.__setitem__('DISPLAY', ':0.0')
from PyQt5 import QtWidgets, uic
class Ombre(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Creation de la fenetre
        self.setWindowTitle('Opppmbre')
        #self.setFixedSize(ScreenWidth, ScreenHeight)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.5)
        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    shadow = Ombre()
    sys.exit(app.exec_())
