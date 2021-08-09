#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# lsusb to check device name
# dmesg | grep "tty" to find port name
import serial, time, sys
from tinydb import TinyDB, Query
from typing import Any

db = TinyDB('/home/pi/lucas/db.json')
import threading
import tkinter as tk
root = tk.Tk()
root.geometry("400x500")

VOLUME_FRAME_DATA = tk.StringVar(root, '1')
TEMPERATURE_FRAME_DATA = tk.StringVar(root, '2')
RADIO_SOURCE_FRAME_DATA = tk.StringVar(root, '3')
RADIO_NAME_FRAME_DATA = tk.StringVar(root, '4')
RADIO_FREQ_FRAME_DATA = tk.StringVar(root, '5')
RADIO_FMTYPE_FRAME_DATA = tk.StringVar(root, '6')
RADIO_DESC_FRAME_DATA = tk.StringVar(root, '7')
INFO_MSG_FRAME_DATA = tk.StringVar(root, '8')
RADIO_STATIONS_FRAME_DATA = tk.StringVar(root, '9')
SEATBELTS_FRAME_DATA = tk.StringVar(root, '10')
AIRBAG_STATUS_FRAME_DATA = tk.StringVar(root, '11')
INFO_TRIP1_FRAME_DATA = tk.StringVar(root, '12')
INFO_TRIP2_FRAME_DATA = tk.StringVar(root, '13')
INFO_INSTANT_FRAME_DATA = tk.StringVar(root, '14')
TRIP_MODE_FRAME_DATA = tk.StringVar(root, '15')
AUDIO_SETTINGS_FRAME_DATA = tk.StringVar(root, '16')
SECRET_FRAME_DATA = tk.StringVar(root, '17')


INIT_STATUS_FRAME    = 0
VOLUME_FRAME         = 1
TEMPERATURE_FRAME    = 2
RADIO_SOURCE_FRAME   = 3
RADIO_NAME_FRAME     = 4
RADIO_FREQ_FRAME     = 5
RADIO_FMTYPE_FRAME   = 6
RADIO_DESC_FRAME     = 7
INFO_MSG_FRAME       = 8
RADIO_STATIONS_FRAME = 9
SEATBELTS_FRAME      = 10
AIRBAG_STATUS_FRAME  = 11
INFO_TRIP1_FRAME     = 12
INFO_TRIP2_FRAME     = 13
INFO_INSTANT_FRAME   = 14
TRIP_MODE_FRAME      = 15
AUDIO_SETTINGS_FRAME = 16
SECRET_FRAME         = 17


def on_closing() :
    # Trouevr un moyen de killer le thread
    root.destroy()

def reading_loop() :
    with serial.Serial("/dev/ttyUSB0", 115200) as arduino:
        while True:
            data_line = arduino.readline()
            data_line = data_line.decode("utf-8")
            if "Entering Configuration Mode Successful!" not in data_line:
                if "Setting Baudrate Successful!" not in data_line:
                    split_data = data_line.split(" ")
                    FRAMEID = int(split_data[0].replace("FRAME:", ""))
                    DATA = split_data[1].replace("DATA:", "")
                    # DATA = DATA.srtrip("\n")
                    DATA = DATA.rstrip()
                    if FRAMEID == VOLUME_FRAME :
                        VOLUME_FRAME_DATA.set("Vol :" +DATA)
                        db.update({'Valeur': int(DATA)}, Query()['Nom'] == 'Volume')
                        db.update({'Valeur': int(time.time())}, Query()['Nom'] == 'Last_click')

                    if FRAMEID == TEMPERATURE_FRAME :
                        TEMPERATURE_FRAME_DATA.set(DATA)

                    if FRAMEID == RADIO_SOURCE_FRAME :
                        RADIO_SOURCE_FRAME_DATA.set(DATA)

                    if FRAMEID == RADIO_NAME_FRAME :
                        RADIO_NAME_FRAME_DATA.set(DATA)

                    if FRAMEID == RADIO_FREQ_FRAME :
                        RADIO_FREQ_FRAME_DATA.set(DATA)

                    if FRAMEID == RADIO_FMTYPE_FRAME :
                        RADIO_FMTYPE_FRAME_DATA.set(DATA)

                    if FRAMEID == RADIO_DESC_FRAME :
                        RADIO_DESC_FRAME_DATA.set(DATA)

                    if FRAMEID == INFO_MSG_FRAME :
                        INFO_MSG_FRAME_DATA.set(DATA)

                    if FRAMEID == RADIO_STATIONS_FRAME :
                        RADIO_STATIONS_FRAME_DATA.set(DATA)

                    if FRAMEID == SEATBELTS_FRAME :
                        SEATBELTS_FRAME_DATA.set(DATA)

                    if FRAMEID == AIRBAG_STATUS_FRAME :
                        AIRBAG_STATUS_FRAME_DATA.set(DATA)

                    if FRAMEID == INFO_TRIP1_FRAME :
                        INFO_TRIP1_FRAME_DATA.set(DATA)

                    if FRAMEID == INFO_TRIP2_FRAME :
                        INFO_TRIP2_FRAME_DATA.set(DATA)

                    if FRAMEID == INFO_INSTANT_FRAME :
                        INFO_INSTANT_FRAME_DATA.set(DATA)

                    if FRAMEID == TRIP_MODE_FRAME :
                        TRIP_MODE_FRAME_DATA.set(DATA)

                    if FRAMEID == AUDIO_SETTINGS_FRAME :
                        AUDIO_SETTINGS_FRAME_DATA.set(DATA)

                    if FRAMEID == SECRET_FRAME :
                        SECRET_FRAME_DATA.set(DATA)
                    else:
                        print ("ID = %s, DATA = %s" % (FRAMEID, DATA))

if __name__ == '__main__':
    w = tk.Label(root, text="VOLUME_FRAME_DATA  : ").grid(column=1, row=1)
    w = tk.Label(root, textvariable=VOLUME_FRAME_DATA).grid(column=2, row=1)

    w1 = tk.Label(root, text="TEMPERATURE_FRAME_DATA  : ").grid(column=1, row=2)
    w1 = tk.Label(root, textvariable=TEMPERATURE_FRAME_DATA).grid(column=2, row=2)

    w2 = tk.Label(root, text="RADIO_SOURCE_FRAME_DATA     : ").grid(column=1, row=3)
    w2 = tk.Label(root, textvariable=RADIO_SOURCE_FRAME_DATA ).grid(column=2, row=3)

    w3 = tk.Label(root, text="RADIO_NAME_FRAME_DATA  : ").grid(column=1, row=4)
    w3 = tk.Label(root, textvariable=RADIO_NAME_FRAME_DATA ).grid(column=2, row=4)

    w5 = tk.Label(root, text="RADIO_FREQ_FRAME_DATA  : ").grid(column=1, row=6)
    w5 = tk.Label(root, textvariable=RADIO_FREQ_FRAME_DATA ).grid(column=2, row=6)

    w6 = tk.Label(root, text="RADIO_FMTYPE_FRAME_DATA    : ").grid(column=1, row=7)
    w6 = tk.Label(root, textvariable=RADIO_FMTYPE_FRAME_DATA  ).grid(column=2, row=7)

    w7 = tk.Label(root, text="RADIO_DESC_FRAME_DATA  : ").grid(column=1, row=8)
    w7 = tk.Label(root, textvariable=RADIO_DESC_FRAME_DATA ).grid(column=2, row=8)

    w8 = tk.Label(root, text="INFO_MSG_FRAME_DATA  : ").grid(column=1, row=9)
    w8 = tk.Label(root, textvariable=INFO_MSG_FRAME_DATA ).grid(column=2, row=9)

    w9 = tk.Label(root, text="RADIO_STATIONS_FRAME_DATA  : ").grid(column=1, row=10)
    w9 = tk.Label(root, textvariable=RADIO_STATIONS_FRAME_DATA ).grid(column=2, row=10)

    w10 = tk.Label(root, text="SEATBELTS_FRAME_DATA  : ").grid(column=1, row=11)
    w10 = tk.Label(root, textvariable=SEATBELTS_FRAME_DATA ).grid(column=2, row=11)

    w11 = tk.Label(root, text="AIRBAG_STATUS_FRAME_DATA   : ").grid(column=1, row=12)
    w11 = tk.Label(root, textvariable=AIRBAG_STATUS_FRAME_DATA  ).grid(column=2, row=12)

    w12 = tk.Label(root, text="INFO_TRIP1_FRAME_DATA   : ").grid(column=1, row=13)
    w12 = tk.Label(root, textvariable=INFO_TRIP1_FRAME_DATA  ).grid(column=2, row=13)

    w13 = tk.Label(root, text="INFO_TRIP2_FRAME_DATA   : ").grid(column=1, row=14)
    w13 = tk.Label(root, textvariable=INFO_TRIP2_FRAME_DATA  ).grid(column=2, row=14)

    w14 = tk.Label(root, text="INFO_INSTANT_FRAME_DATA    : ").grid(column=1, row=15)
    w14 = tk.Label(root, textvariable=INFO_INSTANT_FRAME_DATA   ).grid(column=2, row=15)

    w15 = tk.Label(root, text="TRIP_MODE_FRAME_DATA     : ").grid(column=1, row=16)
    w15 = tk.Label(root, textvariable=TRIP_MODE_FRAME_DATA   ).grid(column=2, row=16)

    w16 = tk.Label(root, text="AUDIO_SETTINGS_FRAME_DATA   : ").grid(column=1, row=17)
    w16 = tk.Label(root, textvariable=AUDIO_SETTINGS_FRAME_DATA  ).grid(column=2, row=17)

    w17 = tk.Label(root, text="SECRET_FRAME_DATA   : ").grid(column=1, row=18)
    w17 = tk.Label(root, textvariable=SECRET_FRAME_DATA  ).grid(column=2, row=18)

    root.after(0, threading.Thread(target=reading_loop).start())
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()