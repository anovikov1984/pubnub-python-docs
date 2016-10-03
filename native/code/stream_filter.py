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


def publish_with_meta():
    meta = {
        'my': 'meta',
        'name': 'PubNub'
    }

    pubnub.publish().channel('ch1').meta(meta).message('hello').sync()


def subscribing_with_filtering():
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = 'my_key'
    pnconfig.filter_expression = "filter == expression"
    pubnub = PubNub(pnconfig)

publish_with_meta()
