import logging

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_tornado import PubNubTornado
from tornado.ioloop import IOLoop
from tornado import gen

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNubTornado(pnconfig)

logger = logging.getLogger("pubnub")


@gen.coroutine
def main():
    envelope = yield pubnub.publish()\
        .channel("my_channel")\
        .message(['hello', 'there'])\
        .should_store(True)\
        .use_post(True)\
        .future()

if __name__ == '__main__':
    IOLoop.current().run_sync(main)
