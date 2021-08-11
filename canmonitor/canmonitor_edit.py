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

can_messages = :}
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
                    parseInfoMessage(data)
                    #Alors là ya du taf !! on verra après ;) Avec une fonction dédiée ! 
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
                    elif data[0] ==1 :
                        tripInfoMode = "trip1"
                    elif data[0] ==2 :
                        tripInfoMode = "trip2"
                        
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

                    #audioSettings = AudioSettings(activeMode: activeMode,
                     #                             frontRearBalance: Int(data[1] & 0x7F) - 63,
                      #                            leftRightBalance: Int(data[0] & 0x7F) - 63,
                       #                           automaticVolume: (data[5] & 0x07) == 0x07,
                        #                          equalizer: equalizerSetting,
                         #                         bass: Int(data[2] & 0x7F) - 63,
                          #                        treble: Int(data[4] & 0x7F) - 63,
                           #                       loudness: (data[5] & 0x40) == 0x40)
                    
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
            
def parseInfoMessage(data) :
        if isInfoMessage(data, b1: 0x01, b2: 0x2F, b3: 0xC4) :
            infoMessage = "Essuie-vitre automatique activé"
        elif isInfoMessage(data, b1: 0x01, b2: 0x30, b3: 0xC4) :
            infoMessage = "Essuie-vitre automatique désactivé"
        elif isInfoMessage(data, b1: 0x01, b2: 0x31, b3: 0xC4) :
            infoMessage = "Allumage automatique des projecteurs activé"
        elif isInfoMessage(data, b1: 0x01, b2: 0x32, b3: 0xC4) :
            infoMessage = "Allumage automatique des projecteurs désactivé"
        elif isInfoMessage(data, b1: 0x01, b2: 0x33, b3: 0xC4) :
            infoMessage = "Auto-verrouillage des portes activé"
        elif isInfoMessage(data, b1: 0x01, b2: 0x34, b3: 0xC4) :
            infoMessage = "Auto-verrouillage des portes déactivé"
        elif isInfoMessage(data, b1: 0x01, b2: 0x37, b3: 0xC4) :
            infoMessage = "Sécurité enfant activée"
        elif isInfoMessage(data, b1: 0x01, b2: 0x38, b3: 0xC4) :
            infoMessage = "Sécurité enfant désactivée"
        elif isInfoMessage(data, b1: 0x01, b2: 0x3D, b3: 0xC4) :
            infoMessage = "Stationnement NON (cf photo)"
        elif isInfoMessage(data, b1: 0x01, b2: 0x98, b3: 0xC4) :
            infoMessage = "Système STOP START défaillant"
        elif isInfoMessage(data, b1: 0x01, b2: 0xF6, b3: 0xC4) :
            infoMessage = "Manoeuvre toit impossible: tº ext. trop faible"
        elif isInfoMessage(data, b1: 0x01, b2: 0xF7, b3: 0xC4) :
            infoMessage = "Manoeuvre toit impossible: vitesse trop élevée"
        elif isInfoMessage(data, b1: 0x01, b2: 0xF8, b3: 0xC4) :
            infoMessage = "Manoeuvre toit impossible: coffre ouvert"
        elif isInfoMessage(data, b1: 0x01, b2: 0xFA, b3: 0xC4) :
            infoMessage = "Manoeuvre toit impossible: rideau coffre non déployé"
        elif isInfoMessage(data, b1: 0x01, b2: 0xFB, b3: 0xC4) :
            infoMessage = "Manoeuvre toit terminée"
        elif isInfoMessage(data, b1: 0x01, b2: 0xFC, b3: 0xC4) :
            infoMessage = "Terminer immédiatement la manoeuvre de toit"
        elif isInfoMessage(data, b1: 0x01, b2: 0xFD, b3: 0xC4) :
            infoMessage = "Manoeuvre impossible: toit verrouillé"
        elif isInfoMessage(data, b1: 0x01, b2: 0xFE, b3: 0xC4) :
            infoMessage = "Mécanisme toit escamotable défaillant"
        elif isInfoMessage(data, b1: 0x01, b2: 0xFF, b3: 0xC4) :
            infoMessage = "Manoeuvre impossible: lunette ouverte"
        elif isInfoMessage(data, b1: 0x00, b2: 0x00, b3: 0xC8) :
            infoMessage = "Diagnostic OK"
        elif isInfoMessage(data, b1: 0x00, b2: 0x01, b3: 0xC8) :
            infoMessage = "STOP: défaut température moteur, arrêtez le véhicule"
        elif isInfoMessage(data, b1: 0x00, b2: 0x03, b3: 0xC8) :
            infoMessage = "Ajustez niveau liquide de refroidissement"
        elif isInfoMessage(data, b1: 0x00, b2: 0x04, b3: 0xC8) :
            infoMessage = "Ajustez le niveau d'huile moteur"
        elif isInfoMessage(data, b1: 0x00, b2: 0x05, b3: 0xC8) :
            infoMessage = "STOP: défaut pression huile moteur, arrêtez le véhicule"
        elif isInfoMessage(data, b1: 0x00, b2: 0x08, b3: 0xC8) :
            infoMessage = "STOP: système de freinage défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x0A, b3: 0xC8) :
            infoMessage = "Demande non permise (cf photo)"
        elif isInfoMessage(data, b1: 0x00, b2: 0x0D, b3: 0xC8) :
            infoMessage = "Plusieurs roues crevées"
        elif isInfoMessage(data, b1: 0x00, b2: 0x0F, b3: 0xC8) :
            infoMessage = "Risque de colmatage filtre à particules: consultez la notice"
        elif isInfoMessage(data, b1: 0x00, b2: 0x11, b3: 0xC8) :
            infoMessage = "Suspension défaillante, vitesse max 90km/h"
        elif isInfoMessage(data, b1: 0x00, b2: 0x12, b3: 0xC8) :
            infoMessage = "Suspension défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x13, b3: 0xC8) :
            infoMessage = "Direction assistée défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x14, b3: 0xC8) :
            infoMessage = "WTF?"
        elif isInfoMessage(data, b1: 0x00, b2: 0x61, b3: 0xC8) :
            infoMessage = "Frein de parking serré"
        elif isInfoMessage(data, b1: 0x00, b2: 0x62, b3: 0xC8) :
            infoMessage = "Frein de parking desserré"
        elif isInfoMessage(data, b1: 0x00, b2: 0x64, b3: 0xC8) :
            infoMessage = "Commande frein de parking défaillante, frein de parking auto activé"
        elif isInfoMessage(data, b1: 0x00, b2: 0x67, b3: 0xC8) :
            infoMessage = "Plaquettes de frein usées"
        elif isInfoMessage(data, b1: 0x00, b2: 0x68, b3: 0xC8) :
            infoMessage = "Frein de parking défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x69, b3: 0xC8) :
            infoMessage = "Aileron mobile défaillant, vitesse limitée, consultez la notice"
        elif isInfoMessage(data, b1: 0x00, b2: 0x6A, b3: 0xC8) :
            infoMessage = "Système de freinage ABS défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x6B, b3: 0xC8) :
            infoMessage = "Système ESP/ASR défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x6C, b3: 0xC8) :
            infoMessage = "Suspension défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x6D, b3: 0xC8) :
            infoMessage = "STOP: direction assistée défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x6E, b3: 0xC8) :
            infoMessage = "Défaut boite de vitesse, faites réparer le véhicule"
        elif isInfoMessage(data, b1: 0x00, b2: 0x6F, b3: 0xC8) :
            infoMessage = "Système de controle de vitesse défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x73, b3: 0xC8) :
            infoMessage = "Capteur de luminosité ambiante défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x74, b3: 0xC8) :
            infoMessage = "Ampoule feu de position défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x75, b3: 0xC8) :
            infoMessage = "Réglage automatique des projecteurs défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x76, b3: 0xC8) :
            infoMessage = "Projecteurs directionnels défaillants"
        elif isInfoMessage(data, b1: 0x00, b2: 0x78, b3: 0xC8) :
            infoMessage = "Airbag(s) ou ceinture(s) à prétensionneur(s) défaillant(s)"
        elif isInfoMessage(data, b1: 0x00, b2: 0x7A, b3: 0xC8) :
            infoMessage = "Défaut boite de vitesse, faites réparer le véhicule"
        elif isInfoMessage(data, b1: 0x00, b2: 0x7B, b3: 0xC8) :
            infoMessage = "Pied sur frein et levier en position \"N\" nécessaires"
        elif isInfoMessage(data, b1: 0x00, b2: 0x7D, b3: 0xC8) :
            infoMessage = "Présence d'eau dans le filtre à gasoil, faites réparer le véhicule"
        elif isInfoMessage(data, b1: 0x00, b2: 0x7E, b3: 0xC8) :
            infoMessage = "Défaut moteur, faites réparer le véhicule"
        elif isInfoMessage(data, b1: 0x00, b2: 0x7F, b3: 0xC8) :
            infoMessage = "Défaut moteur, faites réparer le véhicule"
        elif isInfoMessage(data, b1: 0x00, b2: 0x81, b3: 0xC8) :
            infoMessage = "Niveau additif FAP trop faible, faites réparer le véhicule"
        elif isInfoMessage(data, b1: 0x00, b2: 0x83, b3: 0xC8) :
            infoMessage = "Antivol électronique défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x88, b3: 0xC8) :
            infoMessage = "Système aide au stationnement défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x89, b3: 0xC8) :
            infoMessage = "Système de mesure de place défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x8A, b3: 0xC8) :
            infoMessage = "Charge batterie ou alimentation électrique défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x8D, b3: 0xC8) :
            infoMessage = "Pression pneumatiques insuffisante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x97, b3: 0xC8) :
            infoMessage = "Système d'alerte de franchissement de ligne défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x9A, b3: 0xC8) :
            infoMessage = "Ampoule feu de croisement défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x9B, b3: 0xC8) :
            infoMessage = "Ampoule feu de route défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x9C, b3: 0xC8) :
            infoMessage = "Ampoule feu stop défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x9D, b3: 0xC8) :
            infoMessage = "Ampoule anti-brouillard défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0x9E, b3: 0xC8) :
            infoMessage = "Clignotant défaillant"
        elif isInfoMessage(data, b1: 0x00, b2: 0x9F, b3: 0xC8) :
            infoMessage = "Ampoule feu de recul défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0xA0, b3: 0xC8) :
            infoMessage = "Ampoule feu de position défaillante"
        elif isInfoMessage(data, b1: 0x00, b2: 0xCD, b3: 0xC8) :
            infoMessage = "Régulation de vitesse impossible: vitesse trop faible"
        elif isInfoMessage(data, b1: 0x00, b2: 0xCE, b3: 0xC8) :
            infoMessage = "Activation du régulateur impossible: saisir la vitesse"
        elif isInfoMessage(data, b1: 0x00, b2: 0xD2, b3: 0xC8) :
            infoMessage = "Ceintures AV non bouclées"
        elif isInfoMessage(data, b1: 0x00, b2: 0xD3, b3: 0xC8) :
            infoMessage = "Ceintures passagers AR bouclées"
        elif isInfoMessage(data, b1: 0x00, b2: 0xD7, b3: 0xC8) :
            infoMessage = "Placer boite automatique en position P"
        elif isInfoMessage(data, b1: 0x00, b2: 0xD8, b3: 0xC8) :
            infoMessage = "Risque de verglas"
        elif isInfoMessage(data, b1: 0x00, b2: 0xD9, b3: 0xC8) :
            infoMessage = "Oubli frein à main !"
        elif isInfoMessage(data, b1: 0x00, b2: 0xDE, b3: 0xC8) || isInfoMessage(data, b1: 0x00, b2: 0x0B, b3: 0xC8) :
            # Car doors frame
            decodedCarDoors = 1

            let doorByte1 = data[3]
            let doorByte2 = data[4]

            if doorByte1 & 0x04 == 0x04 :
                decodedCarDoors.insert(.Hood)

            if doorByte1 & 0x08 == 0x08 :
                decodedCarDoors.insert(.Trunk)

            if doorByte1 & 0x10 == 0x10 :
                decodedCarDoors.insert(.RearLeft)

            if doorByte1 & 0x20 == 0x20 :
                decodedCarDoors.insert(.RearRight)

            if doorByte1 & 0x40 == 0x40 :
                decodedCarDoors.insert(.FrontLeft)

            if doorByte1 & 0x80 == 0x80 :
                decodedCarDoors.insert(.FrontRight)

            if doorByte2 & 0x40 == 0x40 :
                decodedCarDoors.insert(.FuelFlap)
                
            carDoors = decodedCarDoors
        elif isInfoMessage(data, b1: 0x00, b2: 0xDF, b3: 0xC8) :
            infoMessage = "Niveau liquide lave-glace insuffisant"
        elif isInfoMessage(data, b1: 0x00, b2: 0xE0, b3: 0xC8) :
            infoMessage = "Niveau carburant faible"
        elif isInfoMessage(data, b1: 0x00, b2: 0xE1, b3: 0xC8) :
            infoMessage = "Circuit de carburant neutralisé"
        elif isInfoMessage(data, b1: 0x00, b2: 0xE3, b3: 0xC8) :
            infoMessage = "Pile télécommande plip usagée"
        elif isInfoMessage(data, b1: 0x00, b2: 0xE5, b3: 0xC8) :
            infoMessage = "Pression pneumatique(s) non surveillée"
        elif isInfoMessage(data, b1: 0x00, b2: 0xE7, b3: 0xC8) :
            infoMessage = "Vitesse élevée, vérifier si pression pneumatiques adaptée"
        elif isInfoMessage(data, b1: 0x00, b2: 0xE8, b3: 0xC8) :
            infoMessage = "Pression pneumatique(s) insuffisante"
        elif isInfoMessage(data, b1: 0x00, b2: 0xEB, b3: 0xC8) :
            infoMessage = "La phase de démarrage a échoué (consulter la notice)"
        elif isInfoMessage(data, b1: 0x00, b2: 0xEC, b3: 0xC8) :
            infoMessage = "Démarrage prolongé en cours"
        elif isInfoMessage(data, b1: 0x00, b2: 0xEF, b3: 0xC8) :
            infoMessage = "Télécommande non détectée"
        elif isInfoMessage(data, b1: 0x00, b2: 0xF0, b3: 0xC8) :
            infoMessage = "Diagnostic en cours"
        elif isInfoMessage(data, b1: 0x00, b2: 0xF1, b3: 0xC8) :
            infoMessage = "Diagnostic terminé"
        elif isInfoMessage(data, b1: 0x00, b2: 0xF7, b3: 0xC8) :
            infoMessage = "Ceinture passager AR gauche débouclée"
        elif isInfoMessage(data, b1: 0x00, b2: 0xF8, b3: 0xC8) :
            infoMessage = "Ceinture passager AR central débouclée"
        elif isInfoMessage(data, b1: 0x00, b2: 0xF9, b3: 0xC8) :
            infoMessage = "Ceinture passager AR droit débouclée"
        else :
            carDoors = .None
            infoMessage = nil
        
            
            
            
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


def isInfoMessage(data, byte b1, byte b2,  byte b3) :
#Fonction qui compare les trois bytes du premier paramètre avec les trois bytes des autres paramètres en omettant le premier quartet et le dernier
    return ((data[0] & 0x0F) == b1 && (data[1] & 0xFF) == b2 && (data[2] & 0xF0) == (b3 & 0xF0))


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
