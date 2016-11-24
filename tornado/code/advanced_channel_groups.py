import time

from tornado.ioloop import IOLoop
from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_tornado import PubNubTornado
from pubnub.callbacks import SubscribeCallback
from tornado import gen

pnconf = PNConfiguration()
pnconf.publish_key = "demo"
pnconf.subscribe_key = "demo"
pubnub = PubNubTornado(pnconf)


@gen.coroutine
def main():
    ####
    data = {
      'author': 'user-a',
      'status': 'I am reading about Advanced Channel Groups!',
      'timestamp': time.time()
    }

    try:
        result = yield pubnub.publish()\
             .message(data)\
             .channel("ch-user-b-present")\
             .future()

        print("Message published with timetoken %s" % result.timetoken)
    except PubNubException as e:
        print("Operation failed w/ status: %s" % e)


    ####
    try:
        yield pubnub.add_channel_to_channel_group()\
             .channel_group("cg-user-a-friends")\
             .channels("ch-user-a-present")\
             .future()

        print("Channel added to channel group")
    except PubNubException as e:
        print("Operation failed w/ status: %s" % e)

    try:
        yield pubnub.add_channel_to_channel_group()\
             .channel_group("cg-user-a-status-feed")\
             .channels("ch-user-a-present")\
             .future()

        print("Channel added to channel group")
    except PubNubException as e:
        print("Operation failed w/ status: %s" % e)

    ####
    try:
        yield pubnub.add_channel_to_channel_group()\
             .channel_group("cg-user-a-friends")\
             .channels("ch-user-b-present")\
             .future()

        print("Channel added to channel group")
    except PubNubException as e:
        print("Operation failed w/ status: %s" % e)

    try:
        yield pubnub.add_channel_to_channel_group()\
             .channel_group("cg-user-a-status-feed")\
             .channels("ch-user-b-status")\
             .future()

        print("Channel added to channel group")
    except PubNubException as e:
        print("Operation failed w/ status: %s" % e)

    try:
        yield pubnub.add_channel_to_channel_group()\
             .channel_group("cg-user-b-friends")\
             .channels("ch-user-a-present")\
             .future()

        print("Channel added to channel group")
    except PubNubException as e:
        print("Operation failed w/ status: %s" % e)

    try:
        yield pubnub.add_channel_to_channel_group()\
             .channel_group("cg-user-b-status-feed")\
             .channels("ch-user-a-status")\
             .future()

        print("Channel added to channel group")
    except PubNubException as e:
        print("Operation failed w/ status: %s" % e)


    ####
    try:
        env = yield pubnub.list_channels_in_channel_group()\
             .channel_group("cg-user-a-friends")\
             .envelope()

        print("FRIEND LIST:")

        for channel in env.result.channels:
            print(channel)
    except PubNubException as e:
        print("Operation failed w/ status: %s" % e)


    ####
    try:
        env = yield pubnub.here_now()\
            .channels("cg-user-a-status") \
            .envelope()

        print("ONLINE NOW: %d" % env.result.total_occupancy)

    except PubNubException as e:
        print("Operation failed w/ status: %s" % e)


    ####
    class PresenceListener(SubscribeCallback):
        def status(self, pubnub, status):
            pass

        def message(self, pubnub, message):
            pass

        def presence(self, pubnub, presence):
            print("FRIEND PRESENCE: %s" % presence)

    my_listener = PresenceListener()

    pubnub.add_listener(my_listener)

    pubnub.subscribe().channel_groups("cg-user-a-friends").with_presence().execute()


    ####
    class MessageListener(SubscribeCallback):
        def status(self, pubnub, status):
            pass

        def message(self, pubnub, message):
            print("MESSAGE: %s" % message)

        def presence(self, pubnub, presence):
            pass

    my_listener = MessageListener()
    pubnub.add_listener(my_listener)

    pubnub.subscribe().channel_groups("cg-user-a-friends").execute()

if __name__ == '__main__':
    IOLoop.current().run_sync(main())
