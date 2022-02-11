#
#  API to retrieve informations from the Open Auto pro soft
#  Based on https://github.com/bluewave-studio/openauto-pro-api  Copyright (C) BlueWave Studio - All Rights Reserved
#

import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler

# Output something like that :
# received hello response, result: 1, oap version: 15.0, api version: 1.0
# media metadata, artist: Amadou & Mariam feat. Santigold, title: Dougou Badia (feat. Santigold), album: Folila, duration label: 03:54
# media status, is playing: True, position label: 03:20, source: 3


class EventHandler(ClientEventHandler, root):
    ''' Handle the define events e.g. data coming from OAP API '''
    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
            .format(message.result, message.oap_version.major, message.oap_version.minor, message.api_version.major, message.api_version.minor))

        set_status_subscriptions = oap_api.SetStatusSubscriptions()
        set_status_subscriptions.subscriptions.append(oap_api.SetStatusSubscriptions.Subscription.MEDIA)
        client.send(oap_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0, set_status_subscriptions.SerializeToString())

    def on_media_status(self, client, message):
        print(f"media status, is playing: {message.is_playing}, position label: {message.position_label}, source: { message.source}"

        self.Bluetooth_timing.setText(message.position_label)
        # Retrieve Bluetooth_duration value to calculate a percentage
        position_label_in_sec=int(message.position_label[:-3])*60+int(message.position_label[-2:])
        duration_label = self.Bluetooth_duration.text()
        duration_label_in_sec =int(duration_label[:-3])*60+int(duration_label[-2:])
        percent=(position_label_in_sec/duration_label_in_sec)*100
        self.percent.setText(str(percent))
        # Send signal to update progress bar according to percent value
        self.custom_signals.update_progress_bluetooth_track_signal.emit()

    def on_media_metadata(self, client, message):
        print(f"media metadata, artist: {message.artist}, title: {message.title}, album: {message.album}, duration label: {message.duration_label}"

        self.Bluetooth_track.setText(message.title)
        self.Bluetooth_artist.setText(message.artist)
        self.Bluetooth_duration.setText(message.duration_label)

def mediadata(root):
    client = Client("media data")
    event_handler = EventHandler()
    client.set_event_handler(event_handler, root)
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    client.disconnect()


if __name__ == "__main__":
    mediadata()
