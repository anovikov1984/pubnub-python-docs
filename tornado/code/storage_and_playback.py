import logging

import asyncio
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_tornado import PubNubTornado
from tornado.ioloop import IOLoop

pnconfig = PNConfiguration()

pnconfig.publish_key = "pub-c-98863562-19a6-4760-bf0b-d537d1f5c582"
pnconfig.subscribe_key = "sub-c-7ba2ac4c-4836-11e6-85a4-0619f8945a4f"
pnconfig.secret_key = "sec-c-MGFkMjQxYjMtNTUxZC00YzE3LWFiZGYtNzUwMjdjNmM3NDhk"
pnconfig.auth_key = "blah"
pnconfig.enable_subscribe = False

pubnub = PubNubTornado(pnconfig)

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

if __name__ == '__main__':
    # IOLoop.current().run_sync(publish500)
    IOLoop.current().run_sync(lambda: get_all_messages(14759343456292767))

