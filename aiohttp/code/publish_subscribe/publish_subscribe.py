import logging

import asyncio
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNubAsyncio(pnconfig)

logger = logging.getLogger("pubnub")


async def main():
    envelope = await pubnub.publish()\
        .channel("my_channel")\
        .message(['hello', 'there'])\
        .should_store(True)\
        .use_post(True)\
        .future()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
