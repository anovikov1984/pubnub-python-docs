import logging

import asyncio
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

logger = logging.getLogger("pubnub")

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'
pnconfig.uuid = 'Stephen'

pubnub = PubNubAsyncio(pnconfig)


def subscribe():
    pubnub.subscribe()\
        .channels("my_channel")\
        .with_presence()\
        .execute()


# > here_now:
async def here_now_snippet():
    envelope = await pubnub.here_now()\
        .channels(['cool_channel1', 'cool_channel2'])\
        .include_uuids(True)\
        .future()

    if envelope.status.is_error():
        # handle error
        return

    for channel_data in envelope.result.channels:
        print("---")
        print("channel: %s" % channel_data.channel_name)
        print("occupancy: %s" % channel_data.occupancy)

        print("occupants: %s" % channel_data.channel_name)
        for occupant in channel_data.occupants:
            print("uuid: %s, state: %s" % (occupant.uuid, occupant.state))


async def here_now2():
    envelope = await pubnub.here_now()\
        .include_state(True)\
        .include_uuids(True)\
        .future()


async def get_state():
    envelope = await pubnub.get_state()\
        .channels("my_channel")\
        .uuid("jbonham")\
        .future()


async def set_state():
    envelope = await pubnub.set_state()\
        .channels("my_channel")\
        .state({"full_name": "James Patrick Page"})\
        .uuid("jbonham")\
        .future()


def config():
    pnconfig = PNConfiguration()

    pnconfig.subscribe_key = 'demo'
    pnconfig.publish_key = 'demo'
    pnconfig.set_presence_timeout_with_custom_interval(320, 20)

    pubnub = PubNubAsyncio(pnconfig)


loop = asyncio.get_event_loop()
loop.run_until_complete(here_now_snippet())
