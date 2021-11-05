#!/usr/bin/python

import dbus

SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".MediaPlayer1"
bus = dbus.SystemBus()
manager = dbus.Interface(bus.get_object(SERVICE_NAME, "/"),
                    "org.freedesktop.DBus.ObjectManager")
objects = manager.GetManagedObjects()

if __name__ == '__main__':
    for path, ifaces in objects.iteritems():
        adapter = ifaces.get(ADAPTER_INTERFACE)
        if adapter is None:
            continue
        print path
        player = bus.get_object('org.bluez',path)
        BT_Media_iface = dbus.Interface(player, dbus_interface=ADAPTER_INTERFACE)
        break

    track =  adapter.get('Track')
    print('Title: ' + track.get('Title'))
    print('Artist: ' + track.get('Artist'))
    print('Album: ' + track.get('Album'))
    print('Duration: ' + str(track.get('Duration')))
    print('Timing: ' + str(adapter.get('Position')))
