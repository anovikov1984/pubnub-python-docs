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

my_listener = SubscribeListener()
pubnub.add_listener(my_listener)

pubnub.subscribe().channels("awesomeChannel").execute()
my_listener.wait_for_connect()
print("connected")

pubnub.publish().channel("awesomeChannel").message({'fieldA': 'awesome', 'fieldB': 10}).sync()
result = my_listener.wait_for_message_on("awesomeChannel")
print(result.message)

pubnub.unsubscribe().channels("awesomeChannel").execute()
my_listener.wait_for_disconnect()

print("unsubscribed")
