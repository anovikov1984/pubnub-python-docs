import logging

import time
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

logger = logging.getLogger("pubnub")

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'
pnconfig.uuid = 'Stephen'

pubnub = PubNub(pnconfig)

pubnub.subscribe()\
    .channels("my_channel")\
    .with_presence()\
    .execute()


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

    pubnub.here_now().channels(['cool_channel1', 'cool_channel2']).include_uuids(True).async(here_now_callback)
    time.sleep(10)

pubnub.here_now()\
    .include_state(True)\
    .include_uuids(True)\
    .sync()


pubnub.get_state()\
    .channels("my_channel")\
    .uuid("jbonham")\
    .sync()


pubnub.set_state()\
    .channels("my_channel")\
    .state({"full_name": "James Patrick Page"})\
    .uuid("jbonham")\
    .sync()
