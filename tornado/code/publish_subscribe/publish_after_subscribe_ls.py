import logging
import pubnub

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_tornado import PubNubTornado, SubscribeListener
from tornado.ioloop import IOLoop

from tornado import gen

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.publish_key = "demo"
pnconfig.subscribe_key = "demo"

pubnub = PubNubTornado(pnconfig)


@gen.coroutine
def main():
    my_listener = SubscribeListener()
    pubnub.add_listener(my_listener)

    pubnub.subscribe().channels("awesomeChannel").execute()
    yield my_listener.wait_for_connect()
    print("connected")

    yield pubnub.publish().channel("awesomeChannel").message({'fieldA': 'awesome', 'fieldB': 10}).future()
    result = yield my_listener.wait_for_message_on("awesomeChannel")
    print(result.message)

    pubnub.unsubscribe().channels("awesomeChannel").execute()
    yield my_listener.wait_for_disconnect()

    print("unsubscribed")

if __name__ == '__main__':
    IOLoop.current().run_sync(main)
