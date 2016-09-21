import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNub(pnconfig)


# > time
def time_snippet():
    print('current time: %d', pubnub.time().sync().result)


# > subscribe
def subscribe_snippet():
    pubnub.subscribe().channels('my_channel').execute()


# > publish
def publish_snippet():
    def publish_callback(result, status):
        pass
        # Handle PNPublishResult and PNStatus

    pubnub.publish().channel('such_channel').message(['hello', 'there']).async(publish_callback)
    time.sleep(10)


# > here_now:
def here_now_snippet():
    def here_now_callback(result, status):
        if status.is_error():
            # handle error
            return

        for channel_data in result.channels:
            print("---")
            print("channel: %s" % channel_data.channel_name)
            print("occupancy: %s" % channel_data.occupancy)

            print("occupants: %s" % channel_data.channel_name)
            for occupant in channel_data.occupants:
                print("uuid: %s, state: %s" % (occupant.uuid, occupant.state))

    pubnub.here_now().channels('demo').include_uuids(True).async(here_now_callback)
    time.sleep(10)


def presence_snippet():
    pubnub.subscribe().channels('my_channel').with_presence().execute()


def history_snippet():
    envelope = pubnub.history().channel('history_channel').count(100).sync()
    # handle messages stored at evelope.result.messages
    # status is available as envelope.status


def unsubscribe_snippet():
    pubnub.unsubscribe().channels(['my_channel', 'another_channel']).execute()
    pubnub.stop()


unsubscribe_snippet()
