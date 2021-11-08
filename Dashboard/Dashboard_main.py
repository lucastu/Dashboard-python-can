#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import sys
import threading
import traceback
import time
import os
import logging
import RPi.GPIO as GPIO   
from functools import partial

from source_handler import InvalidFrame, SerialHandler
from sound_level import volumewindow
from ombre import ombre
from alertMSG import alertmsg
from InfoMSG_parser import parseInfoMessage
from Bluetooth_utils import bluetooth_utils
#Display on the device display in case of SSH launch of the script
# os.environ.__setitem__('DISPLAY', ':0.0')
stop_reading = threading.Event()

# can_messages = {}
# can_messages_lock = threading.Lock()

# thread_exception = None

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
   'activeMode' : '0',
   'frontRearBalance' : '0',
   'leftRightBalance' : '0',
   'automaticVolume' : '0',
   'equalizer' : '0',
   'bass' : '0',
   'treble' : '0',
   'loudness' : '0',
}

def reading_loop(source_handler, root):
    """Background thread for reading data from Arduino."""
    #FRAMETYPES and their IDs
    INIT_STATUS_FRAME =    0x00
    VOLUME_FRAME =         0x01
    TEMPERATURE_FRAME =    0x02
    RADIO_SOURCE_FRAME =   0x03
    RADIO_NAME_FRAME =     0x04
    RADIO_FREQ_FRAME =     0x05
    RADIO_FMTYPE_FRAME =   0x06
    RADIO_DESC_FRAME =     0x07
    INFO_MSG_FRAME =       0x08
    RADIO_STATIONS_FRAME = 0x09
    INFO_TRIP_FRAME =     0x0C
    # INFO_TRIP2_FRAME =     0x0D
    INFO_INSTANT_FRAME =   0x0E
    # TRIP_MODE_FRAME =      0x0F
    AUDIO_SETTINGS_FRAME = 0x10
    REMOTE_COMMAND_FRAME = 0x11  
    OPEN_DOOR_FRAME      = 0x12
    # RADIO_FACE_BUTTON =    0x13
    SHUTDOWN_FRAME    =    0x14

    while not stop_reading.is_set():
        try:
            frame_id, data = source_handler.get_message()
        except InvalidFrame:
            continue
        except EOFError:
            break

        if frame_id == VOLUME_FRAME:
            temp = str(data[0] & 0b00011111)
            root.Volume.setText(temp)
            root.custom_signals.update_progress_volume_signal.emit()

            if (not (data[0] & 0b11100000 == 0b11100000)) and (not root.Volumewindow.visible):
                root.Volumewindow.moveup()

            elif ((data[0] & 0b11100000 == 0b11100000) and root.Volumewindow.visible):
                root.Volumewindow.movedown()
            
        elif frame_id == INIT_STATUS_FRAME:
            logging.info("Init communication with arduino OK")
            
        elif frame_id == SHUTDOWN_FRAME:
            logging.info("Shut down data : " + data[0])
            #os.system("sudo shutdown -h now")
            
        elif frame_id == REMOTE_COMMAND_FRAME:
            #logging.info("REMOTE_COMMAND_FRAME data : " + str(data[0]))
            if ((data[0] & 0b00001100) == 0b11001100) :
                #Both button pressed : Pause/play      
                cmd = 'xdotool key B'
                os.system(cmd)
                logging.info("Play pause track")
            elif ((data[0] & 0b10000000) == 0b10000000) :
                #Next button pressed
                cmd = 'xdotool key N'
                os.system(cmd)
                logging.info("Next track")
            elif ((data[0] & 0b01000000) == 0b01000000) :
                #Previous button pressed
                cmd = 'xdotool key V'
                os.system(cmd)
                logging.info("Previous track") 
               
        elif frame_id == OPEN_DOOR_FRAME:
            if (data[0] & 0b10000000) == 0b10000000 :
                #Door Front Left     
                logging.info("Door Front Left")
            if (data[0] & 0b01000000) == 0b01000000 :
                #Door Front Right
                logging.info("Door Front Right")
            if (data[0] & 0b00100000) == 0b00100000 :
                #Door Back Left
                logging.info("Door Back Left")
            if (data[0] & 0b00010000) == 0b00010000 :
                #Door Back Right
                logging.info("Door Back Right")
            if (data[0] & 0b00001000) == 0b00001000 :
                #Door Trunk    
                logging.info("Door Trunk ")
      
        elif frame_id == TEMPERATURE_FRAME:
            temp = str(data[0])
            root.Temperature.setText( temp + "°C")

        elif frame_id == RADIO_NAME_FRAME:
            root.RadioName.setText(format_data_ascii(data))

        elif frame_id == RADIO_FREQ_FRAME:
            temp = format_data_hex(data)
            root.RadioFreq.setText(str(float(int(temp,16))/10)+ "MHz")                                            

        elif frame_id == RADIO_FMTYPE_FRAME:
            temp = data[0]
            radioFMType ="No Type"
            if temp == 1:
                RadioFMType ="FM1"
            elif temp == 2:
                RadioFMType ="FM2"
            elif temp == 4:
                RadioFMType ="FMAST"
            elif temp == 5 :
                RadioFMType ="AM"
            root.RadioType.setText("Radio "+ RadioFMType)

        elif frame_id == RADIO_SOURCE_FRAME:
            temp = data[0]
            Source = "Aucune source..."
            if temp == 1:
                Source = "Tuner"
            elif temp == 2:
                Source = "cd"
            elif temp == 3:
                Source = "OpenAuto"
            elif temp == 4:
                Source = "AUX1"
            elif temp == 5:
                Source = "AUX2"
            elif temp == 6:
                Source = "USB"
            elif temp == 7:
                Source = "BLUETOOTH"
            root.RadioSource.setText(Source)                 
                  
        elif frame_id == RADIO_DESC_FRAME:
            temp = format_data_ascii(data)      
            root.RadioDesc.setText(temp)
            #This one never worked....
            logging.info("Radio desc frame data : %s  " % temp)
                  
        elif frame_id == INFO_MSG_FRAME:
            infomessage = parseInfoMessage(data, root)
            root.InfoMSG.setText(infomessage)
            root.AlertMSG.texte.setText(infomessage)
            
            if not (data[0] & 0b01110000) :
               root.show_alert()
            else :
               root.hide_alert()
                  
        elif frame_id == RADIO_STATIONS_FRAME:
            temp = format_data_ascii(data)
            logging.info("station liste : " + temp)
            if '|' in temp:
                radio_list = temp.split("|")
                root.radioList0.setText("1 : "+ radio_list[0])
                root.radioList1.setText("2 : "+ radio_list[1])
                root.radioList2.setText("3 : "+ radio_list[2])
                root.radioList3.setText("4 : "+ radio_list[3])
                root.radioList4.setText("5 : "+ radio_list[4])
                root.radioList5.setText("6 : "+ radio_list[5])

        elif frame_id == INFO_TRIP_FRAME :
            #a mettre en forme mais tout correspond, mais je m'en fout ?
            #root.tripinfo3.setText("Vitesse moyenne : %s km/h" % (data[0]))
                                            
            distanceafterresetbyte= bytes([data[1],data[2]])
            distanceafterreset =int((''.join('%02X' % byte for byte in distanceafterresetbyte)),16)                   
            logging.info("Distance after reset : %s" % distanceafterreset )
            root.tripinfo1.setText("Distance trajet : %skm" % distanceafterreset)
                                             
            averageFuelUsagebyte= bytes([data[3],data[4]])
            averageFuelUsage =int((''.join('%02X' % byte for byte in averageFuelUsagebyte)),16)/10
            root.tripinfo3.setText("Conso moyenne : %sL/100km" % averageFuelUsage)

            
        elif frame_id == INFO_INSTANT_FRAME :
            fuelleftbyte= bytes([data[3],data[4]])
            fuelleftbyte2=''.join('%02X' % byte for byte in fuelleftbyte)
            root.tripinfo2.setText("Reste en essence : %skm" % (int(fuelleftbyte2,16)))
            
            if (data[1] & 0b10000000) == 0b10000000 : 
              root.tripinfo4.setText("conso instantanée : -- ")
            else :                                
              consoinstantbyte= bytes([data[1],data[2]])
              consoinstantbyte2=''.join('%02X' % byte for byte in consoinstantbyte)                                               
              root.tripinfo4.setText("conso instantanée : %s " + str(float(int(consoinstantbyte2,16))/10))

            if (data[0] & 0b00001000) == 0b00001000 :
                # if Tripbutton pressed : switch window
                cmd = 'xdotool keydown  alt +Tab keyup alt+Tab'
                os.system(cmd)

        #elif frame_id == TRIP_MODE_FRAME:
        #    #temp = int(format_data_hex(data))
        #    #Maybe useless for my integration ?
        #    temp = data[0]
        #    tripInfoMode =""
        #    if temp == 0:
        #        tripInfoMode = "instant"
        #    elif temp == 1:
        #        tripInfoMode = "trip1"
        #    elif temp == 2:
        #        tripInfoMode = "trip2"
        #    root.tripInfoMode.setText(tripInfoMode)

        elif frame_id == AUDIO_SETTINGS_FRAME:
            #activeMode = 0
            #equalizerSetting = 0             
                  
            #Active selected mode in audio settings      
            if (data[0] & 0b10000000) == 0b10000000 :
                activeMode = 1  # .leftRightBalance
                root.resetaudiosettingselector()
                root.leftRightBalanceselector.setHidden(False)
                root.leftRightBalanceselector_2.setHidden(False)
            elif (data[1] & 0b10000000) == 0b10000000 :
                activeMode = 2  # .frontRearBalance
                root.resetaudiosettingselector()
                root.frontRearBalanceselector.setHidden(False)
                root.frontRearBalanceselector_2.setHidden(False)
            elif (data[2] & 0b10000000) == 0b10000000 :
                activeMode = 3  # .bass
                root.resetaudiosettingselector()
                root.SliderBassesselector.setHidden(False)
                root.SliderBassesselector_2.setHidden(False)
            elif (data[4] & 0b10000000) == 0b10000000 :
                activeMode = 4  # .treble
                root.resetaudiosettingselector()
                root.SliderAigusselector.setHidden(False)
                root.SliderAigusselector_2.setHidden(False)
            elif (data[5] & 0b10000000) == 0b10000000 :
                activeMode = 5  # .loudness
                root.resetaudiosettingselector()
                root.Loudnessselector.setHidden(False)
                root.Loudnessselector_2.setHidden(False)
            elif (data[5] & 0b00000001) == 0b00000001 :
                activeMode = 6  # .automaticVolume
                root.resetaudiosettingselector()
                root.automaticVolumeselector.setHidden(False)
                root.automaticVolumeselector_2.setHidden(False)
            elif (data[6] & 0b01000000) == 0b01000000 :
                activeMode = 7  # .equalizer
                root.resetaudiosettingselector()
                root.equalizerselector.setHidden(False)
                root.equalizerselector_2.setHidden(False)
                print("value 1 OK")
            elif (data[6] & 0b10000000) == 0b10000000 :
                activeMode = 7  # .equalizer
                root.resetaudiosettingselector()
                root.equalizerselector.setHidden(False)
                root.equalizerselector_2.setHidden(False)    
                print("value 2 OK")
            else :
                activeMode = 0
                root.resetaudiosettingselector()

            #Valeur de l'equalizer Setting
            if (data[6] & 0b10111111) ==  0b00000011 :
                equalizerSetting = 0  # .none
                root.resetequalizerselector()
                root.equalizernone.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) ==  0b00000111 :
                equalizerSetting = 1  # .classical
                root.resetequalizerselector()
                root.equalizerclassical.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00001011 :
                equalizerSetting = 2  # .jazzBlues
                root.resetequalizerselector()
                root.equalizerjazzBlues.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00001111 :
                equalizerSetting = 3  # .popRock
                root.resetequalizerselector()
                root.equalizerpopRock.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00010011 :
                equalizerSetting = 4  # .vocals
                root.resetequalizerselector()
                root.equalizervocal.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00010111 :
                equalizerSetting = 5  # .techno
                root.resetequalizerselector()
                root.equalizertechno.setStyleSheet("color: white;")  
                  
            #Enregistrement de toutes ces variables dans le dictionnaire audiosettings
            audiosettings['activeMode']         = activeMode
            audiosettings['frontRearBalance']   = int(data[1] & 0b01111111) - 63
            audiosettings['leftRightBalance']   = int(data[0] & 0b01111111) - 63
            audiosettings['automaticVolume']    = (data[5] & 0b00000111) == 0b00000111
            #audiosettings['equalizer']          = equalizerSetting
            audiosettings['bass']               = int(data[2] & 0b01111111) - 63
            audiosettings['treble']             = int(data[4] & 0b01111111) - 63
            audiosettings['loudness']           = ((data[5] & 0b01000000) == 0b01000000)
             
            #Update de l'affichage dans l'onglet Settings
            root.SliderBasses.setValue(audiosettings['bass'])
            root.SliderAigus.setValue(audiosettings['treble'])
            root.frontRearBalance.setValue(audiosettings['frontRearBalance'])
            root.leftRightBalance.setValue(audiosettings['leftRightBalance'])                      
            root.Loudness.setChecked(audiosettings['loudness'])
            root.automaticVolume.setChecked(audiosettings['automaticVolume'])
            root.equalizer.setText(str(audiosettings['equalizer']))

        else:
            logging.info ("FRAME ID NON TRAITE : %s  :  %s  %s" % (frame_id, format_data_hex(data), format_data_ascii(data)))

        # f there is an activeMode of audio settings, switch to the audiosettings tab 
        # if audiosettings['activeMode'] != 0 :
        #     root.tabWidget.setCurrentIndex(1)
        # else :
        #     root.tabWidget.setCurrentIndex(0)


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
    # reading_thread = None
    # Reading from a serial device, opened with timeout=0 (non-blocking read())
    source_handler.open()

    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    root = Ui()  # Create an instance of our class for the MainWindow

    # Create Thread for the reading loop , args : source_handler for USB & root for UI
    reading_thread = threading.Thread(target=reading_loop, args=(source_handler, root,))
    # Start the reading in background thread              
    reading_thread.start()

    B_read =threading.Thread(target=root.update_bluetooth_track)
    B_read.start()
    app.exec_()


class Ui(QtWidgets.QMainWindow):
   def update_progress_bluetooth_track(self):
       try:
           self.Bluetooth_progressBar.setValue(int(float(self.percent.text())))
       except:
           logging.info("Wrong type of value for track position")

   def update_progress_volume(self):
       # self.Volume.setText('5')
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

        self.AlertONbutton.clicked.connect(self.show_alert)
        self.AlertOFFbutton.clicked.connect(self.hide_alert)
        self.closebutton.clicked.connect(self.close_all)
        self.Switchtab.clicked.connect(self.switchtab)
        self.Switchtab1.clicked.connect(self.switchtab)
        self.showMaximized()  # Show the GUI

        self.custom_signals = Communicate()
        self.custom_signals.update_progress_bluetooth_track_signal.connect(self.update_progress_bluetooth_track)
        self.custom_signals.update_progress_volume_signal.connect(self.update_progress_volume)
        # self.custom_signals.update_progress_volume_signal.emit()


   def switchtab(self):
       if self.tabWidget.currentIndex() :
           self.tabWidget.setCurrentIndex(0)
       else :
           self.tabWidget.setCurrentIndex(1)

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
         self.SliderBassesselector.setHidden(True)
         self.SliderBassesselector_2.setHidden(True)
         self.SliderAigusselector.setHidden(True)
         self.SliderAigusselector_2.setHidden(True)
         self.frontRearBalanceselector.setHidden(True)
         self.frontRearBalanceselector_2.setHidden(True)
         self.leftRightBalanceselector.setHidden(True)
         self.leftRightBalanceselector_2.setHidden(True)
         self.Loudnessselector.setHidden(True)
         self.Loudnessselector_2.setHidden(True)
         self.automaticVolumeselector.setHidden(True)
         self.automaticVolumeselector_2.setHidden(True)
         self.equalizerselector.setHidden(True)
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
       while True :
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
             time.sleep(.5)
         except:
             pass
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
        # If the thread returned an exception, print it
        if thread_exception:
             #traceback.print_exception(*thread_exception)
             sys.stderr.flush()
                      
        logging.info("Fermeture de l'application")              
        #After closing threads, closing the window            
        self.close()

class Communicate(QObject):
    update_progress_bluetooth_track_signal = pyqtSignal()
    update_progress_volume_signal = pyqtSignal()

if __name__ == '__main__':
    run()
