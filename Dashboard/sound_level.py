import sys
import time
import os
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)
# from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
# import threading
from PyQt5 import QtWidgets, uic

# Pour le dev : affiche sur l ecran de la raspberry
#os.environ.__setitem__('DISPLAY', ':0.0')

class volumewindow(QtWidgets.QDialog):
    def __init__(self):
        Volume =0
        #Definition de la taille de lecran
        self.ScreenHeight = 720
        self.ScreenWidth = 1280
        # Definition de la taille de la fenetre
        self.WindowHeight = 80
        self.WindowWidth =1000
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
        self.progress.setTextVisible(0)
        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.visible=False

    def moveup(self):
        self.visible=True
        self.show()
        size = self.size()
        # Emplacement de la fenetre en fonction de la taille de l ecran et de la fenetre pour etre centre
        emplacement_y_cible = int(self.ScreenHeight - size.height())
        emplacement_x = int(self.ScreenWidth / 2 - size.width() / 2)
        # emplacement_y = int(self.ScreenHeight)
        emplacement_y = emplacement_y_cible
        # Application nouvelle geometry

        self.move(emplacement_x, emplacement_y)
        # add = 30
        # while emplacement_y > emplacement_y_cible:
        #     velocity = 5
        #     if add - velocity > 0:
        #         add = add - velocity
        #     emplacement_y = (emplacement_y - add)
        #     # Application nouvelle geometry
        #     self.move(emplacement_x, emplacement_y)
        #     time.sleep(.01)



    def movedown(self):
        size = self.size()
        # Emplacement de la fenetre en fonction de la taille de l ecran et de la fenetre pour etre centre
        emplacement_y_cible =  self.ScreenHeight
        emplacement_x = int(self.ScreenWidth / 2 - size.width() / 2)
        emplacement_y = int(self.ScreenHeight - size.height())
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
        self.visible=False
        # print("Fin movedown")

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
    window = volumeWindow()
    # On lance la boucle qui attend le changment de volume
    threading.Thread(target=window.volume_loop).start()
    sys.exit(app.exec_())
