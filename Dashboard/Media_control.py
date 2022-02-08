import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler


def run(action=""):
    client = Client("media control")
    client.connect('127.0.0.1', 44405)

    key_type = None

    if action == "playpause":
        key_type = oap_api.KeyEvent.KEY_TYPE_TOGGLE_PLAY
    elif action == "previous":
        key_type = oap_api.KeyEvent.KEY_TYPE_PREVIOUS_TRACK
    elif action == "next":
        key_type = oap_api.KeyEvent.KEY_TYPE_NEXT_TRACK

    print(action)

    if key_type is not None :
        key_event = oap_api.KeyEvent()
        key_event.key_type = key_type

        key_event.event_type = oap_api.KeyEvent.EVENT_TYPE_PRESS
        client.send(oap_api.MESSAGE_KEY_EVENT, 0, key_event.SerializeToString())

        key_event.event_type = oap_api.KeyEvent.EVENT_TYPE_RELEASE
        client.send(oap_api.MESSAGE_KEY_EVENT, 0, key_event.SerializeToString())
    else :
        print('Nothing Done')
    client.disconnect()


if __name__ == "__main__":
    # action="playpause"
    # action="previous"
    # action="next"
    run()