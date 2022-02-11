import sys
import time
import os
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic

# os.environ.__setitem__('DISPLAY', ':0.0')

class volumewindow(QtWidgets.QDialog):
    def __init__(self):
        Volume =0
        #Definition de la taille de lecran
        self.ScreenHeight = 600
        self.ScreenWidth = 1024
        # Definition de la taille de la fenetre
        self.WindowHeight = 30
        self.WindowWidth =600
        
        super().__init__()
        self.initUI()

    def initUI(self):
        # Creation de la fenetre
        self.setWindowTitle('sound_level')
        self.setFixedSize(self.WindowWidth, self.WindowHeight)
        self.move(self.ScreenWidth / 2 - self.WindowWidth / 2, self.ScreenHeight)
        # Creation de la barre
        self.progress = QProgressBar(self)
        # Taille de la fenetre
        self.progress.setGeometry(0, 0, self.WindowWidth, self.WindowHeight)
        # Maxmimum de valeur de volume
        self.progress.setMaximum(30)
        # Retire le text du pourcentage dans la barre
        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.visible=False
        
    def moveup(self):
        self.visible=True
        self.show()
        # Placement according to window and display size
        emplacement_x = int(self.ScreenWidth / 2 - self.WindowWidth / 2)
        emplacement_y = int(self.ScreenHeight - self.WindowHeight)
        # Application nouvelle geometry
        self.move(emplacement_x, emplacement_y)

    def movedown(self):
        # Placement according to window and display size
        emplacement_y_cible =  self.ScreenHeight
        emplacement_x = int(self.ScreenWidth / 2 - self.WindowWidth / 2)
        emplacement_y = int(self.ScreenHeight - self.WindowHeight)
        self.move(emplacement_x, emplacement_y)

        add = 3
        velocity = 5
        while emplacement_y < emplacement_y_cible:
            if add - velocity > 0:
                add -= velocity
            emplacement_y += add
            self.move(emplacement_x, emplacement_y)
            time.sleep(.01)
        # Hide when out of screen
        self.hide()
        self.visible=False
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = volumewindow()
    window.show()
    window.move(0,0)
    sys.exit(app.exec_())
