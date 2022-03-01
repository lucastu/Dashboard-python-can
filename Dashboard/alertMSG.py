import sys
import os
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel,
                             QProgressBar, QPushButton,QGridLayout)
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
#import threading

# Pour le dev : affiche sur l ecran de la raspberry
os.environ.__setitem__('DISPLAY', ':0.0')
#Definition de la taille de lecran


class alertmsg(QDialog):
    ''' Define the window centered that will show the Infomessage of the car'''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        ScreenHeight = 600
        ScreenWidth = 1024

        # Definition de la taille de la fenetre
        WindowHeight = 200
        WindowWidth =800

        Info_text="ljfeh lejsfhmejfhm fnd vmkje  fjz efmjze"
        self.setWindowTitle('AlertMSG')
        # Creation de la fenetre
        self.setFixedSize(WindowWidth, WindowHeight)
        self.move(ScreenWidth / 2 - WindowWidth / 2, ScreenHeight/2- WindowHeight/2)
        self.setStyleSheet("background-color: white;")
        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.texte = QLabel(self)
        self.texte.setFont(QFont('Roboto', 50))
        self.texte.setText(Info_text)
        self.texte.setAlignment(Qt.AlignCenter)
        self.texte.setWordWrap(True)
        # Create widget
        self.image = QPixmap("/home/pi/lucas/images/info.png")
        self.image = self.image.scaledToHeight(WindowHeight)
        self.label = QLabel(self)
        self.label.setPixmap(self.image)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.label,1,1)
        self.grid.addWidget(self.texte,1,2)
        self.setLayout(self.grid)

    def mousePressEvent(self, QMouseEvent):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = alertmsg()
    window.show()

    sys.exit(app.exec_())
