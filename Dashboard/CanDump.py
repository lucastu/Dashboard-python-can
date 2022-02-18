#!/usr/bin/env python3


############ Libraries import from my files ###############
import sys
import traceback
import time
import os
import threading

from source_handler import InvalidFrame, SerialHandler

############## Event for closing everything ##############
stop_reading = threading.Event()

################## USB Arduino parameters  #################
baudrate = 115200
serial_device = "/dev/ttyUSB0"

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

framenamedict = {
0x00:    "INIT_STATUS_FRAME",
0x01:    "VOLUME_FRAME",
0x02:    "TEMPERATURE_FRAME",
0x03:    "RADIO_SOURCE_FRAME",
0x04:    "RADIO_NAME_FRAME",
0x05:    "RADIO_FREQ_FRAME",
0x06:    "RADIO_FMTYPE_FRAME",
0x07:    "RADIO_DESC_FRAME",
0x08:    "INFO_MSG_FRAME",
0x09:    "RADIO_STATIONS_FRAME",
0x0C:    "INFO_TRIP_FRAME",
0x0E:    "INFO_INSTANT_FRAME",
0x10:    "AUDIO_SETTINGS_FRAME",
0x11:    "REMOTE_COMMAND_FRAME",
0x12:    "OPEN_DOOR_FRAME",
0x13:    "TIME_FRAME",
0x14:    "SHUTDOWN_FRAME"
}

def run():
    source_handler = SerialHandler(serial_device, baudrate)
    # Reading from a serial device, opened with timeout=0 (non-blocking read())
    source_handler.open()

    while True:
        try:
            frame_id, data = source_handler.get_message()
        except InvalidFrame:
            continue
        except EOFError:
            break
        if frame_id in framenamedict:
            print(f"FRAME ID {hex(frame_id)}({framenamedict[frame_id]}) DATA : Hex:{format_data_hex(data)}, ASCII: {format_data_ascii(data)}")
        else :
            print(f"FRAME ID {hex(frame_id)}(UNKNOWN) DATA : Hex:{format_data_hex(data)}, ASCII: {format_data_ascii(data)}")

if __name__ == '__main__':
    run()
