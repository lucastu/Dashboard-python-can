#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import pyqtSignal

import sys
import threading
#import traceback
import time
import os
import logging
import RPi.GPIO as GPIO   

from source_handler import InvalidFrame, SerialHandler
from sound_level import volumewindow
from ombre import ombre
from alertMSG import alertmsg
from InfoMSG_parser import parseInfoMessage

#Display on the device display in case of SSH launch of the script
os.environ.__setitem__('DISPLAY', ':0.0')
# os.environ["QT_LOGGING_RULES"] = "qt5ct.debug=false"
stop_reading = threading.Event()

# If the app is started, RPI_State_PIN set to True
RPI_State_PIN = 0
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
GPIO.setup(RPI_State_PIN, GPIO.OUT) # set a port/pin as an output   
GPIO.output(RPI_State_PIN, 1)       # set port/pin value to 1/GPIO.HIGH/True 

can_messages = {}
can_messages_lock = threading.Lock()

thread_exception = None

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
   
      
    INFO_TRIP1_FRAME =     0x0C
    INFO_TRIP2_FRAME =     0x0D
    INFO_INSTANT_FRAME =   0x0E
    TRIP_MODE_FRAME =      0x0F
    AUDIO_SETTINGS_FRAME = 0x10
    REMOTE_COMMAND_FRAME = 0x11  
    OPEN_DOOR_FRAME      = 0x12
    # RADIO_FACE_BUTTON =    0x13
    SHUTDOWN_FRAME    =    0x14

    self.signals = Communicate()
    
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
            root.Volumewindow.progress.setValue(int(temp))   
            
            self.signals.signal_int.connect(root.Volumewindow.progress.setValue(int(temp))
            
            if (not (data[0] & 0b11100000 == 0b11100000)) and (not root.Volumewindow.visible) :
                root.Volumewindow.moveup()

            elif ((data[0] & 0b11100000 == 0b11100000) and root.Volumewindow.visible):
                root.Volumewindow.movedown()
            
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
            #after mod of format_data_hex to remove ' '
            #root.RadioFreq.setText(str(float(int(temp.replace(" ", ""),16))/10)+ "MHz")
            root.RadioFreq.setText(str(float(int(temp,16))/10)+ "MHz")                                            

        elif frame_id == RADIO_FMTYPE_FRAME:
            #if that                                 
            #temp = int(format_data_hex(data))
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
                                            
           # temp = int(format_data_ascii(data))
            temp = data[0]
            Source = "Aucune source..."
            if temp == 1:
                Source = "Tuner"
            elif temp == 2:
                Source = "cd"
            elif temp == 3:
                Source = "CDC"
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
            #PARSER LE PREMIER 
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

        elif frame_id == INFO_TRIP1_FRAME :
            #a mettre en forme mais tout correspond
            root.tripinfo3.setText("Vitesse moyenne : %s km/h" % (data[0]))
                                            
            distanceafterresetbyte= bytes([data[1],data[2]])
            distanceafterreset =int((''.join('%02X' % byte for byte in distanceafterresetbyte)),16)                   
            logging.info("Distance after reset : %s" % distanceafterreset )
            root.tripinfo1.setText("Distance after reset : %s" % distanceafterreset)
                                            
            #averageFuelUsage=int(data[3]+data[4])/10
            #root.tripinfo2.setText("Conso. moyenne : %s l/100km " % averageFuelUsage)
                                            
            averageFuelUsagebyte= bytes([data[1],data[2]])
            averageFuelUsage =int((''.join('%02X' % byte for byte in averageFuelUsagebyte)),16)                   
            logging.info("Conso moyenne : %s" % averageFuelUsage )
            root.tripinfo1.setText("Conso moyenne : %sl/100km" % averageFuelUsage)  
                                            
        elif  frame_id == INFO_TRIP2_FRAME :
            distanceafterresetbyte= bytes([data[1],data[2]])
            distanceafterreset =int((''.join('%02X' % byte for byte in distanceafterresetbyte)),16)                   
            logging.info("Distance after reset2 : %s" % distanceafterreset )
            root.tripinfo4.setText("Distance 2 : %s" % distanceafterreset)
                                            
            root.tripinfo6.setText("Vitesse moy2 : %s km/h" % (data[0]))                                            
                                            
            averageFuelUsagebyte= bytes([data[1],data[2]])
            averageFuelUsage =int((''.join('%02X' % byte for byte in averageFuelUsagebyte)),16)                   
            logging.info("Conso moyenne2 : %s" % averageFuelUsage )
            root.tripinfo5.setText("Conso moyenne2 : %sl/100km" % averageFuelUsage)                                            
            
        elif frame_id == INFO_INSTANT_FRAME :
            fuelleftbyte= bytes([data[3],data[4]])
            fuelleftbyte2=''.join('%02X' % byte for byte in fuelleftbyte)                   
            logging.info("Reste en essence : %s" % (int(fuelleftbyte2,16)))
                                            
            if (data[0] & 0b10000000) == 0b10000000 : 
              root.tripinfo7.setText("conso instantanée : -- ")
            else :                                
              consoinstantbyte= bytes([data[1],data[2]])
              consoinstantbyte2=''.join('%02X' % byte for byte in consoinstantbyte)                                               
              root.tripinfo7.setText("conso instantanée : %s " + str(float(int(consoinstantbyte2,16))/10))

            if (data[0] & 0b00001000) == 0b00001000 :
                # if Tripbutton pressed : switch window
                cmd = 'xdotool keydown  alt +Tab keyup alt+Tab'
                os.system(cmd)

        elif frame_id == TRIP_MODE_FRAME:
            #temp = int(format_data_hex(data))
            temp = data[0]
            tripInfoMode =""
            if temp == 0:
                tripInfoMode = "instant"
            elif temp == 1:
                tripInfoMode = "trip1"
            elif temp == 2:
                tripInfoMode = "trip2"
            #Maybe useless for my integration ?
            root.tripInfoMode.setText(tripInfoMode)

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
            audiosettings['equalizer']          = equalizerSetting
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
    reading_thread = None
    # Reading from a serial device, opened with timeout=0 (non-blocking read())
    source_handler.open()

    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    root = Ui()  # Create an instance of our class for the MainWindow

    # Creation du Thread pour la boucle de lecture, args : source_handler pour l'usb et root pour l'UI
    reading_thread = threading.Thread(target=reading_loop, args=(source_handler, root,))
    # Start the reading background thread              
    reading_thread.start()
    # Start the application              
    app.exec_() 


class Ui(QtWidgets.QMainWindow):
   def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('/home/pi/lucas/interface.ui', self)  # Load the .ui Mainwindow file
        # self.setStyleSheet(self.stylesheet)
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
      
        #Initialisation of the alert window
        self.init_alert_window()
        #Initialisation of the volume window
        self.Volumewindow=volumewindow()
         
         
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.Background, QColor(53, 53, 53))

        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
        self.setPalette(dark_palette)

         
        self.AlertONbutton.clicked.connect(self.show_alert)
        self.AlertOFFbutton.clicked.connect(self.hide_alert)
        self.closebutton.clicked.connect(self.close_all)                  
        self.showMaximized()  # Show the GUI

   
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
         #Each selectorelctor display go grey
         self.equalizernone.setStyleSheet("color: grey;")
         self.equalizerclassical.setStyleSheet("color: grey;")
         self.equalizerjazzBlues.setStyleSheet("color: grey;")
         self.equalizerpopRock.setStyleSheet("color: grey;")
         self.equalizertechno.setStyleSheet("color: grey;")
         self.equalizervocal.setStyleSheet("color: grey;")
         
   def close_all(self):
        # set flag of              
        if reading_thread:
            stop_reading.set()
            reading_thread.join()
        if source_handler:
            source_handler.close()

            # If the thread returned an exception, print it
        if thread_exception:
             #traceback.print_exception(*thread_exception)
             sys.stderr.flush()
                      
        logging.info("Fermeture de l'application")              
        #After closing threads, closing the window            
        self.close()              
                      
class Communicate(QObject):                                                 
    signal_int = Signal(int)

          
if __name__ == '__main__':
    run()
