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


pubnub.grant().channels(["ch1", "ch2", "ch3"]).\
    channel_groups(["cg1", "cg2"]).\
    auth_keys(["key1", "key2"]).\
    read(True).write(True).manage(True).\
    async(grant_handler)
    # ttl(12337).\







