import time
from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

pnconf = PNConfiguration()
pnconf.publish_key = "demo"
pnconf.subscribe_key = "demo"
pubnub = PubNub(pnconf)


####
data = {
  'author': 'user-a',
  'status': 'I am reading about Advanced Channel Groups!',
  'timestamp': time.time()
}

try:
    envelope = pubnub.publish()\
         .message(data)\
         .channel("ch-user-b-present")\
         .sync()

    print("Message published with timetoken %s" % envelope.result.timetoken)
except PubNubException as e:
    print("Operation failed w/ status: %s" % e)


####
try:
    result = pubnub.add_channel_to_channel_group()\
         .channel_group("cg-user-a-friends")\
         .channels("ch-user-a-present")\
         .sync()

    print("Channel added to channel group")
except PubNubException as e:
    print("Operation failed w/ status: %s" % e)

try:
    result = pubnub.add_channel_to_channel_group()\
         .channel_group("cg-user-a-status-feed")\
         .channels("ch-user-a-present")\
         .sync()

    print("Channel added to channel group")
except PubNubException as e:
    print("Operation failed w/ status: %s" % e)

####
try:
    result = pubnub.add_channel_to_channel_group()\
         .channel_group("cg-user-a-friends")\
         .channels("ch-user-b-present")\
         .sync()

    print("Channel added to channel group")
except PubNubException as e:
    print("Operation failed w/ status: %s" % e)

try:
    result = pubnub.add_channel_to_channel_group()\
         .channel_group("cg-user-a-status-feed")\
         .channels("ch-user-b-status")\
         .sync()

    print("Channel added to channel group")
except PubNubException as e:
    print("Operation failed w/ status: %s" % e)


try:
    result = pubnub.add_channel_to_channel_group()\
         .channel_group("cg-user-b-friends")\
         .channels("ch-user-a-present")\
         .sync()

    print("Channel added to channel group")
except PubNubException as e:
    print("Operation failed w/ status: %s" % e)

try:
    result = pubnub.add_channel_to_channel_group()\
         .channel_group("cg-user-b-status-feed")\
         .channels("ch-user-a-status")\
         .sync()

    print("Channel added to channel group")
except PubNubException as e:
    print("Operation failed w/ status: %s" % e)


####
try:
    env = pubnub.list_channels_in_channel_group()\
         .channel_group("cg-user-a-friends")\
         .sync()

    print("FRIEND LIST:")

    for channel in env.result.channels:
        print(channel)
except PubNubException as e:
    print("Operation failed w/ status: %s" % e)


####
try:
    env = pubnub.here_now()\
        .channels("cg-user-a-status") \
        .sync()

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

pubnub.add_listener(my_listener)

pubnub.subscribe().channel_groups("cg-user-a-friends").execute()
