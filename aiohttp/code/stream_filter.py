import logging

import asyncio
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNubAsyncio(pnconfig)

logger = logging.getLogger("pubnub")


async def publish_with_meta():
    meta = {
        'my': 'meta',
        'name': 'PubNub'
    }

    await pubnub.publish().channel('ch1').meta(meta).message('hello').future()


def subscribing_with_filtering():
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = 'my_key'
    pnconfig.filter_expression = "filter == expression"
    pubnub = PubNubAsyncio(pnconfig)

loop = asyncio.get_event_loop()
loop.run_until_complete(publish_with_meta())
