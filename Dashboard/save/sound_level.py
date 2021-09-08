#import sys
#import time
#import os
# from PyQt5.QtWidgets import (QApplication, QDialog,
#                             QProgressBar, QPushButton)
# from PyQt5.QtCore import QTimer
# from PyQt5.QtCore import Qt
# import threading
from PyQt5 import QtWidgets, uic

# Pour le dev : affiche sur l ecran de la raspberry
#os.environ.__setitem__('DISPLAY', ':0.0')

class volumewindow(QtWidgets.QDialog):
    def __init__(self):
        Volume =0
        #Definition de la taille de lecran
        ScreenHeight = 720
        ScreenWidth = 1280
        # Definition de la taille de la fenetre
        WindowHeight = 100
        WindowWidth =1000
        super().__init__()
        self.initUI()

    def initUI(self):
        # Creation de la fenetre
        self.setWindowTitle('sound_level')
        self.setFixedSize(WindowWidth, WindowHeight)
        self.move(ScreenWidth / 2 - WindowWidth / 2, ScreenHeight)
        # Creation de la barre
        self.progress = QProgressBar(self)
        # Taille de la fenetre
        self.progress.setGeometry(0, 0, WindowWidth, WindowHeight)
        # Maxmimum de valeur de volume
        self.progress.setMaximum(30)
        # Retire le text du pourcentage dans la barre
        self.progress.setTextVisible(0)
        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)

    def moveup(self):
        self.show()
        size = self.size()
        # Emplacement de la fenetre en fonction de la taille de l ecran et de la fenetre pour etre centre
        emplacement_y_cible = int(ScreenHeight - size.height())
        emplacement_x = int(ScreenWidth / 2 - size.width() / 2)
        emplacement_y = int(ScreenHeight)
        # Application nouvelle geometry
        self.move(emplacement_x, emplacement_y)
        add = 30
        while emplacement_y > emplacement_y_cible:
            velocity = 5
            if add - velocity > 0:
                add = add - velocity
            emplacement_y = (emplacement_y - add)
            # Application nouvelle geometry
            self.move(emplacement_x, emplacement_y)
            time.sleep(.01)
        self.update()
        self.movedown()


    def movedown(self):
        size = self.size()
        # Emplacement de la fenetre en fonction de la taille de l ecran et de la fenetre pour etre centre
        emplacement_y_cible =  ScreenHeight
        emplacement_x = int(ScreenWidth / 2 - size.width() / 2)
        emplacement_y = int(ScreenHeight - size.height())
        # Application nouvelle geometry
        self.move(emplacement_x, emplacement_y)

        add = 3
        while emplacement_y < emplacement_y_cible:
            velocity = 5
            if add - velocity > 0:
                add = add - velocity
            emplacement_y = (emplacement_y + add)
            # Application nouvelle geometrie
            self.move(emplacement_x, emplacement_y)
            time.sleep(.01)
        # On se cache arrivé en bas
        self.hide()

    def volume_loop(self):
          positionup = False
          while not stop_thread :
            #Si le flag interne du threald est levé, on enregistre son heure et on descend le flag
            if self.isset() :
              lastchangetime = int(time.time())
              self.clear()

            #Si ça fait moins de 2 secondes qu'il ya eu un changement
            if int(time.time()) - lastchangetime < 2 :
              self.progress.setValue(Volume)
              if positionup == False :
                #Volume.show()
                self.moveup()
                positionup = True
            #si ça fait plus de 2 secondes mais que la position de la fenêtre est Up, on la descend
            elif positionup == True :
              self.movedown()
              positionup = False
            #En dehors de ces cas, on attend la levée du flag
            else : 
              self.wait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VolumeWindow()
    # On lance la boucle qui attend le changment de volume
    threading.Thread(target=window.volume_loop).start()
    sys.exit(app.exec_())
