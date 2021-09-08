#!/usr/bin/env python3

import sys
import threading
import traceback
import time

from source_handler import InvalidFrame, SerialHandler


can_messages = {}
can_messages_lock = threading.Lock()

thread_exception = None

baudrate = 115200
serial_device = "/dev/ttyUSB0"

def reading_loop(source_handler):
    """Background thread for reading."""
    

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
    try:
        # If reading from a serial device, it will be opened with timeout=0 (non-blocking read())
        source_handler.open()
        
        #NOUVEAU
        try:
        while True:
            try:
                frame_id, data = source_handler.get_message()
            except InvalidFrame:
                #si le frame reçu n'est pas valable, on oublie et on recommence
                continue
            except EOFError:
                #si erreur on quit la boucle
                break

            # Add the frame to the can_messages dict and tell the main thread to refresh its content
            with can_messages_lock:
                can_messages[frame_id] = data
                print ("FRAME ID %s  :  %s" % (frame_id, format_data_hex(data)))
    except:
      # Only log exception if we were not going to stop the thread
      # When quitting, the main thread calls close() on the serial device
      # and read() may throw an exception. We don't want to display it as
      # we're stopping the script anyway
      global thread_exception
      thread_exception = sys.exc_info()
            
            
    #NOUVEAU                  
    finally:
        # Cleanly stop reading thread before exiting
      if source_handler:
          source_handler.close()

      # If the thread returned an exception, print it
      if thread_exception:
          traceback.print_exception(*thread_exception)
          sys.stderr.flush()

if __name__ == '__main__':
    run()
