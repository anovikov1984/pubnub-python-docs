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

pubnub = PubNub(pnconfig)


class MyListener(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            pubnub.publish().channel("awesomeChannel").message({'fieldA': 'awesome', 'fieldB': 10}).sync()

    def message(self, pubnub, message):
        pass

    def presence(self, pubnub, presence):
        pass

my_listener = MyListener()

pubnub.add_listener(my_listener)

pubnub.subscribe().channels("awesomeChannel").execute()
