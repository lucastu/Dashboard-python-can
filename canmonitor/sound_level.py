import sys
import time
import os
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from tinydb import TinyDB, Query
import threading

# Pour le dev : affiche sur l ecran de la raspberry
os.environ.__setitem__('DISPLAY', ':0.0')

global Volume
Volume =0
#Definition de la taille de lecran
ScreenHeight = 720
ScreenWidth = 1280
# Definition de la taille de la fenetre
WindowHeight = 100
WindowWidth =1000
# Creation dune mini database pour passer des infos entre mes scripts... faute de mieux
db = TinyDB('/home/pi/lucas/db.json')

class Actions(QDialog):

    def __init__(self):
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
        # recuperation de la valeur du volume
        Niveau = db.get(Query()['Nom'] == 'Volume')
        Volume = int(Niveau.get('Valeur'))
        self.progress.setValue( Volume )
        # Retire le text du pourcentage dans la barre
        self.progress.setTextVisible(0)
        # Mode Frameless
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)

    def moveup(self):
        self.show()
        # print("plus caché")
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

        Last_click = db.get(Query()['Nom'] == 'Last_click')
        Last_click_time = int(Last_click.get('Valeur'))
        while int(time.time())-Last_click_time < 2 :
            Niveau = db.get(Query()['Nom'] == 'Volume')
            Volume = int(Niveau.get('Valeur'))
            self.progress.setValue(Volume)
            time.sleep(0.1)
            Last_click = db.get(Query()['Nom'] == 'Last_click')
            Last_click_time = int(Last_click.get('Valeur'))
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
        # On se cache
        self.hide()

    def waitforchange(self):
        Niveau = db.get(Query()['Nom'] == 'Volume')
        Volume = int(Niveau.get('Valeur'))
        New_Volume = Volume
        while 1:
            Niveau = db.get(Query()['Nom'] == 'Volume')
            New_Volume = int(Niveau.get('Valeur'))

            if Volume != New_Volume:
                print ("Volume : %s, Nouveau Volume : %s " %(Volume, New_Volume ))
                Volume = New_Volume
                self.moveup()
                # On recupere la valeur du volume apres s'être cache pour eviter une relmontee
                Niveau = db.get(Query()['Nom'] == 'Volume')
                Volume = int(Niveau.get('Valeur'))
            time.sleep(1)
            # print ("attente changement")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Actions()
    # On lance la boucle qui attend le changment de volume
    threading.Thread(target=window.waitforchange).start()
    sys.exit(app.exec_())