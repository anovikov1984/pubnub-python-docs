import logging
import pubnub

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNub(pnconfig)

my_listener = SubscribeListener()
pubnub.add_listener(my_listener)

pubnub.subscribe().channels("my_channel").execute()

my_listener.wait_for_connect()

state = {'field_a': 'awesome', 'field_b': 10}
envelope = pubnub.set_state().channels('awesome_channel').channel_groups('awesome_channel_groups').state(state).sync()

