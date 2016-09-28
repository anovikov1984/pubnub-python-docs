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

pubnub.publish()\
    .channel("my_channel")\
    .message(['hello', 'there'])\
    .should_store(True)\
    .use_post(True)\
    .sync()

