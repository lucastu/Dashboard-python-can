#!/usr/bin/python

# https://qiita.com/eggman/items/339a9c9b338634ac27a5
# https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.43/doc/media-api.txt
# https://linuxtut.com/fr/30cb07454670450e3adf/  
  
import dbus
import time

class bluetooth_utils :
     SERVICE_NAME = "org.bluez"
     ADAPTER_INTERFACE = SERVICE_NAME + ".MediaPlayer1"
     bus = dbus.SystemBus()
     manager = dbus.Interface(bus.get_object(SERVICE_NAME, "/"), "org.freedesktop.DBus.ObjectManager")

     def control(self, action):
         objects = self.manager.GetManagedObjects()
         for path, ifaces in objects.items():
             adapter = ifaces.get(self.ADAPTER_INTERFACE)
             if adapter is not None:
                 # continue
                 player = self.bus.get_object('org.bluez', path)
                 BT_Media_iface = dbus.Interface(player, dbus_interface=self.ADAPTER_INTERFACE)
             # break

                 if action == 'playpause':
                     if adapter.get('Status') == "playing":
                         BT_Media_iface.Pause()
                     else :
                         BT_Media_iface.Play()
                 elif action == 'stop':
                     BT_Media_iface.Stop()
                 elif action == 'pre':
                     BT_Media_iface.Previous()
                 # elif action == 'next':
                 else:
                     BT_Media_iface.Next()


     def run(self):
        title, artist, album, timing_format, duration_format, in_track_postition = "No title", "No artist", "No album", "00:00", "00:00", "0"
        objects = self.manager.GetManagedObjects()
        for path, ifaces in objects.items():
            if 'player0' in path :
                adapter = ifaces.get(self.ADAPTER_INTERFACE)
                if adapter is not None:
                    # player = bus.get_object('org.bluez',path)
                    # BT_Media_iface = dbus.Interface(player, dbus_interface=ADAPTER_INTERFACE)
                    track =  adapter.get('Track')

                    title = track.get('Title')
                    artist = track.get('Artist')
                    album =  track.get('Album')

                    # Formatting the timing
                    millis = adapter.get('Position')
                    seconds = int((millis / 1000) % 60)
                    seconds = f"{seconds:02d}"
                    minutes = int((millis / (1000 * 60)) % 60)
                    minutes = f"{minutes:02d}"
                    timing_format = "%s:%s" % (minutes, seconds)
                    # Formatting the duration
                    millis2 = track.get('Duration')
                    seconds2 = int((millis2 / 1000) % 60)
                    seconds2 = f"{seconds2:02d}"
                    minutes2 = int((millis2 / (1000 * 60)) % 60)
                    minutes2 = f"{minutes2:02d}"
                    duration_format= "%s:%s" % (minutes2, seconds2)

                    # Postion of the reading from 0 to 1 (start to end
                    if int(track.get('Duration')) is not 0 :
                        # print(type(track.get('Duration')))
                        in_track_postition=int((adapter.get('Position')/track.get('Duration'))*100)

        return title, artist, album, timing_format, duration_format, in_track_postition

if __name__ == '__main__':
    B = bluetooth_utils()
    while True :
        track_info = B.run()
        print("title: " + str(track_info[0]))
        print("artist: " +  str(track_info[1]))
        print("album: " + str(track_info[2]))
        print("timing: " +  str(track_info[3]))
        print("duration: " +  str(track_info[4]))
        print("position: " + str(track_info[5]))
        time.sleep(1)