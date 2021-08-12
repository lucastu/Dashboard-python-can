import sys
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDialog)
# Pour le dev : affiche sur l ecran de la raspberry
os.environ.__setitem__('DISPLAY', ':0.0')
#Definition de la taille de lecran
#ScreenHeight = 720
#ScreenWidth = 1280

class Ombre(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Creation de la fenetre
        self.setWindowTitle('Ombre')
        #self.setFixedSize(ScreenWidth, ScreenHeight)
        self.setStyleSheet("background-color: black;")
        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    shadow = Ombre()
    #QTimer.singleShot (7000, shadow.close)
    sys.exit(app.exec_())
