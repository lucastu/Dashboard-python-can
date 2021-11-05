#!/usr/bin/python

# from https://stackoverflow.com/questions/47718378/bluez-5-43-read-mediaplayer1-properties-python
# https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.43/doc/media-api.txt

# try this : qdbus --system org.bluez /org/bluez/hci0/dev_D8_C4_E9_B6_5C_80/player1

import dbus
bus = dbus.SystemBus()

player = bus.get_object('org.bluez','/org/bluez/hci0/dev_78_6A_89_FA_1C_95/player0')
BT_Media_iface = dbus.Interface(player, dbus_interface='org.bluez.MediaPlayer1')
BT_Media_props = dbus.Interface(player, "org.freedesktop.DBus.Properties")

#props = BT_Media_props.GetAll("org.bluez.MediaPlayer1")
props = BT_Media_props.getProperties()
print props
props = BT_Media_iface.getProperties()
print props
