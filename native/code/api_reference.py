import logging

import time
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNub(pnconfig)

logger = logging.getLogger("pubnub")


def handle_exception(e):
    print(str(e))


class BasicListener(SubscribeListener):
    def presence(self, pubnub, presence):
        pass

    def message(self, pubnub, message):
        pass

basic_listener = BasicListener()
pubnub.add_listener(basic_listener)


# > publish basic
def publish_snippet():
    def publish_callback(result, status):
        pass
        # handle publish result, status always present, result if successful
        # status.isError to see if error happened

    pubnub.publish().channel("my_channel").message(["hello", "there"])\
        .should_store(True).use_post(True).async(publish_callback)
    time.sleep(10)


# > publish #1 with meta
def publish_with_meta_snippet():
    def publish_callback(result, status):
        pass
        # handle publish result, status always present, result if successful
        # status.isError to see if error happened

    pubnub.publish().channel("my_channel").message(["hello", "there"]) \
        .meta({'name': 'Alex'}).async(publish_callback)
    time.sleep(10)


# > publish #2 object
def publish_dict():
    try:
        envelope = pubnub.publish().channel("my_channel").message({'name': 'Alex', 'online': True}).sync()
        print("publish timetoken: %d" % envelope.result.timetoken)
    except PubNubException as e:
        handle_exception(e)

    time.sleep(100)


def subscribe_basic():
    pubnub.subscribe().channels("my_channel").execute()

    # helpers
    basic_listener.wait_for_connect()
    pubnub.publish().channel("my_channel").message("hey").sync()
    time.sleep(10)


def subscribe_with_presence():
    pubnub.subscribe().channels("my_channel").with_presence().execute()
    time.sleep(10)


subscribe_with_presence()

