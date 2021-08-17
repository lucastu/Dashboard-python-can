import sys
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDialog)
os.environ.__setitem__('DISPLAY', ':0.0')
from PyQt5 import QtWidgets, uic

class ombre(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Creation de la fenetre
        #self.setWindowTitle('shadow')
        #self.setFixedSize(ScreenWidth, ScreenHeight)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.5)
        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.showMaximized()

     def mousePressEvent(self, QMouseEvent):
        self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    shadow = Ombre()
    sys.exit(app.exec_())
