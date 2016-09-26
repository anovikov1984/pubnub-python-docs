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


# subscribe_callback
class MyCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.operation == PNOperationType.PNSubscribeOperation \
                and status.category == PNStatusCategory.PNConnectedCategory:
            print("connected")

    def presence(self, pubnub, presence):
        pass

    def message(self, pubnub, message):
        pass

my_listener = MyCallback()
pubnub.add_listener(my_listener)
pubnub.subscribe().channel("my_channel").execute()

# subscribe_listener
my_listener = SubscribeListener()

pubnub.add_listener(my_listener)
pubnub.subscribe().channel("my_channel").execute()

my_listener.wait_for_connect()
print('connected')
