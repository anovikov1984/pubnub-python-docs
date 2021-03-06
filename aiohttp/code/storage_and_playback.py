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

async def grant():
    envelope = await pubnub.grant().auth_keys("blah").channels("history_channel").read(True).write(True).ttl(0).future()
    print("Grant access: %r" % envelope.status.is_error())

logger = logging.getLogger("pubnub")


async def publish500():
    for i in range(0, 500):
        envelope = await pubnub.publish()\
            .message(['message#', i])\
            .channel('history_channel')\
            .should_store(True)\
            .future()

        print("%d: %s" % (i, envelope.status.is_error()))


async def pulling_history():
    envelope = await pubnub.history()\
        .channel("history_channel")\
        .count(2)\
        .future()

    print(envelope)


async def time_interval():
    envelope = await pubnub.history()\
        .channel("history_channel")\
        .count(100) \
        .start(13847168620721752)\
        .end(13847168819178600)\
        .future()

    print(envelope)


async def include_tt():
    envelope = await pubnub.history()\
        .channel("history_channel")\
        .count(100) \
        .include_timetoken(True)\
        .future()

    print(envelope)

async def get_all_messages(start_tt):
    envelope = await pubnub.history()\
        .channel('history_channel')\
        .count(100)\
        .start(start_tt)\
        .future()

    msgs = envelope.result.messages
    start = envelope.result.start_timetoken
    end = envelope.result.end_timetoken
    count = len(msgs)

    if count > 0:
        print("%d" % count)
        print("start %d" % start)
        print("end %d" % end)

    if count == 100:
        await get_all_messages(start)



loop = asyncio.get_event_loop()
loop.run_until_complete(grant())
# loop.run_until_complete(publish500())
loop.run_until_complete(get_all_messages(14759343456292767))
