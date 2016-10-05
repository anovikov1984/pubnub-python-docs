import logging
import pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNub(pnconfig)


def here_now_callback(result, status):
    if status.is_error():
        # handle error
        return

    for channel_data in result.channels:
        print("---")
        print("channel: %s" % channel_data.channel_name)
        print("occupancy: %s" % channel_data.occupancy)

        print("occupants: %s" % channel_data.channel_name)
        for occupant in channel_data.occupants:
            print("uuid: %s, state: %s" % (occupant.uuid, occupant.state))

pubnub.here_now().channels("my_channel", "demo").include_uuids(True).async(here_now_callback)





