import logging
import pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory, PNPushType

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.publish_key = "demo"
pnconfig.subscribe_key = "demo"
pnconfig.secret_key = "demo"

pubnub = PubNub(pnconfig)


def gcm_handler(result, status):
    if status.is_error():
        # handle error
        return

    print(result)

envelope = pubnub.add_channels_to_push()\
    .push_type(PNPushType.GCM)\
    .channels("ch1", "ch2", "ch3")\
    .device_id("deviceId")\
    .sync()

envelope = pubnub.remove_channels_from_push()\
    .push_type(PNPushType.GCM)\
    .channels("ch1", "ch2", "ch3")\
    .device_id("deviceId")\
    .sync()
