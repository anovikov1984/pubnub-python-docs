import logging
import pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.publish_key = "demo"
pnconfig.subscribe_key = "demo"
pnconfig.secret_key = "demo"

pubnub = PubNub(pnconfig)


def history_handler(result, status):
    if status.is_error():
        # handle error
        return

    print(result)


envelope = pubnub.history().channel("history_channel").count(100).sync()
print(envelope)

pubnub.history()\
    .channel("my_channel")\
    .count(100)\
    .start(-1)\
    .end(13847168819178600)\
    .reverse(True)
