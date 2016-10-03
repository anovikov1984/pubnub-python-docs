import logging

import asyncio
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

pnconfig = PNConfiguration()

pnconfig.publish_key = "pub-c-98863562-19a6-4760-bf0b-d537d1f5c582"
pnconfig.subscribe_key = "sub-c-7ba2ac4c-4836-11e6-85a4-0619f8945a4f"
pnconfig.secret_key = "sec-c-MGFkMjQxYjMtNTUxZC00YzE3LWFiZGYtNzUwMjdjNmM3NDhk"
pnconfig.auth_key = "blah"
pnconfig.enable_subscribe = False

pubnub = PubNubAsyncio(pnconfig)

envelope = pubnub.grant().auth_keys("blah").channels("history_channel").read(True).write(True).ttl(50).sync()
print("Grant access: %r" % envelope.status.is_error())

logger = logging.getLogger("pubnub")


async def publish500():
    for i in range(0, 500):
        envelope = await pubnub.publish()\
            .message(['message#', i])\
            .channel('history_channel')\
            .should_store(True)\
            .sync()

        print("%d: %s" % (i, envelope.status.is_error()))


async def pulling_history():
    envelope = await pubnub.history()\
        .channel("history_channel")\
        .count(2)\
        .sync()

    print(envelope)


async def time_interval():
    envelope = await pubnub.history()\
        .channel("history_channel")\
        .count(100) \
        .start(13847168620721752)\
        .end(13847168819178600)\
        .sync()

    print(envelope)


async def include_tt():
    envelope = await pubnub.history()\
        .channel("history_channel")\
        .count(100) \
        .include_timetoken(True)\
        .sync()

    print(envelope)

loop = asyncio.get_event_loop()
loop.run_until_complete(include_tt())


