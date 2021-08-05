# Python CAN bus monitor

This script allows you to read live data from a CAN bus or offline CAN data from a file and display it in an easy-to-read table.

## Live

It's primarily meant to be used in conjunction with an Arduino and a CAN bus shield. You'll need this [Arduino sketch](https://github.com/alexandreblin/arduino-can-reader.git) to make it work.

You can also use any serial device capable of reading a CAN bus. It expects data in this format:

    FRAME:ID=X:LEN=Y:ZZ:ZZ:ZZ:ZZ:ZZ:ZZ:ZZ:ZZ

where `X` is the CAN frame ID (decimal), `Y` is the number of bytes in the frame, and `ZZ:ZZ...` are the actual bytes (in hex).

## Usage
Install the dependencies (preferably in a virtualenv)

    pip install -e .

Launch the script via le launcher.sh
