import logging

import asyncio
import pubnub

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio, SubscribeListener

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.publish_key = "demo"
pnconfig.subscribe_key = "demo"

pubnub = PubNubAsyncio(pnconfig)

async def main():
    my_listener = SubscribeListener()
    pubnub.add_listener(my_listener)

    pubnub.subscribe().channels("awesomeChannel").execute()
    await my_listener.wait_for_connect()
    print("connected")

    asyncio.ensure_future(pubnub.publish().channel("awesomeChannel").message({'fieldA': 'awesome', 'fieldB': 10}).future())
    result = await my_listener.wait_for_message_on("awesomeChannel")
    print(result.message)

    pubnub.unsubscribe().channels("awesomeChannel").execute()
    await my_listener.wait_for_disconnect()

    print("unsubscribed")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

