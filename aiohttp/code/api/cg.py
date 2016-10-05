import logging
import pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.publish_key = "pub-c-98863562-19a6-4760-bf0b-d537d1f5c582"
pnconfig.subscribe_key = "sub-c-7ba2ac4c-4836-11e6-85a4-0619f8945a4f"
pnconfig.secret_key = "sec-c-MGFkMjQxYjMtNTUxZC00YzE3LWFiZGYtNzUwMjdjNmM3NDhk"

pubnub = PubNub(pnconfig)


def grant_handler(result, status):
    if status.is_error():
        # handle error
        return

    print(result)


pubnub.add_channel_to_channel_group().\
    channels(["ch1", "ch2"]).\
    channel_group("cg1").\
    sync()

pubnub.list_channels_in_channel_group().\
    channel_group("cg1").\
    sync()

pubnub.remove_channel_from_channel_group().\
    channels(["ch1", "ch2"]).\
    channel_group("cg1").\
    sync()

pubnub.remove_channel_group().\
    channel_group("cg1").sync()
