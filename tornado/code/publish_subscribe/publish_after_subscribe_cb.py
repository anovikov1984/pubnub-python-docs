import logging
import pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_tornado import PubNubTornado
from tornado.ioloop import IOLoop
from tornado import gen

pubnub.set_stream_logger('pubnub', logging.DEBUG)

pnconfig = PNConfiguration()

pnconfig.publish_key = "demo"
pnconfig.subscribe_key = "demo"

pubnub = PubNubTornado(pnconfig)


@gen.coroutine
def main():
    def publish_callback(*args):
        pass

    class MyListener(SubscribeCallback):
        def status(self, pubnub, status):
            if status.category == PNStatusCategory.PNConnectedCategory:
                pubnub.ioloop.add_future(
                    pubnub.publish().channel("awesomeChannel").message({'fieldA': 'awesome', 'fieldB': 10}).future(),
                    publish_callback
                )

        def message(self, pubnub, message):
            pass

        def presence(self, pubnub, presence):
            pass

    my_listener = MyListener()

    pubnub.add_listener(my_listener)

    pubnub.subscribe().channels("awesomeChannel").execute()
    yield gen.sleep(10)

if __name__ == '__main__':
    IOLoop.current().run_sync(main)
