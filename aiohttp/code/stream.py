import logging

import time
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNub(pnconfig)

logger = logging.getLogger("pubnub")

channel_group = "family"

pubnub.add_channel_to_channel_group()\
    .group(channel_group)\
    .channels("wife")\
    .future()

pubnub.subscribe().channel_groups(channel_group).execute()

pubnub.unsubscribe().channel_groups(channel_group).execute()

pubnub.subscribe().channel_groups(["cg1", "cg2"]).with_presence().execute()

pubnub.remove_channel_from_channel_group()\
    .group(channel_group)\
    .channels(["son", "daughter"])\
    .future()


pubnub.remove_channel_group()\
    .group(channel_group)\
    .future()
