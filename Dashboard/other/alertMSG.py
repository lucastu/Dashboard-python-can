import sys
import time
import os
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel,
                             QProgressBar, QPushButton,QGridLayout)
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
import threading
import subprocess

# Pour le dev : affiche sur l ecran de la raspberry
os.environ.__setitem__('DISPLAY', ':0.0')
#Definition de la taille de lecran


class alertmsg(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
      
        ScreenHeight = 720
        ScreenWidth = 1280
        # Definition de la taille de la fenetre
        WindowHeight = 400
        WindowWidth =800
        
        Info_type="gas"
        Info_text=""
        # Creation de la fenetre
        self.setFixedSize(WindowWidth, WindowHeight)
        self.move(ScreenWidth / 2 - WindowWidth / 2, -WindowHeight)
        #self.setStyleSheet("background-color: grey;")

        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.texte = QLabel(self)
        self.texte.setFont(QFont('Roboto', 50))
        self.texte.setText(Info_text)
        self.texte.setAlignment(Qt.AlignCenter)
        # Create widget
        self.image = QPixmap("/home/pi/lucas/%s.png" % Info_type)
        self.image = self.image.scaledToHeight(WindowHeight)
        self.label = QLabel(self)
        self.label.setPixmap(self.image)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.label,1,1)
        self.grid.addWidget(self.texte,1,1)
        self.setLayout(self.grid)
        #self.show()

    def movedown(self):
        size = self.size()
        # Emplacement de la fenetre en fonction de la taille de l ecran et de la fenetre pour etre centre
        emplacement_y_cible = int(ScreenHeight/2 - size.height() /2)
        emplacement_x = int(ScreenWidth / 2 - size.width() / 2)
        emplacement_y = -WindowHeight
        # Application nouvelle geometry
        self.move(emplacement_x, emplacement_y)
        velocity = 100
        # print(emplacement_y_cible)
        while emplacement_y < emplacement_y_cible:
            velocity=int(velocity/1.1)
            emplacement_y = (emplacement_y + velocity)
            # Application nouvelle geometrie
            self.move(emplacement_x, emplacement_y)
            time.sleep(.03)
            
    def mousePressEvent(self, QMouseEvent):
        self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Actions()
    #QTimer.singleShot (100, window.movedown)

    sys.exit(app.exec_())
