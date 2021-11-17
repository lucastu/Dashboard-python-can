#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap,QFontDatabase
from PyQt5.QtWidgets import QLabel
import sys
import threading
import traceback
import time
import os
import logging  
from functools import partial

#Imports classes and function from my files
from source_handler import InvalidFrame, SerialHandler
from sound_level import volumewindow
from ombre import ombre
from alertMSG import alertmsg
from InfoMSG_parser import parseInfoMessage
from Bluetooth_utils import bluetooth_utils

# Event for closing everything
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


def reading_loop(source_handler, root):
    """Background thread for reading data from Arduino."""
    # FRAMETYPES and their IDs
    INIT_STATUS_FRAME = 0x00
    VOLUME_FRAME = 0x01
    TEMPERATURE_FRAME = 0x02
    RADIO_SOURCE_FRAME = 0x03
    RADIO_NAME_FRAME = 0x04
    RADIO_FREQ_FRAME = 0x05
    RADIO_FMTYPE_FRAME = 0x06
    RADIO_DESC_FRAME = 0x07
    INFO_MSG_FRAME = 0x08
    RADIO_STATIONS_FRAME = 0x09
    INFO_TRIP_FRAME = 0x0C
    INFO_INSTANT_FRAME = 0x0E
    AUDIO_SETTINGS_FRAME = 0x10
    REMOTE_COMMAND_FRAME = 0x11
    OPEN_DOOR_FRAME = 0x12
    SHUTDOWN_FRAME = 0x14

    # Init for the bluetooth command
    B = bluetooth_utils()
    
    while not stop_reading.is_set():
        time.sleep(.05)
        try:
            frame_id, data = source_handler.get_message()
        except InvalidFrame:
            continue
        except EOFError:
            break

        if frame_id == VOLUME_FRAME:
            text = str(data[0] & 0b00011111)
            root.Volume.setText(text)
            root.custom_signals.update_progress_volume_signal.emit()

            if (not (data[0] & 0b11100000 == 0b11100000)) and (not root.Volumewindow.visible):
                root.Volumewindow.moveup()

            elif ((data[0] & 0b11100000 == 0b11100000) and root.Volumewindow.visible):
                root.Volumewindow.movedown()

        elif frame_id == INIT_STATUS_FRAME:
            logging.info("Init communication with arduino OK")

        elif frame_id == SHUTDOWN_FRAME:
            logging.info("Shut down data : " + data[0])
            # os.system("sudo shutdown -h now")

        elif frame_id == REMOTE_COMMAND_FRAME:
            if (data[0] & 0b00001100) == 0b00001100:
                # Both button pressed : Pause/play
                B.control('playpause')
            elif (data[0] & 0b10000000) == 0b10000000:
                # Next button pressed
                B.control('next')
            elif (data[0] & 0b01000000) == 0b01000000:
                # Previous button pressed
                B.control('pre')

        elif frame_id == OPEN_DOOR_FRAME:
            # Maybe Useless
            if (data[0] & 0b10000000) == 0b10000000:
                # Door Front Left
                logging.info("Door Front Left")
            if (data[0] & 0b01000000) == 0b01000000:
                # Door Front Right
                logging.info("Door Front Right")
            if (data[0] & 0b00100000) == 0b00100000:
                # Door Back Left
                logging.info("Door Back Left")
            if (data[0] & 0b00010000) == 0b00010000:
                # Door Back Right
                logging.info("Door Back Right")
            if (data[0] & 0b00001000) == 0b00001000:
                # Door Trunk
                logging.info("Trunk Door")

        elif frame_id == TEMPERATURE_FRAME:
            text = str(data[0]) + "°C"
            root.Temperature.setText(text)
            root.Temperatureb.setText(text)

        elif frame_id == RADIO_NAME_FRAME:
            root.RadioName.setText(format_data_ascii(data))

        elif frame_id == RADIO_FREQ_FRAME:
            temp = format_data_hex(data)
            root.RadioFreq.setText(str(float(int(temp, 16)) / 10) + "MHz")

        elif frame_id == RADIO_FMTYPE_FRAME:
            temp = data[0]
            radioFMType = "No Type"
            if temp == 1:
                RadioFMType = "FM1"
            elif temp == 2:
                RadioFMType = "FM2"
            elif temp == 4:
                RadioFMType = "FMAST"
            elif temp == 5:
                RadioFMType = "AM"
            root.RadioType.setText("Radio " + RadioFMType)

        elif frame_id == RADIO_SOURCE_FRAME:
            temp = data[0]
            Source = "Aucune source..."
            if temp == 1:
                Source = "Tuner"
                root.tabWidget.setCurrentIndex(0)
            elif temp == 2:
                Source = "cd"
            elif temp == 3:
                Source = "OpenAuto"
                root.tabWidget.setCurrentIndex(1)
            elif temp == 4:
                Source = "AUX1"
            elif temp == 5:
                Source = "AUX2"
            elif temp == 6:
                Source = "USB"
            elif temp == 7:
                Source = "BLUETOOTH"
            audiosettings['source'] = Source

        elif frame_id == RADIO_DESC_FRAME:
            temp = format_data_ascii(data)
            # This one never worked....
            logging.info("Radio desc frame data : %s  " % temp)

        elif frame_id == INFO_MSG_FRAME:
            infomessage = parseInfoMessage(data, root)
            root.AlertMSG.texte.setText(infomessage)
            if not (data[0] & 0b01110000):
                root.show_alert()
            else:
                root.hide_alert()

        elif frame_id == RADIO_STATIONS_FRAME:
            temp = format_data_ascii(data)
            logging.info("station liste : " + temp)
            if '|' in temp:
                radio_list = temp.split("|")
                root.radioList0.setText("1 : " + radio_list[0])
                root.radioList1.setText("2 : " + radio_list[1])
                root.radioList2.setText("3 : " + radio_list[2])
                root.radioList3.setText("4 : " + radio_list[3])
                root.radioList4.setText("5 : " + radio_list[4])
                root.radioList5.setText("6 : " + radio_list[5])

        elif frame_id == INFO_TRIP_FRAME:
            distanceafterresetbyte = bytes([data[1], data[2]])
            distanceafterreset = int((''.join('%02X' % byte for byte in distanceafterresetbyte)), 16)
            text = "Reste %skm" % distanceafterreset
            root.tripinfo1.setText(text)
            root.tripinfo1b.setText(text)

            averageFuelUsagebyte = bytes([data[3], data[4]])
            averageFuelUsage = int((''.join('%02X' % byte for byte in averageFuelUsagebyte)), 16) / 10
            text = "Moyenne : %sL/100km" % averageFuelUsage
            root.tripinfo3.setText(text)
            root.tripinfo3b.setText(text)


        elif frame_id == INFO_INSTANT_FRAME:
            fuelleftbyte = bytes([data[3], data[4]])
            fuelleftbyte2 = ''.join('%02X' % byte for byte in fuelleftbyte)
            text = "%skm" % (int(fuelleftbyte2, 16))
            root.tripinfo2.setText(text)
            root.tripinfo2b.setText(text)

            if (data[1] & 0b10000000) == 0b10000000:
                text = "conso instantanée : -- "
            else:
                consoinstantbyte = bytes([data[1], data[2]])
                consoinstantbyte2 = ''.join('%02X' % byte for byte in consoinstantbyte)
                text = "conso instantanée : %s " + str(float(int(consoinstantbyte2, 16)) / 10)
            root.tripinfo4.setText(text)
            root.tripinfo4b.setText(text)

            if (data[0] & 0b00001000) == 0b00001000:
                # if Tripbutton pressed : switch window
                cmd = 'xdotool keydown  alt +Tab keyup alt+Tab'
                os.system(cmd)

        elif frame_id == AUDIO_SETTINGS_FRAME:
            # Active selected mode in audio settings
            switchToAudiosettingsTab = True
            if (data[0] & 0b10000000) == 0b10000000:
                # .leftRightBalance
                root.resetaudiosettingselector()
                root.leftRightBalanceselector.setHidden(False)
                root.leftRightBalanceselector_2.setHidden(False)
            elif (data[1] & 0b10000000) == 0b10000000:
                # .frontRearBalance
                root.resetaudiosettingselector()
                root.frontRearBalanceselector.setHidden(False)
                root.frontRearBalanceselector_2.setHidden(False)
            elif (data[2] & 0b10000000) == 0b10000000:
                # .bass
                root.resetaudiosettingselector()
                root.SliderBassesselector.setHidden(False)
                root.SliderBassesselector_2.setHidden(False)
            elif (data[4] & 0b10000000) == 0b10000000:
                # .treble
                root.resetaudiosettingselector()
                root.SliderAigusselector.setHidden(False)
                root.SliderAigusselector_2.setHidden(False)
            elif (data[5] & 0b10000000) == 0b10000000:
                # .loudness
                root.resetaudiosettingselector()
                root.Loudnessselector.setHidden(False)
                root.Loudnessselector_2.setHidden(False)
            elif (data[5] & 0b00010000) == 0b00010000:
                # .automaticVolume
                root.resetaudiosettingselector()
                root.automaticVolumeselector.setHidden(False)
                root.automaticVolumeselector_2.setHidden(False)
            elif (data[6] & 0b01000000) == 0b01000000:
                # .equalizer
                root.resetaudiosettingselector()
                root.equalizerselector.setHidden(False)
                root.equalizerselector_2.setHidden(False)
            else:
                switchToAudiosettingsTab = False
                root.resetaudiosettingselector()

            # If amode is active, switch to the audiosettings tab
            if switchToAudiosettingsTab:
                root.tabWidget.setCurrentIndex(2)
            else:
                if audiosettings['source'] == "OpenAuto":
                    root.tabWidget.setCurrentIndex(1)
                else:
                    root.tabWidget.setCurrentIndex(0)

            # Valeur de l'equalizer Setting
            if (data[6] & 0b10111111) == 0b00000011:
                # .none
                root.resetequalizerselector()
                root.equalizernone.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00000111:
                # .classical
                root.resetequalizerselector()
                root.equalizerclassical.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00001011:
                # .jazzBlues
                root.resetequalizerselector()
                root.equalizerjazzBlues.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00001111:
                # .popRock
                root.resetequalizerselector()
                root.equalizerpopRock.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00010011:
                # .vocals
                root.resetequalizerselector()
                root.equalizervocal.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00010111:
                # .techno
                root.resetequalizerselector()
                root.equalizertechno.setStyleSheet("color: white;")

                # Enregistrement de toutes ces variables dans le dictionnaire audiosettings
            audiosettings['frontRearBalance'] = int(data[1] & 0b01111111) - 63
            audiosettings['leftRightBalance'] = int(data[0] & 0b01111111) - 63
            audiosettings['automaticVolume'] = (data[5] & 0b00000111) == 0b00000111
            audiosettings['bass'] = int(data[2] & 0b01111111) - 63
            audiosettings['treble'] = int(data[4] & 0b01111111) - 63
            audiosettings['loudness'] = ((data[5] & 0b01000000) == 0b01000000)

            # Update de l'affichage dans l'onglet Settings
            root.SliderBasses.setValue(audiosettings['bass'])
            root.SliderAigus.setValue(audiosettings['treble'])
            root.frontRearBalance.setValue(audiosettings['frontRearBalance'])
            root.leftRightBalance.setValue(audiosettings['leftRightBalance'])
            root.Loudness.setChecked(audiosettings['loudness'])
            root.automaticVolume.setChecked(audiosettings['automaticVolume'])
            
        else:
            logging.info(
                "FRAME ID NON TRAITE : %s  :  %s  %s" % (frame_id, format_data_hex(data), format_data_ascii(data)))

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

    # Timer that execute Bluetooth_reading_loop function every 500ms
    Bluetooth_timer = QtCore.QTimer()
    Bluetooth_timer.timeout.connect(root.update_bluetooth_track)
    Bluetooth_timer.start(500)
   
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

        # Init of the custom signals that connects to the progress bars
        self.custom_signals = Communicate()
        self.custom_signals.update_progress_bluetooth_track_signal.connect(self.update_progress_bluetooth_track)
        self.custom_signals.update_progress_volume_signal.connect(self.update_progress_volume)

        # Init radio list
        self.radioList0.setText('')
        self.radioList1.setText('')
        self.radioList2.setText('')
        self.radioList3.setText('')
        self.radioList4.setText('')
        self.radioList5.setText('')

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

   def close_all(self):
        # set flag off
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
