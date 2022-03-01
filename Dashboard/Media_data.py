#
#  API to retrieve informations from the Open Auto pro soft
#  Based on https://github.com/bluewave-studio/openauto-pro-api 
#
import time
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler

class EventHandler(ClientEventHandler):
    ''' Handle events comming from OAP API'''
    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
                .format(message.result, message.oap_version.major,
                        message.oap_version.minor, message.api_version.major,
                        message.api_version.minor))

        set_status_subscriptions = oap_api.SetStatusSubscriptions()
        set_status_subscriptions.subscriptions.append(
            oap_api.SetStatusSubscriptions.Subscription.MEDIA)
        client.send(oap_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

def wait_for_media_message(client, root):
    can_continue = True

    message = client.receive()
    if message.id == oap_api.MESSAGE_PING:
        client.send(oap_api.MESSAGE_PONG, 0, bytes())
    elif message.id == oap_api.MESSAGE_BYEBYE:
        can_continue = False

    if client._event_handler is not None:
        if message.id == oap_api.MESSAGE_HELLO_RESPONSE:
            hello_response = oap_api.HelloResponse()
            hello_response.ParseFromString(message.payload)
            client._event_handler.on_hello_response(client, hello_response)

        elif message.id == oap_api.MESSAGE_MEDIA_STATUS:
            media_status = oap_api.MediaStatus()
            media_status.ParseFromString(message.payload)
            if root == 0:
                print(f"media status, is playing: {media_status.is_playing}, position label: {media_status.position_label}, source: {media_status.source}")
            else:
                # Retrieve media_duration value to calculate a percentage
                # xx:xx:xx instead of xx:xx
                duration_label_value = root.media_duration.text()
                if media_status.position_label != '' and duration_label_value != '00:00':
                    position_label = media_status.position_label.split(':')
                    if len(position_label)==2:
                        position_label_in_sec = int(position_label[0])*60+int(position_label[1])
                    elif len(position_label)==3:
                        position_label_in_sec = int(position_label[0])*3600+int(position_label[1])*60+int(position_label[1])

                    duration_label = duration_label_value.split(':')
                    if len(duration_label)==2:
                        duration_label_in_sec = int(duration_label[0])*60+int(duration_label[1])
                    elif len(duration_label)==3:    
                        duration_label_in_sec = int(duration_label[0])*3600+int(duration_label[1])*60+int(duration_label[1])

                    percent = (position_label_in_sec / duration_label_in_sec) * 100

                    # Send signal to update progress bar according to percent value
                    root.percent.setText(str(percent))
                    root.media_timing.setText(media_status.position_label)
                    root.custom_signals.update_progress_media_track_signal.emit()

        elif message.id == oap_api.MESSAGE_MEDIA_METADATA:
            media_metadata = oap_api.MediaMetadata()
            media_metadata.ParseFromString(message.payload)
            if root == 0:
                print(f"media metadata, artist: {media_metadata.artist}, title: {media_metadata.title}, album: {media_metadata.album}, duration label: {media_metadata.duration_label}")
            else:
                root.media_track.setText('No Title' if not media_metadata.title else media_metadata.title)
                root.media_artist.setText('No Artist' if not media_metadata.artist else media_metadata.artist)
                root.media_duration.setText(media_metadata.duration_label)
    return can_continue


def mediadata(root):
    if root !=0 :
        time.sleep(2)
    client = Client('Media_data')
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)
    active = True
    while active:
        try:
            active = wait_for_media_message(client, root)
        except KeyboardInterrupt:
            break

    client.disconnect()


if __name__ == "__main__":
    # if the mediadata argument is set to 0, the script print the result to the console
    mediadata(0)
