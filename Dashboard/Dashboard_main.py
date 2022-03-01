#!/usr/bin/env python3

################# Libraries import  ####################
import sys
import threading
import traceback
import time
import os
import logging

################# UI components ####################
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap,QFontDatabase
from PyQt5.QtWidgets import QLabel

############ Libraries import from my files ###############
from source_handler import InvalidFrame, SerialHandler
from ombre import ombre
from sound_level import volumewindow
from alertMSG import alertmsg
from InfoMSG_parser import parseInfoMessage
from Media_control import mediacontrol
from Media_data import mediadata
from other.fakedata import retrievedatafromfile

############## Event for closing everything ##############
stop_reading = threading.Event()

################# Log file formatting #################
# write log in console (sys.stderr) and log file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/home/pi/lucas/log.txt')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)

################## USB Arduino parameters  #################
baudrate = 115200
serial_device = "/dev/ttyUSB0"

################## define global variable  #################
audiosettings = {
   'frontRearBalance' : '0',
   'leftRightBalance' : '0',
   'automaticVolume' : '0',
   'bass' : '0',
   'treble' : '0',
   'loudness' : '0',
   'source' : '0'
}

################# Testing mode if start with arg ################

try :
  testWithFakeData = bool(sys.argv[1] == 'test')
except IndexError :
  testWithFakeData = False
  
print('Mode Test' if testWithFakeData else 'Mode Normal')

################# string formating function ################
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
            msg_str += '.'
        elif ord(char) < 32 or ord(char) > 126:
            msg_str += '?'
        else:
            msg_str += char
    return msg_str

################## LOOP reading from Arduino  #################
""" 
Background thread for reading data from Arduino (and by extension the car)
and doing the corresponding action
"""
def reading_loop(source_handler, root):
    # FRAMETYPES and their IDs
    INIT_STATUS_FRAME    = 0x00
    VOLUME_FRAME         = 0x01
    TEMPERATURE_FRAME    = 0x02
    RADIO_SOURCE_FRAME   = 0x03
    RADIO_NAME_FRAME     = 0x04
    RADIO_FREQ_FRAME     = 0x05
    RADIO_FMTYPE_FRAME   = 0x06
    RADIO_DESC_FRAME     = 0x07
    INFO_MSG_FRAME       = 0x08
    RADIO_STATIONS_FRAME = 0x09
    KEY_FRAME            = 0x0A
    INFO_TRIP_FRAME      = 0x0C
    INFO_INSTANT_FRAME   = 0x0E
    AUDIO_SETTINGS_FRAME = 0x10
    REMOTE_COMMAND_FRAME = 0x11
    OPEN_DOOR_FRAME      = 0x12
    TIME_FRAME           = 0x13
    SHUTDOWN_FRAME       = 0x14

    # Dict of controls and their ID to send to mediacontrol()
    listcontrol = { 
                  1 : "enter",
                  2 : "scroll_left",
                  3 : "scroll_right",
                  4 : "down",
                  5 : "up" ,
                  6 : "back",
                  7 : "home"
                  }

    while not stop_reading.is_set():
        time.sleep(.05)
        frame_id, data = None, None

        if testWithFakeData :
          frame_id, data = retrievedatafromfile()
        else :
            try:
                frame_id, data = source_handler.get_message()
            except InvalidFrame:
                continue
            except EOFError:
                break

        if frame_id == INIT_STATUS_FRAME:
            logging.info("Init communication with arduino OK")

        elif frame_id == VOLUME_FRAME:
            text = str(data[0] & 0b00011111)
            root.Volume.setText(text)
            root.custom_signals.update_progress_volume_signal.emit()

            if not (data[0] & 0b11100000 == 0b11100000) and not root.Volumewindow.visible:
                root.Volumewindow.moveup()

            elif (data[0] & 0b11100000 == 0b11100000) and root.Volumewindow.visible:
                root.Volumewindow.movedown()

        elif frame_id == TEMPERATURE_FRAME:
            text = str(round(data[0]/2-39.5))+ "°C"
            root.Temperature.setText(text)
            root.Temperatureb.setText(text)
            
        elif frame_id == SHUTDOWN_FRAME:
            logging.info("Shuting DOWN")
            os.system("sudo shutdown now")

        elif frame_id == TIME_FRAME:
            text = f"{data[3]:02d}:{data[4]:02d}"
            root.heure.setText(text)
            root.heureb.setText(text)

        elif frame_id == REMOTE_COMMAND_FRAME:
            if (data[0] & 0b00001100) == 0b00001100:
                # Both button pressed : Pause/play
                mediacontrol("playpause")
            elif (data[0] & 0b10000000) == 0b10000000:
                # Next button pressed
                mediacontrol("next")
            elif (data[0] & 0b01000000) == 0b01000000:
                # Previous button pressed
                mediacontrol("previous")
                
        elif frame_id == KEY_FRAME :
                if data[0] in listcontrol :
                    logging.info(listcontrol[data[0]])
                    mediacontrol(listcontrol[data[0]])

        elif frame_id == OPEN_DOOR_FRAME:
            # Maybe Useless
            if (data[0] & 0b10000000) == 0b10000000:
                logging.info("Door Front Left")
            if (data[0] & 0b01000000) == 0b01000000:
                logging.info("Door Front Right")
            if (data[0] & 0b00100000) == 0b00100000:
                logging.info("Door Back Left")
            if (data[0] & 0b00010000) == 0b00010000:
                logging.info("Door Back Right")
            if (data[0] & 0b00001000) == 0b00001000:
                logging.info("Trunk Door")

        elif frame_id == RADIO_NAME_FRAME:
            root.RadioName.setText(format_data_ascii(data))

        elif frame_id == RADIO_FREQ_FRAME:
            temp = str(float(int(format_data_hex(data),16))/10)
            root.RadioFreq.setText(temp + "MHz")

        elif frame_id == RADIO_FMTYPE_FRAME:
            temp = data[0]

            if temp == 1:
                RadioFMType = "FM1"
            elif temp == 2:
                RadioFMType = "FM2"
            elif temp == 4:
                RadioFMType = "FMAST"
            elif temp == 5:
                RadioFMType = "AM"
            else :
                RadioFMType = "No Type"

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
            logging.info("Radio desc frame data : %s",temp)

        elif frame_id == INFO_MSG_FRAME:
            infomessage = parseInfoMessage(data)
            if infomessage != "Aucun message" :
              root.AlertMSG.texte.setText(infomessage)
              if not data[0] & 0b01110000:
                  root.show_alert()
              else:
                  root.hide_alert()
            else:
                root.hide_alert()

        elif frame_id == RADIO_STATIONS_FRAME:
            temp = format_data_ascii(data)
            logging.info("station liste : %s",temp)
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
            distanceafterreset = int(format_data_hex(distanceafterresetbyte), 16)
            text = f"{distanceafterreset}km"
            root.tripinfo1.setText(text)
            root.tripinfo1b.setText(text)

            averageFuelUsagebyte = bytes([data[3], data[4]])
            averageFuelUsage = int(format_data_hex(averageFuelUsagebyte), 16) / 10
            text = f"Moy : {averageFuelUsage}L/100km"
            root.tripinfo3.setText(text)
            root.tripinfo3b.setText(text)

        elif frame_id == INFO_INSTANT_FRAME:
            fuelleftbyte = bytes([data[3], data[4]])
            fuelleftbyte2 = int(format_data_hex(fuelleftbyte),16)
            text = f"Reste {fuelleftbyte2}km"
            root.tripinfo2.setText(text)
            root.tripinfo2b.setText(text)

            if (data[1] & 0b10000000) == 0b10000000:
                text = "Instant. : -- l/100km"
            else:
                consoinstantbyte = bytes([data[1], data[2]])
                consoinstantbyte2 = float(int(format_data_hex(consoinstantbyte), 16)) / 10
                text = f"Instant. : {consoinstantbyte2:.1f} l/100km"
            root.tripinfo4.setText(text)
            root.tripinfo4b.setText(text)

            if (data[0] & 0b00001000) == 0b00001000:
                # if Tripbutton pressed : switch window
                mediacontrol("mode")
                
        elif frame_id == AUDIO_SETTINGS_FRAME:
            # Active selected mode in audio settings
            switchToAudiosettingsTab = True
            if (data[0] & 0b10000000) == 0b10000000:
                root.resetaudiosettingselector()
                root.leftRightBalanceselector.setHidden(False)
                root.leftRightBalanceselector_2.setHidden(False)
            elif (data[1] & 0b10000000) == 0b10000000:
                root.resetaudiosettingselector()
                root.frontRearBalanceselector.setHidden(False)
                root.frontRearBalanceselector_2.setHidden(False)
            elif (data[2] & 0b10000000) == 0b10000000:
                root.resetaudiosettingselector()
                root.SliderBassesselector.setHidden(False)
                root.SliderBassesselector_2.setHidden(False)
            elif (data[4] & 0b10000000) == 0b10000000:
                root.resetaudiosettingselector()
                root.SliderAigusselector.setHidden(False)
                root.SliderAigusselector_2.setHidden(False)
            elif (data[5] & 0b10000000) == 0b10000000:
                root.resetaudiosettingselector()
                root.Loudnessselector.setHidden(False)
                root.Loudnessselector_2.setHidden(False)
            elif (data[5] & 0b00010000) == 0b00010000:
                root.resetaudiosettingselector()
                root.automaticVolumeselector.setHidden(False)
                root.automaticVolumeselector_2.setHidden(False)
            elif (data[6] & 0b01000000) == 0b01000000:
                root.resetaudiosettingselector()
                root.equalizerselector.setHidden(False)
                root.equalizerselector_2.setHidden(False)
            else:
                switchToAudiosettingsTab = False
                root.resetaudiosettingselector()

            # if a mode is active, switch to the audiosettings tab
            if switchToAudiosettingsTab:
                root.tabWidget.setCurrentIndex(2)
            else:
                if audiosettings['source'] == "OpenAuto":
                    root.tabWidget.setCurrentIndex(1)
                else:
                    root.tabWidget.setCurrentIndex(0)

            # Value of the equalizer Setting
            if (data[6] & 0b10111111) == 0b00000011:
                root.resetequalizerselector()
                root.equalizernone.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00000111:
                root.resetequalizerselector()
                root.equalizerclassical.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00001011:
                root.resetequalizerselector()
                root.equalizerjazzBlues.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00001111:
                root.resetequalizerselector()
                root.equalizerpopRock.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00010011:
                root.resetequalizerselector()
                root.equalizervocal.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00010111:
                root.resetequalizerselector()
                root.equalizertechno.setStyleSheet("color: white;")

            # saving every setting in the audiosettings[] dict
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

        elif frame_id is not None:
            logging.info(f"FRAME ID NON TRAITE : {frame_id} : {format_data_hex(data)}  {format_data_ascii(data)}")



###################### Main start of the program ###################
def run():
    source_handler = SerialHandler(serial_device, baudrate )
    # Reading from a serial device, opened with timeout=0 (non-blocking read())

    source_handler.open()

    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    root = Ui()  # Create an instance of our class for the MainWindow

    # Create Thread for the reading loop , args : source_handler for USB & root for UI
    reading_thread = threading.Thread(target=reading_loop, args=(source_handler, root,))
    # Start the reading in background thread
    reading_thread.start()

    # Create Thread for the media data loop , args :  root for UI
    mediadata_thread = threading.Thread(target=mediadata, args=(root,))
    # Start the reading in background thread
    mediadata_thread.start()

    app.exec_()

class Ui(QtWidgets.QMainWindow):
   ''' Define the main window of the app '''
   def update_progress_media_track(self):
       try:
           self.media_progressBar.setValue(int(float(self.percent.text())))
       except TypeError:
           logging.info("Wrong type of value for track position")

   def update_progress_volume(self):
       try:
           self.Volumewindow.progress.setValue(int(self.Volume.text()))
       except TypeError:
           logging.info("Wrong type of value for Volume")

   def __init__(self):
        super().__init__()  # Call the inherited classes __init__ method
        uic.loadUi('/home/pi/lucas/interface.ui', self)  # Load the .ui Mainwindow file
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)

        #Initialisation of the window
        self.Ombre = ombre()
        self.AlertMSG = alertmsg()
        self.Volumewindow = volumewindow()

        # Init both tabs
#         self.tabWidget.setCurrentIndex(0)
#         self.tabWidget.setCurrentIndex(1)

        self.showMaximized()  # Show the GUI

        # Init of the custom signals that connects to the progress bars
        self.custom_signals = Communicate()
        self.custom_signals.update_progress_media_track_signal.connect(self.update_progress_media_track)
        self.custom_signals.update_progress_volume_signal.connect(self.update_progress_volume)

        # Init radio list
        self.radioList0.setText('')
        self.radioList1.setText('')
        self.radioList2.setText('')
        self.radioList3.setText('')
        self.radioList4.setText('')
        self.radioList5.setText('')

   def show_alert(self):
         self.Ombre.showMaximized()
         self.AlertMSG.show()

   def hide_alert(self):
         self.Ombre.hide()
         self.AlertMSG.hide()

   def resetaudiosettingselector(self) :
         #Each selector display go hidden
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

   def close_all(self):
        # set flag off
        if reading_thread.is_alive():
            stop_reading.set()
            reading_thread.join()
        if source_handler.is_alive():
            source_handler.close()
        logging.info("Fermeture de l'application")
        #After closing threads, closing the window
        self.close()

class Communicate(QObject):
    ''' create  signals for the progress bars '''
    update_progress_media_track_signal = pyqtSignal()
    update_progress_volume_signal = pyqtSignal()

if __name__ == '__main__':
    run()
