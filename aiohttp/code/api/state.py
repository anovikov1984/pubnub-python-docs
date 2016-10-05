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


def get_state_handler(result, status):
    if status.is_error():
        # handle error
        return

    print(result)


pubnub.set_state().channels("my_channel").state({'age': 30}).sync()
pubnub.get_state().channels("my_channel").async(get_state_handler)





