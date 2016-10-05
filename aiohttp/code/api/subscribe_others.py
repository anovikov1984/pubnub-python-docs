import logging
import pubnub

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNub(pnconfig)

pubnub.add_listener(SubscribeListener())


# 2
def second():
    pubnub.subscribe().channels(["my_channel1", "my_channel2"]).execute()


# 3
def third():
    pubnub.subscribe().channels("my_channel").with_presence().execute()


third()
