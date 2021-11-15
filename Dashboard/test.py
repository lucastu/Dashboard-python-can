#!/usr/bin/python

import dbus

SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".MediaPlayer1"
bus = dbus.SystemBus()
manager = dbus.Interface(bus.get_object(SERVICE_NAME, "/"),
                    "org.freedesktop.DBus.ObjectManager")

def control(action):
    objects = manager.GetManagedObjects()
    for path, ifaces in objects.items():
        adapter = ifaces.get(ADAPTER_INTERFACE)
        if adapter is None:
            continue
        player = bus.get_object('org.bluez',path)
        BT_Media_iface = dbus.Interface(player, dbus_interface=ADAPTER_INTERFACE)
        break
    print (adapter.get('Status'))
    if action == 'playpause':
        if adapter.get('Status') == "playing":
            BT_Media_iface.Pause()
        else:
            BT_Media_iface.Play()
    elif action == 'stop':
        BT_Media_iface.Stop()
    elif action == 'next':
        BT_Media_iface.Next()
    elif action == 'pre':
        BT_Media_iface.Previous()
if __name__ == '__main__':
    control('playpause')
