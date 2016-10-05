import time

import asyncio
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNubAsyncio(pnconfig)


# > time
async def time_snippet():
    envelope = await pubnub.time().future()
    print('current time: %d' % envelope.result)


# > subscribe
def subscribe_snippet():
    pubnub.subscribe().channels('my_channel').execute()


# > publish
async def publish_snippet():
    def publish_callback(task):
        exception = task.exception()

        if exception is None:
            envelope = task.result()
            # Handle PNPublishResult(envelope.result) and PNStatus (envelope.status)
            pass
        else:
            # Handle exception
            pass

    asyncio.ensure_future(pubnub.publish().channel('such_channel').message(['hello', 'there']).future()) \
        .add_done_callback(publish_callback)

    await asyncio.sleep(10)


# > here_now:
async def here_now():
    envelope = await asyncio.ensure_future(pubnub.here_now().channels('demo').include_uuids(True).future())

    if envelope.status.is_error():
        return

    for channel_data in envelope.result.channels:
        print("---")
        print("channel: %s" % channel_data.channel_name)
        print("occupancy: %s" % channel_data.occupancy)

        print("occupants: %s" % channel_data.channel_name)
        for occupant in channel_data.occupants:
            print("uuid: %s, state: %s" % (occupant.uuid, occupant.state))

    pubnub.stop()


def presence_snippet():
    pubnub.subscribe().channels('my_channel').with_presence().execute()


async def history_snippet():
    envelope = await pubnub.history().channel('history_channel').count(100).future()
    # handle messages stored at evelope.result.messages
    # status is available as envelope.status


def unsubscribe_snippet():
    pubnub.unsubscribe().channels(['my_channel', 'another_channel']).execute()
    pubnub.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(time_snippet())
