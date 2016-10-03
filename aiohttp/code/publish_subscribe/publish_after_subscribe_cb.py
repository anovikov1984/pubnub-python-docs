import logging

import asyncio
import pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.publish_key = "demo"
pnconfig.subscribe_key = "demo"

pubnub = PubNubAsyncio(pnconfig)


async def main():
    class MyListener(SubscribeCallback):
        def status(self, pubnub, status):
            if status.category == PNStatusCategory.PNConnectedCategory:
                asyncio.ensure_future(pubnub.publish().channel("awesomeChannel").message({'fieldA': 'awesome', 'fieldB': 10}).future())

        def message(self, pubnub, message):
            pass

        def presence(self, pubnub, presence):
            pass

    my_listener = MyListener()

    pubnub.add_listener(my_listener)

    pubnub.subscribe().channels("awesomeChannel").execute()
    await asyncio.sleep(10)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

