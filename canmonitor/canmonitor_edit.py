#!/usr/bin/env python3
# -*- coding: ISO-8859-1 -*-
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

# Parametres de la lecture USB
baudrate = 115200
serial_device = "/dev/ttyUSB0"

def isInfoMessage(data, b1 , b2, b3 ):
    # Fonction qui compare les trois bytes du premier parametre avec les trois bytes des autres parametres en omettant le premier quartet et le dernier
    return (data[0] & 0x0F) == b1 & (data[1] & 0xFF) == b2 & (data[2] & 0xF0) == (b3 & 0xF0)

def reading_loop(source_handler, root):
    """Background thread for reading."""

    # Variables de l'ID des types de frames
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
    SEATBELTS_FRAME = 0x0A
    AIRBAG_STATUS_FRAME = 0x0B
    INFO_TRIP1_FRAME = 0x0C
    INFO_TRIP2_FRAME = 0x0D
    INFO_INSTANT_FRAME = 0x0E
    TRIP_MODE_FRAME = 0x0F
    AUDIO_SETTINGS_FRAME = 0x10
    SECRET_FRAME = 0x42

    try:
        while not stop_reading.is_set():
            try:
                frame_id, data = source_handler.get_message()
            except InvalidFrame:
                continue
            except EOFError:
                break

            # Add the frame to the can_messages dict and tell the main thread to refresh its content

            # root.RadioName.setText("placeholder")

            if frame_id == VOLUME_FRAME:
                continue
                # VOLUME = int(format_data_hex(data),16)
                # ICI DECLENCHER LE CHANGEMENT DE VOLUME

            elif frame_id == TEMPERATURE_FRAME:
                root.Temperature.setText(format_data_hex(data)+"°C")
                # root.Temperature.setText(string(int(format_data_hex(data), 16)))

            elif frame_id == RADIO_NAME_FRAME:
                root.RadioName.setText(format_data_ascii(data))

            elif frame_id == RADIO_FREQ_FRAME:
                root.RadioFreq.setText(format_data_ascii(data))

            elif frame_id == RADIO_FMTYPE_FRAME:
                temp = (format_data_hex(data))
                RadioFMType =0
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
                temp = format_data_hex(data)
                Source = 0
                if temp == 0x01:
                    Source = "Tuner"
                elif temp == 0x02:
                    Source = "cd"
                elif temp == 0x03:
                    Source = "CDC"
                elif temp == 0x04:
                    Source = "AUX1"
                elif temp == 0x05:
                    Source = "AUX2"
                elif temp == 0x06:
                    Source = "USB"
                elif temp == 0x07:
                    Source = "BLUETOOTH"

            elif frame_id == RADIO_DESC_FRAME:
                root.RadioDesc.setText(format_data_ascii(data))

            elif frame_id == INFO_MSG_FRAME:
                parseInfoMessage(data, root)
                # Alors la ya du taf !! on verra apres ;) Avec une fonction dediee !
                continue
            elif frame_id == RADIO_STATIONS_FRAME:
                # je ne sais pas encore comment ca marche ici ...
                continue
            elif frame_id == SEATBELTS_FRAME:
                # Est-ce que j'en fais quelque chose de cette info ??
                continue
            elif frame_id == AIRBAG_STATUS_FRAME:
                # Est-ce que j'en fais quelque chose de cette info ?? AIRBAG PASSAGER
                continue

            elif frame_id == INFO_TRIP1_FRAME or frame_id == INFO_TRIP2_FRAME:
            # info de trip, idem pour les deux, a voir comment je le traite..
            # tripInfo = TripInfo(distance: Int(UInt16(highByte: data[1], lowByte: data[2])),
            #                        averageFuelUsage: data[3] == 0xFF ?
            #                            -1 :
            #                            Double(UInt16(highByte: data[3], lowByte: data[4])) / 10.0,
            #                        averageSpeed: data[0] == 0xFF ? -1 : Int(data[0]))

            # if frameID == 0x0C
            #    tripInfo1 = tripInfo
            # else
            #    tripInfo2 = tripInfo
            #
                continue
            elif frame_id == INFO_INSTANT_FRAME:
                # instantInfo = InstantInfo(autonomy: data[3] == 0xFF ? -1: Int(UInt16(highByte: data[3], lowByte: data[4])),
                # fuelUsage: data[1] == 0xFF ? 0: Double(UInt16(highByte: data[1], lowByte: data[2])) / 10.0)
                continue

            elif frame_id == TRIP_MODE_FRAME:
                tripInfoMode =""
                if data[0] == 0:
                    tripInfoMode = "instant"
                elif data[0] == 1:
                    tripInfoMode = "trip1"
                elif data[0] == 2:
                    tripInfoMode = "trip2"
                root.tripInfoMode.setText(tripInfoMode)

            elif frame_id == AUDIO_SETTINGS_FRAME:
                # Si on a un mode actif, on bascule de tab
                activeMode = 0
                
                if (data[0] & 0x80) == 0x80 :
                    activeMode = 1  # .leftRightBalance
                elif (data[1] & 0x80) == 0x80 :
                    activeMode = 2  # .frontRearBalance
                elif (data[2] & 0x80) == 0x80 :
                    activeMode = 3  # .bass
                elif (data[4] & 0x80) == 0x80 :
                    activeMode = 4  # .treble
                elif (data[5] & 0x80) == 0x80 :
                    activeMode = 5  # .loudness
                elif (data[5] & 0x10) == 0x10 :
                    activeMode = 6  # .automaticVolume
                elif (data[6] & 0x40) == 0x40 :
                    activeMode = 7  # .equalizer

                equalizerSetting = 0
                if (data[6] & 0xBF) == 0x07 :
                    equalizerSetting = 1  # .classical
                elif (data[6] & 0xBF) == 0x0B :
                    equalizerSetting = 2  # .jazzBlues
                elif (data[6] & 0xBF) == 0x0F :
                    equalizerSetting = 3  # .popRock
                elif (data[6] & 0xBF) == 0x13 :
                    equalizerSetting = 4  # .vocals
                elif (data[6] & 0xBF) == 0x17 :
                    equalizerSetting = 5  # .techno


                # audioSettings = AudioSettings(activeMode: activeMode,
                #                             frontRearBalance: Int(data[1] & 0x7F) - 63,
                #                            leftRightBalance: Int(data[0] & 0x7F) - 63,
                #                           automaticVolume: (data[5] & 0x07) == 0x07,
                #                          equalizer: equalizerSetting,
                #                         bass: Int(data[2] & 0x7F) - 63,
                #                        treble: Int(data[4] & 0x7F) - 63,
                #                       loudness: (data[5] & 0x40) == 0x40)

                else:
                    print ("FRAME ID %s  :  %s  %s" % (frame_id, format_data_hex(data), format_data_ascii(data)))

                stop_reading.wait()

    except():
        if not stop_reading.is_set():
            # Only log exception if we were not going to stop the thread
            # When quitting, the main thread calls close() on the serial device
            # and read() may throw an exception. We don't want to display it as
            # we're stopping the script anyway
            global thread_exception
            thread_exception = sys.exc_info()


def parseInfoMessage(data, root):
    infomessage = "none"
    if isInfoMessage(data, 0x01, 0x2F, 0xC4):
        infomessage = "Essuie-vitre automatique activé"

    elif isInfoMessage(data, 0x01, 0x30, 0xC4):
        infomessage = "Essuie-vitre automatique désactivé"

    elif isInfoMessage(data, 0x01, 0x31, 0xC4):
        infomessage = "Allumage automatique des projecteurs activé"
    elif isInfoMessage(data, 0x01, 0x32, 0xC4):
        infomessage = "Allumage automatique des projecteurs désactivé"
    elif isInfoMessage(data, 0x01, 0x33, 0xC4):
        infomessage = "Auto-verrouillage des portes activé"
    elif isInfoMessage(data, 0x01, 0x34, 0xC4):
        infomessage = "Auto-verrouillage des portes déactivé"
    elif isInfoMessage(data, 0x01, 0x37, 0xC4):
        infomessage = "Sécurité enfant activée"
    elif isInfoMessage(data, 0x01, 0x38, 0xC4):
        infomessage = "Sécurité enfant désactivée"
    elif isInfoMessage(data, 0x01, 0x3D, 0xC4):
        infomessage = "Stationnement NON (cf photo)"
    elif isInfoMessage(data, 0x01, 0x98, 0xC4):
        infomessage = "Système STOP START défaillant"
    elif isInfoMessage(data, 0x01, 0xF6, 0xC4):
        infomessage = "Manoeuvre toit impossible: tº ext. trop faible"
    elif isInfoMessage(data, 0x01, 0xF7, 0xC4):
        infomessage = "Manoeuvre toit impossible: vitesse trop élevée"
    elif isInfoMessage(data, 0x01, 0xF8, 0xC4):
        infomessage = "Manoeuvre toit impossible: coffre ouvert"
    elif isInfoMessage(data, 0x01, 0xFA, 0xC4):
        infomessage = "Manoeuvre toit impossible: rideau coffre non déployé"
    elif isInfoMessage(data, 0x01, 0xFB, 0xC4):
        infomessage = "Manoeuvre toit terminée"
    elif isInfoMessage(data, 0x01, 0xFC, 0xC4):
        infomessage = "Terminer immédiatement la manoeuvre de toit"
    elif isInfoMessage(data, 0x01, 0xFD, 0xC4):
        infomessage = "Manoeuvre impossible: toit verrouillé"
    elif isInfoMessage(data, 0x01, 0xFE, 0xC4):
        infomessage = "Mécanisme toit escamotable défaillant"
    elif isInfoMessage(data, 0x01, 0xFF, 0xC4):
        infomessage = "Manoeuvre impossible: lunette ouverte"
    elif isInfoMessage(data, 0x00, 0x00, 0xC8):
        infomessage = "Diagnostic OK"
    elif isInfoMessage(data, 0x00, 0x01, 0xC8):
        infomessage = "STOP: défaut température moteur, arrêtez le véhicule"
    elif isInfoMessage(data, 0x00, 0x03, 0xC8):
        infomessage = "Ajustez niveau liquide de refroidissement"
    elif isInfoMessage(data, 0x00, 0x04, 0xC8):
        infomessage = "Ajustez le niveau d'huile moteur"
    elif isInfoMessage(data, 0x00, 0x05, 0xC8):
        infomessage = "STOP: défaut pression huile moteur, arrêtez le véhicule"
    elif isInfoMessage(data, 0x00, 0x08, 0xC8):
        infomessage = "STOP: système de freinage défaillant"
    elif isInfoMessage(data, 0x00, 0x0A, 0xC8):
        infomessage = "Demande non permise (cf photo)"
    elif isInfoMessage(data, 0x00, 0x0D, 0xC8):
        infomessage = "Plusieurs roues crevées"
    elif isInfoMessage(data, 0x00, 0x0F, 0xC8):
        infomessage = "Risque de colmatage filtre à particules: consultez la notice"
    elif isInfoMessage(data, 0x00, 0x11, 0xC8):
        infomessage = "Suspension défaillante, vitesse max 90km/h"
    elif isInfoMessage(data, 0x00, 0x12, 0xC8):
        infomessage = "Suspension défaillante"
    elif isInfoMessage(data, 0x00, 0x13, 0xC8):
        infomessage = "Direction assistée défaillante"
    elif isInfoMessage(data, 0x00, 0x14, 0xC8):
        infomessage = "WTF?"
    elif isInfoMessage(data, 0x00, 0x61, 0xC8):
        infomessage = "Frein de parking serré"
    elif isInfoMessage(data, 0x00, 0x62, 0xC8):
        infomessage = "Frein de parking desserré"
    elif isInfoMessage(data, 0x00, 0x64, 0xC8):
        infomessage = "Commande frein de parking défaillante, frein de parking auto activé"
    elif isInfoMessage(data, 0x00, 0x67, 0xC8):
        infomessage = "Plaquettes de frein usées"
    elif isInfoMessage(data, 0x00, 0x68, 0xC8):
        infomessage = "Frein de parking défaillant"
    elif isInfoMessage(data, 0x00, 0x69, 0xC8):
        infomessage = "Aileron mobile défaillant, vitesse limitée, consultez la notice"
    elif isInfoMessage(data, 0x00, 0x6A, 0xC8):
        infomessage = "Système de freinage ABS défaillant"
    elif isInfoMessage(data, 0x00, 0x6B, 0xC8):
        infomessage = "Système ESP/ASR défaillant"
    elif isInfoMessage(data, 0x00, 0x6C, 0xC8):
        infomessage = "Suspension défaillante"
    elif isInfoMessage(data, 0x00, 0x6D, 0xC8):
        infomessage = "STOP: direction assistée défaillante"
    elif isInfoMessage(data, 0x00, 0x6E, 0xC8):
        infomessage = "Défaut boite de vitesse, faites réparer le véhicule"
    elif isInfoMessage(data, 0x00, 0x6F, 0xC8):
        infomessage = "Système de controle de vitesse défaillant"
    elif isInfoMessage(data, 0x00, 0x73, 0xC8):
        infomessage = "Capteur de luminosité ambiante défaillant"
    elif isInfoMessage(data, 0x00, 0x74, 0xC8):
        infomessage = "Ampoule feu de position défaillante"
    elif isInfoMessage(data, 0x00, 0x75, 0xC8):
        infomessage = "Réglage automatique des projecteurs défaillant"
    elif isInfoMessage(data, 0x00, 0x76, 0xC8):
        infomessage = "Projecteurs directionnels défaillants"
    elif isInfoMessage(data, 0x00, 0x78, 0xC8):
        infomessage = "Airbag(s) ou ceinture(s) à prétensionneur(s) défaillant(s)"
    elif isInfoMessage(data, 0x00, 0x7A, 0xC8):
        infomessage = "Défaut boite de vitesse, faites réparer le véhicule"
    elif isInfoMessage(data, 0x00, 0x7B, 0xC8):
        infomessage = "Pied sur frein et levier en position \"N\" nécessaires"
    elif isInfoMessage(data, 0x00, 0x7D, 0xC8):
        infomessage = "Présence d'eau dans le filtre à gasoil, faites réparer le véhicule"
    elif isInfoMessage(data, 0x00, 0x7E, 0xC8):
        infomessage = "Défaut moteur, faites réparer le véhicule"
    elif isInfoMessage(data, 0x00, 0x7F, 0xC8):
        infomessage = "Défaut moteur, faites réparer le véhicule"
    elif isInfoMessage(data, 0x00, 0x81, 0xC8):
        infomessage = "Niveau additif FAP trop faible, faites réparer le véhicule"
    elif isInfoMessage(data, 0x00, 0x83, 0xC8):
        infomessage = "Antivol électronique défaillant"
    elif isInfoMessage(data, 0x00, 0x88, 0xC8):
        infomessage = "Système aide au stationnement défaillant"
    elif isInfoMessage(data, 0x00, 0x89, 0xC8):
        infomessage = "Système de mesure de place défaillant"
    elif isInfoMessage(data, 0x00, 0x8A, 0xC8):
        infomessage = "Charge batterie ou alimentation électrique défaillante"
    elif isInfoMessage(data, 0x00, 0x8D, 0xC8):
        infomessage = "Pression pneumatiques insuffisante"
    elif isInfoMessage(data, 0x00, 0x97, 0xC8):
        infomessage = "Système d'alerte de franchissement de ligne défaillant"
    elif isInfoMessage(data, 0x00, 0x9A, 0xC8):
        infomessage = "Ampoule feu de croisement défaillante"
    elif isInfoMessage(data, 0x00, 0x9B, 0xC8):
        infomessage = "Ampoule feu de route défaillante"
    elif isInfoMessage(data, 0x00, 0x9C, 0xC8):
        infomessage = "Ampoule feu stop défaillante"
    elif isInfoMessage(data, 0x00, 0x9D, 0xC8):
        infomessage = "Ampoule anti-brouillard défaillante"
    elif isInfoMessage(data, 0x00, 0x9E, 0xC8):
        infomessage = "Clignotant défaillant"
    elif isInfoMessage(data, 0x00, 0x9F, 0xC8):
        infomessage = "Ampoule feu de recul défaillante"
    elif isInfoMessage(data, 0x00, 0xA0, 0xC8):
        infomessage = "Ampoule feu de position défaillante"
    elif isInfoMessage(data, 0x00, 0xCD, 0xC8):
        infomessage = "Régulation de vitesse impossible: vitesse trop faible"
    elif isInfoMessage(data, 0x00, 0xCE, 0xC8):
        infomessage = "Activation du régulateur impossible: saisir la vitesse"
    elif isInfoMessage(data, 0x00, 0xD2, 0xC8):
        infomessage = "Ceintures AV non bouclées"
    elif isInfoMessage(data, 0x00, 0xD3, 0xC8):
        infomessage = "Ceintures passagers AR bouclées"
    elif isInfoMessage(data, 0x00, 0xD7, 0xC8):
        infomessage = "Placer boite automatique en position P"
    elif isInfoMessage(data, 0x00, 0xD8, 0xC8):
        infomessage = "Risque de verglas"
    elif isInfoMessage(data, 0x00, 0xD9, 0xC8):
        infomessage = "Oubli frein à main !"
    elif isInfoMessage(data, 0x00, 0xDE, 0xC8) or isInfoMessage(data, 0x00, 0x0B, 0xC8):
    # Car doors frame
        doorByte1 = data[3]
        doorByte2 = data[4]
    
        if doorByte1 & 0x04 == 0x04:
            # decodedCarDoors.insert(.Hood)
            print("Capot ouvert")
        if doorByte1 & 0x08 == 0x08:
            # decodedCarDoors.insert(.Trunk)
            print("Coffre ouvert")
        if doorByte1 & 0x10 == 0x10:
            # decodedCarDoors.insert(.RearLeft)
            print("porte arrière gauche ouverte")
        if doorByte1 & 0x20 == 0x20:
            # decodedCarDoors.insert(.RearRight)
            print("porte arrière droite ouverte")
        if doorByte1 & 0x40 == 0x40:
            # decodedCarDoors.insert(.FrontLeft)
            print("porte conducteur ouverte")
        if doorByte1 & 0x80 == 0x80:
            # decodedCarDoors.insert(.FrontRight)
            print("porte passager ouverte")
        if doorByte2 & 0x40 == 0x40:
            # decodedCarDoors.insert(.FuelFlap)
            print("trappe essence ouverte")

    elif isInfoMessage(data, 0x00, 0xDF, 0xC8):
        infomessage = "Niveau liquide lave-glace insuffisant"
    elif isInfoMessage(data, 0x00, 0xE0, 0xC8):
        infomessage = "Niveau carburant faible"
    elif isInfoMessage(data, 0x00, 0xE1, 0xC8):
        infomessage = "Circuit de carburant neutralisé"
    elif isInfoMessage(data, 0x00, 0xE3, 0xC8):
        infomessage = "Pile télécommande plip usagée"
    elif isInfoMessage(data, 0x00, 0xE5, 0xC8):
        infomessage = "Pression pneumatique(s) non surveillée"
    elif isInfoMessage(data, 0x00, 0xE7, 0xC8):
        infomessage = "Vitesse élevée, vérifier si pression pneumatiques adaptée"
    elif isInfoMessage(data, 0x00, 0xE8, 0xC8):
        infomessage = "Pression pneumatique(s) insuffisante"
    elif isInfoMessage(data, 0x00, 0xEB, 0xC8):
        infomessage = "La phase de démarrage a échoué (consulter la notice)"
    elif isInfoMessage(data, 0x00, 0xEC, 0xC8):
        infomessage = "Démarrage prolongé en cours"
    elif isInfoMessage(data, 0x00, 0xEF, 0xC8):
        infomessage = "Télécommande non détectée"
    elif isInfoMessage(data, 0x00, 0xF0, 0xC8):
        infomessage = "Diagnostic en cours"
    elif isInfoMessage(data, 0x00, 0xF1, 0xC8):
        infomessage = "Diagnostic terminé"
    elif isInfoMessage(data, 0x00, 0xF7, 0xC8):
        infomessage = "Ceinture passager AR gauche débouclée"
    elif isInfoMessage(data, 0x00, 0xF8, 0xC8):
        infomessage = "Ceinture passager AR central débouclée"
    elif isInfoMessage(data, 0x00, 0xF9, 0xC8):
        infomessage = "Ceinture passager AR droit débouclée"
    else:
        infomessage = "empty"
    root.InfoMSG.setText(infomessage)


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

        # Création du Thread pour la boucle de lecture, args : source_handler pour l'usb et root pour l'UI
        reading_thread = threading.Thread(target=reading_loop, args=(source_handler, root,))
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
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('/home/pi/lucas/interface.ui', self)  # Load the .ui file

        self.showMaximized()  # Show the GUI

    def mousePressEvent(self, event):
        self.close()

if __name__ == '__main__':
    run()
