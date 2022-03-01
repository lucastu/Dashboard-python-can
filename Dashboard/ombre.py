import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDialog)
os.environ.__setitem__('DISPLAY', ':0.0')


class ombre(QtWidgets.QDialog):
    ''' describe the fake window that displays in the background of alertMSG'''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Creation de la fenetre
        self.setWindowTitle('Ombre')
        #self.setFixedSize(ScreenWidth, ScreenHeight)
        self.setStyleSheet("background-color: rgb(59,59,59);")
        #self.setWindowOpacity(0.5)
        # WindowOpacity handeled by picom (see picom conf file)
        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        # self.showMaximized()

    def mousePressEvent(self, QMouseEvent):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    shadow = ombre()
    sys.exit(app.exec_())
