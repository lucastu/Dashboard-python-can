#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

import sys
import threading
#import traceback
import time
import os

from source_handler import InvalidFrame, SerialHandler
from sound_level import volumewindow
from ombre import ombre
from alertMSG import alertmsg
from InfoMSG_parser import parseInfoMessage

#Display on the device display in case of SSH launch of the script
os.environ.__setitem__('DISPLAY', ':0.0')
# os.environ["QT_LOGGING_RULES"] = "qt5ct.debug=false"
stop_reading = threading.Event()

can_messages = {}
can_messages_lock = threading.Lock()

thread_exception = None

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

def isInfoMessage(data, b1 , b2, b3 ):
   # Compare the 3 firsts bytes of "data" with b1, b2 and b3, ommiting the first and the last quartet
    return (data[0] & 0b00001111) == b1 & (data[1] & 0b11111111) == b2 & (data[2] & 0b11110000) == (b3 & 0b11110000)

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
    SEATBELTS_FRAME =      0x0A
    AIRBAG_STATUS_FRAME =  0x0B
    INFO_TRIP1_FRAME =     0x0C
    INFO_TRIP2_FRAME =     0x0D
    INFO_INSTANT_FRAME =   0x0E
    TRIP_MODE_FRAME =      0x0F
    AUDIO_SETTINGS_FRAME = 0x10
    SECRET_FRAME =         0x42
    
    while not stop_reading.is_set():
        try:
            frame_id, data = source_handler.get_message()
        except InvalidFrame:
            continue
        except EOFError:
            break

        if frame_id == VOLUME_FRAME:
            temp = str(int(format_data_hex(data & 0b00011111),16))
            root.Volume.setText(temp)
            root.Volumewindow.progress.setValue(int(temp))   
            
            if not (data & 0b11100000 == 0b11100000)
                # ICI DECLENCHER LE CHANGEMENT DE VOLUME  
            else
                # ICI cacher le volume


        elif frame_id == TEMPERATURE_FRAME:
            temp = str(int(format_data_hex(data),16))
            root.Temperature.setText( temp + "°C")

        elif frame_id == RADIO_NAME_FRAME:
            root.RadioName.setText(format_data_ascii(data))

        elif frame_id == RADIO_FREQ_FRAME:
            temp = format_data_hex(data)
            root.RadioFreq.setText(str(float(int(temp.replace(" ", ""),16))/10)+ "MHz")

        elif frame_id == RADIO_FMTYPE_FRAME:
            temp = int(format_data_hex(data))
            RadioFMType ="No Type"
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
            temp = int(format_data_ascii(data))
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
            print("Radio desc frame data : %s  " % temp)
                  
        elif frame_id == INFO_MSG_FRAME:
            infomessage = parseInfoMessage(data, root)
            root.InfoMSG.setText(infomessage)
            
            #PARSER LE PREMIER 
            if not (data[0] & 0b01110000) :
               root.show_alert()
            else :
               root.hide_alert()
            #0x80 - show window
            #0x7F - hide window
            #0xFF - clear window (default)
            print("Radio desc frame data : %s; and type : %s  " % (format_data_ascii(data) , type(temp)))
                  
        elif frame_id == RADIO_STATIONS_FRAME:
            temp = format_data_hex(data)
            if '|' in temp:
                radio_list = temp.split("|")
                root.radioList0.setText("1 : "+ radio_list[0])
                root.radioList1.setText("2 : "+ radio_list[1])
                root.radioList2.setText("3 : "+ radio_list[2])
                root.radioList3.setText("4 : "+ radio_list[3])
                root.radioList4.setText("5 : "+ radio_list[4])
                root.radioList5.setText("6 : "+ radio_list[5])

                  
        elif frame_id == SEATBELTS_FRAME:
            # Est-ce que j'en fais quelque chose de cette info ??
            continue

        elif frame_id == AIRBAG_STATUS_FRAME:
            # Est-ce que j'en fais quelque chose de cette info ?? AIRBAG PASSAGER
            continue

        elif frame_id == INFO_TRIP1_FRAME :
            #tripInfo = format_data_ascii(data)  
            # print("INFO_TRIP1_FRAME data : %s; and type : %s  (non validÃƒÂ©)" % (tripInfo , type(tripInfo))  )
            root.tripinfo3.setText("averageSpeed 1 = %s " %(data[0])) 
            root.tripinfo1.setText("distance 1= %s %s " %(data[1], data[2]))
            
            averageFuelUsage=int(data[3]+data[4])/10
            print(data[3], data[4])
            print(averageFuelUsage)
            root.tripinfo2.setText("averageFuelUsage = %s " % averageFuelUsage)


           # info de trip, idem pour les deux, a voir comment je le traite..
           # tripInfo = TripInfo(   distance: Int(UInt16(highByte: data[1], lowByte: data[2])),
           #                        averageFuelUsage: data[3] == 0b11111111 ?-1 : Double(UInt16(highByte: data[3], lowByte: data[4])) / 10.0,
           #                        averageSpeed: data[0] == 0b11111111 ? -1 : Int(data[0]))
                  
        elif  frame_id == INFO_TRIP2_FRAME :
            #tripInfo = format_data_ascii(data)  
            #print("INFO_TRIP1_FRAME data : %s; and type : %s  (non validÃƒÂ©)" % (tripInfo , type(tripInfo))  
            root.tripinfo4.setText("distance 2= %s %s " %          (data[1], data[2]))
            root.tripinfo5.setText("averageFuelUsage 2= %s %s " %  (data[3], data[4]))
            root.tripinfo6.setText("averageSpeed 2 = %s " %         (data[0]))
            
        elif frame_id == INFO_INSTANT_FRAME :
            #tripInfo = format_data_ascii(data)  
            #print("Radio Stations frame data : %s; and type : %s  (non validÃƒÂ©)" % (tripInfo , type(tripInfo))  
            print("autonomy= %s %s " %(data[3], data[4]))
            print("fuelUsage= %s  " %(data[1]))
            # instantInfo = InstantInfo(autonomy: data[3] == 0b11111111 ? -1: Int(UInt16(highByte: data[3], lowByte: data[4])),
            #                           fuelUsage: data[1] == 0b11111111 ? 0: Double(UInt16(highByte: data[1], lowByte: data[2])) / 10.0)
            
        elif frame_id == TRIP_MODE_FRAME:
            temp = int(format_data_hex(data))
            tripInfoMode =""
            if temp == 0:
                tripInfoMode = "instant"
            elif temp == 1:
                tripInfoMode = "trip1"
            elif temp == 2:
                tripInfoMode = "trip2"
            #Maybe useless for my integraation ?      
            root.tripInfoMode.setText(tripInfoMode)

        elif frame_id == AUDIO_SETTINGS_FRAME:
            #activeMode = 0
            #equalizerSetting = 0             
                  
            #Active selected mode in audio settings      
            if (data[0] & 0b10000000) == 0b10000000 :
                activeMode = 1  # .leftRightBalance
            elif (data[1] & 0b10000000) == 0b10000000 :
                activeMode = 2  # .frontRearBalance
            elif (data[2] & 0b10000000) == 0b10000000 :
                activeMode = 3  # .bass
            elif (data[4] & 0b10000000) == 0b10000000 :
                activeMode = 4  # .treble
            elif (data[5] & 0b10000000) == 0b10000000 :
                activeMode = 5  # .loudness
            elif (data[5] & 0b00000001) == 0b00000001 :
                activeMode = 6  # .automaticVolume
            elif (data[6] & 0b00000100) == 0b00000100 :
                activeMode = 7  # .equalizer
            else :
                activeMode = 0

            #Valeur de l'equalizer Setting
            if (data[6] & 0b10111111) ==  0b00000011 :
                equalizerSetting = 0  # .none
            elif (data[6] & 0b10111111) ==  0b00000111 :
                equalizerSetting = 1  # .classical
            elif (data[6] & 0b10111111) == 0b00001011 :
                equalizerSetting = 2  # .jazzBlues
            elif (data[6] & 0b10111111) == 0b00001111 :
                equalizerSetting = 3  # .popRock
            elif (data[6] & 0b10111111) == 0b00010011 :
                equalizerSetting = 4  # .vocals
            elif (data[6] & 0b10111111) == 0b00010111 :
                equalizerSetting = 5  # .techno
                  
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
            print ("FRAME ID NON TRAITE : %s  :  %s  %s" % (frame_id, format_data_hex(data), format_data_ascii(data)))

                  
        # f there is an activeMode of audio settings, switch to the audiosettings tab 
        if audiosettings['activeMode'] != 0 :
            root.tabWidget.setCurrentIndex(1)
        else :
            root.tabWidget.setCurrentIndex(0)

def format_data_hex(data):
    """Convert the bytes array to an hex representation."""
    # Bytes are separated by spaces.
    return ' '.join('%02X' % byte for byte in data)


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
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
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

                      
   def close_all(self):
        # set flag of              
        if reading_thread:
            stop_reading.set()
            reading_thread.join()
        if source_handler:
            source_handler.close()

            # If the thread returned an exception, print it
        if thread_exception:
             traceback.print_exception(*thread_exception)
             sys.stderr.flush()
                      
        print("Fermeture de l'application")              
        #After closing threads, closing the window            
        self.close()              
                      

if __name__ == '__main__':
    run()
