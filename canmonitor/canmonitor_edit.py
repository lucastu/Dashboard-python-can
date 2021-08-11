#!/usr/bin/env python3

from PyQt5 import QtWidgets, uic

import sys
import threading
import traceback
import time
import os
from source_handler import InvalidFrame, SerialHandler
os.environ.__setitem__('DISPLAY', ':0.0')

stop_reading = threading.Event()

can_messages = {}
can_messages_lock = threading.Lock()

thread_exception = None

#Variables de l'ID des types de frames
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
SEATBELTS_FRAME      = 0x0A
AIRBAG_STATUS_FRAME  = 0x0B
INFO_TRIP1_FRAME     = 0x0C
INFO_TRIP2_FRAME     = 0x0D
INFO_INSTANT_FRAME   = 0x0E
TRIP_MODE_FRAME      = 0x0F
AUDIO_SETTINGS_FRAME = 0x10
SECRET_FRAME         = 0x42 

#Paramètres de la lecture USB
baudrate = 115200
serial_device = "/dev/ttyUSB0"

def reading_loop(source_handler, root):
    """Background thread for reading."""
    try:
        while not stop_reading.is_set():
            try:
                frame_id, data = source_handler.get_message()
            except InvalidFrame:
                continue
            except EOFError:
                break

            # Add the frame to the can_messages dict and tell the main thread to refresh its content
            with can_messages_lock:
                #root.RadioName.setText("placeholder")
                can_messages[frame_id] = data

                if frame_id == VOLUME_FRAME :
                    True
                    #VOLUME = int(format_data_hex(data),16)
                    #ICI DECLENCHER LE CHANGEMENT DE VOLUME
                    
                elif frame_id == TEMPERATURE_FRAME :
                   # root.Temperature.setText(format_data_hex(data))
                    root.Temperature.setText(int(format_data_hex(data),16))
                    
                elif frame_id == RADIO_NAME_FRAME :
                    root.RadioName.setText(format_data_ascii(data))
                    
                elif frame_id == RADIO_FREQ_FRAME :
                    root.RadioFreq.setText(format_data_ascii(data))  
                    
                elif frame_id == RADIO_FMTYPE_FRAME :
                    temp = (format_data_hex(data))  
                    if temp == 1 : 
                        root.RadioFMType.setText("FM1")
                    elif temp == 2 : 
                        root.RadioFMType.setText("FM2")   
                    elif temp == 4 : 
                        root.RadioFMType.setText("FMAST")                          
                    elif temp == 5 : 
                        root.RadioFMType.setText("AM")    

                elif frame_id == RADIO_SOURCE_FRAME :
                    temp = format_data_hex(data)
                    if temp == 0x01 : 
                        Source = "Tuner"
                    elif temp == 0x02 : 
                        Source =  "cd"                       
                    elif temp == 0x03 : 
                        Source = "CDC"
                    elif temp == 0x04 : 
                        Source = "AUX1"                        
                    elif temp == 0x05 : 
                        Source = "AUX2"   
                    elif temp == 0x06 : 
                        Source = "USB"   
                    elif temp == 0x07 : 
                        Source = "BLUETOOTH"   
                    
                elif frame_id == RADIO_DESC_FRAME :
                    root.RadioDesc.setText(format_data_ascii(data))                    

                elif frame_id == INFO_MSG_FRAME :
                    #parseInfoMessage(data)
                    #Alors là ya du taf !! on verra après ;)
                    continue
                elif frame_id == RADIO_STATION_FRAME :     
                    #JE ne sais pas encore comment ça marche ici ...
                    continue                    
                elif frame_id == SEATBELTS_FRAME :     
                    #Est-ce que j'en fais quelque chose de cette info ??
                    continue                    
                elif frame_id == AIRBAG_STATUS_FRAME   :     
                    #Est-ce que j'en fais quelque chose de cette info ?? AIRBAG PASSAGER
                    continue           
                    
                elif frame_id == INFO_TRIP1_FRAME  or frame_id == INFO_TRIP2_FRAME :
                    #info de trip, idem pour les deux, à voir comment je le traite..
                    #tripInfo = TripInfo(distance: Int(UInt16(highByte: data[1], lowByte: data[2])),
                    #                        averageFuelUsage: data[3] == 0xFF ?
                    #                            -1 :
                    #                            Double(UInt16(highByte: data[3], lowByte: data[4])) / 10.0,
                    #                        averageSpeed: data[0] == 0xFF ? -1 : Int(data[0]))

                    #if frameID == 0x0C 
                    #    tripInfo1 = tripInfo
                    #else 
                    #    tripInfo2 = tripInfo
                    #                   
                    
                elif frame_id == INFO_INSTANT_FRAME      :     
                    instantInfo = InstantInfo(autonomy: data[3] == 0xFF ? -1 : Int(UInt16(highByte: data[3], lowByte: data[4])),
                                               fuelUsage: data[1] == 0xFF ? 0 : Double(UInt16(highByte: data[1], lowByte: data[2])) / 10.0)
                    
                elif frame_id == TRIP_MODE_FRAME :     
                    if data[0] == 0 :
                        tripInfoMode = "instant"
                    elif data[] ==1 :
                        tripInfoMode = "trip1"
                    elif data[0] ==2 :
                        tripInfoMode = "trip2"
                     default:
                        print("Unknown trip mode \(data[0])")
                        
                elif frame_id == AUDIO_SETTINGS_FRAME : 
                    
                    #Si on a un mode actif, on bascule de tab
                    int activeMode = 0
                    if (data[0] & 0x80) == 0x80 
                        activeMode = 1 #.leftRightBalance
                    elif (data[1] & 0x80) == 0x80 
                        activeMode = 2 #.frontRearBalance
                    elif (data[2] & 0x80) == 0x80 
                        activeMode = 3 #.bass
                    elif (data[4] & 0x80) == 0x80 
                        activeMode = 4 #.treble
                    elif (data[5] & 0x80) == 0x80 
                        activeMode = 5 #.loudness
                    elif (data[5] & 0x10) == 0x10 
                        activeMode = 6 #.automaticVolume
                    elif (data[6] & 0x40) == 0x40 
                        activeMode = 7 #.equalizer
                    

                    int equalizerSetting = 0
                    switch data[6] & 0xBF { // exclude the "active mode" bit
                    if (data[6] & 0xBF)== 0x07:
                        equalizerSetting = 1 #.classical
                    elif (data[6] & 0xBF)== 0x0B:
                        equalizerSetting = 2 #.jazzBlues
                    elif (data[6] & 0xBF)==  0x0F:
                        equalizerSetting = 3 #.popRock
                    elif (data[6] & 0xBF)==  0x13:
                        equalizerSetting = 4 #.vocals
                    elif (data[6] & 0xBF)==  0x17:
                        equalizerSetting = 5 #.techno
                    }

                    audioSettings = AudioSettings(activeMode: activeMode,
                                                  frontRearBalance: Int(data[1] & 0x7F) - 63,
                                                  leftRightBalance: Int(data[0] & 0x7F) - 63,
                                                  automaticVolume: (data[5] & 0x07) == 0x07,
                                                  equalizer: equalizerSetting,
                                                  bass: Int(data[2] & 0x7F) - 63,
                                                  treble: Int(data[4] & 0x7F) - 63,
                                                  loudness: (data[5] & 0x40) == 0x40)
                    
                else :    
                    print ("FRAME ID %s  :  %s  %s"   % (frame_id, format_data_hex(data),format_data_ascii(data)))
        stop_reading.wait()

    except:
        if not stop_reading.is_set():
            # Only log exception if we were not going to stop the thread
            # When quitting, the main thread calls close() on the serial device
            # and read() may throw an exception. We don't want to display it as
            # we're stopping the script anyway
            global thread_exception
            thread_exception = sys.exc_info()

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


def parse_ints(string_list):
    int_set = set()
    for line in string_list:
        try:
            int_set.add(int(line, 0))
        except ValueError:
            continue
    return int_set


def run():
    source_handler = SerialHandler(serial_device, baudrate)
    reading_thread = None

    try:
        # If reading from a serial device, it will be opened with timeout=0 (non-blocking read())
        source_handler.open()

        # Start the reading background thread


        app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
        root = Ui()  # Create an instance of our class
        
        #Création du Thread pour la boucle de lecture, args : source_handler pour l'usb et root pour l'UI
        reading_thread = threading.Thread(target=reading_loop, args=(source_handler,root,))
        reading_thread.start()
        app.exec_()  # Start the application

    finally:
        # Cleanly stop reading thread before exiting
        if reading_thread:
            stop_reading.set()

            if source_handler:
                source_handler.close()

            reading_thread.join()

            # If the thread returned an exception, print it
            if thread_exception:
                traceback.print_exception(*thread_exception)
                sys.stderr.flush()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('/home/pi/lucas/interface.ui', self) # Load the .ui file
        self.show() # Show the GUI

if __name__ == '__main__':
    run()
