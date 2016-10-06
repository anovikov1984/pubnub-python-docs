from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_tornado import PubNubTornado

from tornado import gen
from tornado.ioloop import IOLoop

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNubTornado(pnconfig)


# > time
@gen.coroutine
def time_snippet():
    envelope = yield pubnub.time().future()
    print('current time: %d' % envelope.result)


# > subscribe
def subscribe_snippet():
    pubnub.subscribe().channels('my_channel').execute()


# > publish
@gen.coroutine
def publish_snippet():
    def publish_callback(task):
        exception = task.exception()

        if exception is None:
            envelope = task.result()
            # Handle PNPublishResult(envelope.result) and PNStatus (envelope.status)
            pass
        else:
            # Handle exception
            pass

    pubnub.publish().channel('such_channel').message(['hello', 'there']).future().add_done_callback(publish_callback)

    yield gen.sleep(10)


# > here_now:
@gen.coroutine
def here_now():
    envelope = yield pubnub.here_now().channels('demo').include_uuids(True).future()

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


@gen.coroutine
def history_snippet():
    envelope = yield pubnub.history().channel('history_channel').count(100).future()
    # handle messages stored at envelope.result.messages
    # status is available as envelope.status


def unsubscribe_snippet():
    pubnub.unsubscribe().channels(['my_channel', 'another_channel']).execute()
    pubnub.stop()


if __name__ == '__main__':
    IOLoop.current().run_sync(here_now)
