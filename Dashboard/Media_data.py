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

def wait_for_media_message(client, root):
    can_continue = True

    message = client.receive()

    if message.id == oap_api.MESSAGE_PING:
        client.send(oap_api.MESSAGE_PONG, 0, bytes())
    elif message.id == oap_api.MESSAGE_BYEBYE:
        can_continue = False

    if client._event_handler is not None:
        if message.id == oap_api.MESSAGE_MEDIA_STATUS:
            media_status = oap_api.MediaStatus()
            media_status.ParseFromString(message.payload)
            # self._event_handler.on_media_status(self, media_status)
            if root == 0:
                print(f"media status, is playing: {message.is_playing}, position label: {message.position_label}, source: {message.source}")
            else:
                root.Bluetooth_timing.setText(message.position_label)
                # Retrieve Bluetooth_duration value to calculate a percentage
                position_label_in_sec = int(message.position_label[:-3]) * 60 + int(message.position_label[-2:])
                duration_label = root.Bluetooth_duration.text()
                duration_label_in_sec = int(duration_label[:-3]) * 60 + int(duration_label[-2:])
                percent = (position_label_in_sec / duration_label_in_sec) * 100
                root.percent.setText(str(percent))
                # Send signal to update progress bar according to percent value
                root.custom_signals.update_progress_bluetooth_track_signal.emit()

        elif message.id == oap_api.MESSAGE_MEDIA_METADATA:
            media_metadata = oap_api.MediaMetadata()
            media_metadata.ParseFromString(message.payload)
            # self._event_handler.on_media_metadata(self, media_metadata)
            if root == 0:
                print(f"media metadata, artist: {message.artist}, title: {message.title}, album: {message.album}, duration label: {message.duration_label}")
            else:
                root.Bluetooth_track.setText(message.title)
                root.Bluetooth_artist.setText(message.artist)
                root.Bluetooth_duration.setText(message.duration_label)
    return can_continue


def mediadata(root):
    client = Client("media data")
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = wait_for_media_message(client, root)
        except KeyboardInterrupt:
            break

    client.disconnect()


if __name__ == "__main__":
    # if the mediadata is set to 0, the script print the result to the console
    mediadata(0)
