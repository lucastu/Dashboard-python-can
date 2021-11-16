#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal, QObject, Qtimer
from PyQt5.QtGui import QPixmap,QFontDatabase
from PyQt5.QtWidgets import QLabel
import sys
import threading
import traceback
import time
import os
import logging
#import RPi.GPIO as GPIO   
from functools import partial

#Imports classes and function from my files
from source_handler import InvalidFrame, SerialHandler
from sound_level import volumewindow
from ombre import ombre
from alertMSG import alertmsg
from InfoMSG_parser import parseInfoMessage
from Bluetooth_utils import bluetooth_utils
from reading_loop import reading_loop

#Display on the device display in case of SSH launch of the script
stop_reading = threading.Event()

#Configure the log file and format
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/home/pi/lucas/log.txt')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# USB Arduino parameters
baudrate = 115200
serial_device = "/dev/ttyUSB0"

audiosettings = {
   'frontRearBalance' : '0',
   'leftRightBalance' : '0',
   'automaticVolume' : '0',
   'bass' : '0',
   'treble' : '0',
   'loudness' : '0',
   'source' : '0'
}

def format_data_hex(data):
    """Convert the bytes array to an hex representation."""
    # Bytes are separated by spaces. => not anymore
    return ''.join('%02X' % byte for byte in data)


def format_data_ascii(data):
    """Try to make an ASCII representation of the bytes.

    Non printable characters are replaced by '?' except null character which
    is replaced by '.'.
    DON'T TOUCH !!! WITCHCRAFT !!
    """
    msg_str = ''
    for byte in data:
        char = chr(byte)
        if char == '\0':
            msg_str = msg_str + '.'
        elif ord(char) < 32 or ord(char) > 126:
            msg_str = msg_str + '?'
        else:
            msg_str = msg_str + char
    return msg_str


def run():
    source_handler = SerialHandler(serial_device, baudrate)
    # Reading from a serial device, opened with timeout=0 (non-blocking read())
    source_handler.open()

    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    root = Ui()  # Create an instance of our class for the MainWindow

    # Create Thread for the reading loop , args : source_handler for USB & root for UI
    reading_thread = threading.Thread(target=reading_loop, args=(source_handler, root,))
    # Start the reading in background thread              
    reading_thread.start()

    # Create a timer that execute Bluetooth_reading_loop function every 500ms
    # Better than a while True : Loop 
    # To be tested
    Bluetooth_timer = QtCore.QTimer()
    Bluetooth_timer.timeout.connect(root.update_bluetooth_track)
    Bluetooth_timer.start(500)
    
    #Old way to loop the bluetooth reading
    #B_read =threading.Thread(target=root.update_bluetooth_track)
    #B_read.start()

    app.exec_()


class Ui(QtWidgets.QMainWindow):
   def update_progress_bluetooth_track(self):
       try:
           self.Bluetooth_progressBar.setValue(int(float(self.percent.text())))
       except:
           logging.info("Wrong type of value for track position")

   def update_progress_volume(self):
       try:
           self.Volumewindow.progress.setValue(int(self.Volume.text()))
       except:
           logging.info("Wrong type of value for Volume")

   def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('/home/pi/lucas/interface.ui', self)  # Load the .ui Mainwindow file
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)

        # QFontDatabase.addApplicationFont("Roboto-Thin.ttf")
        # self.setStyleSheet("font-family:'Arial';")
        # self.fontFamily = 'Roboto-Th'
        #Initialisation of the alert window
        self.init_alert_window()
        #Initialisation of the volume window
        self.Volumewindow=volumewindow()

        # Init both tabs
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)

        self.closebutton.clicked.connect(self.close_all)
        self.closebutton_3.clicked.connect(self.close_all)
        self.showMaximized()  # Show the GUI

        self.custom_signals = Communicate()
        self.custom_signals.update_progress_bluetooth_track_signal.connect(self.update_progress_bluetooth_track)
        self.custom_signals.update_progress_volume_signal.connect(self.update_progress_volume)

        # Init radio list
        self.radioList0.setText('')
        self.radioList1.setText('')
        self.radioList2.setText('')
        self.radioList3.setText('Appuyer sur le bouton ')
        self.radioList4.setText('"Liste" Pour charger ')
        self.radioList5.setText('les radios mémorisées')

   def init_alert_window(self):
        self.Ombre = ombre()
        self.AlertMSG = alertmsg() 
         
   def show_alert(self):
         self.Ombre.showMaximized()
         self.AlertMSG.show()
         
   def hide_alert(self):
         self.Ombre.hide()
         self.AlertMSG.hide()   

   def resetaudiosettingselector(self) :
         #Each selelctor display go hidden
         #Ugly but the best way to avoid repainting every selector and crashing program
         if self.SliderBassesselector.isVisible():
            self.SliderBassesselector.setHidden(True)
         if self.SliderBassesselector_2.isVisible():
            self.SliderBassesselector_2.setHidden(True)
         if self.SliderAigusselector.isVisible():
            self.SliderAigusselector.setHidden(True)
         if self.SliderAigusselector_2.isVisible():
            self.SliderAigusselector_2.setHidden(True)
         if self.frontRearBalanceselector.isVisible():
            self.frontRearBalanceselector.setHidden(True)
         if self.frontRearBalanceselector_2.isVisible():
            self.frontRearBalanceselector_2.setHidden(True)
         if self.leftRightBalanceselector.isVisible():
            self.leftRightBalanceselector.setHidden(True)
         if self.leftRightBalanceselector_2.isVisible():
            self.leftRightBalanceselector_2.setHidden(True)
         if self.Loudnessselector.isVisible():
            self.Loudnessselector.setHidden(True)
         if self.Loudnessselector_2.isVisible():
            self.Loudnessselector_2.setHidden(True)
         if self.automaticVolumeselector.isVisible():
            self.automaticVolumeselector.setHidden(True)
         if self.automaticVolumeselector_2.isVisible():
            self.automaticVolumeselector_2.setHidden(True)
         if self.equalizerselector.isVisible():
            self.equalizerselector.setHidden(True)
         if self.equalizerselector_2.isVisible():
            self.equalizerselector_2.setHidden(True)

   def resetequalizerselector(self) :
         #Each equalizer selector display go grey
         self.equalizernone.setStyleSheet("color: grey;")
         self.equalizerclassical.setStyleSheet("color: grey;")
         self.equalizerjazzBlues.setStyleSheet("color: grey;")
         self.equalizerpopRock.setStyleSheet("color: grey;")
         self.equalizertechno.setStyleSheet("color: grey;")
         self.equalizervocal.setStyleSheet("color: grey;")

   def update_bluetooth_track(self):
       #while not stop_reading.is_set():
         try:
             B = bluetooth_utils()
             track_info = B.run()
             self.Bluetooth_track.setText(track_info[0])
             self.Bluetooth_artist.setText(track_info[1])
             self.Bluetooth_album.setText(track_info[2])
             self.Bluetooth_timing.setText(track_info[3])
             self.Bluetooth_duration.setText(track_info[4])
             self.percent.setText(str(track_info[5]))
             self.custom_signals.update_progress_bluetooth_track_signal.emit()

         except:
             pass
         #time.sleep(.5)

   def close_all(self):
        # set flag of
        try :
            if reading_thread:
                stop_reading.set()
                reading_thread.join()
        except:
            pass
        try :
            if source_handler:
                source_handler.close()
        except:
            pass
                      
        logging.info("Fermeture de l'application")              
        #After closing threads, closing the window            
        self.close()

class Communicate(QObject):
    update_progress_bluetooth_track_signal = pyqtSignal()
    update_progress_volume_signal = pyqtSignal()

if __name__ == '__main__':
    run()
