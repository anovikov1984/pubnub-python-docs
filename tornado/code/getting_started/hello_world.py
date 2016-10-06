from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_tornado import PubNubTornado
from tornado.ioloop import IOLoop

from tornado import gen

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNubTornado(pnconfig)


@gen.coroutine
def main():
    def my_publish_callback(future):
        # Check whether request successfully completed or not
        exception = future.exception()
        if exception is None:
            envelope = future.result()
            pass  # Message successfully published to specified channel.
        else:
            pass  # Handle message publish error. Check 'category' property to find out possible issue
            # because of which request did fail.
            # Request can be resent using: [status retry];

    class MySubscribeCallback(SubscribeCallback):
        def presence(self, pubnub, presence):
            pass  # handle incoming presence data

        def status(self, pubnub, status):
            if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass  # This event happens when radio / connectivity is lost

            elif status.category == PNStatusCategory.PNConnectedCategory:
                # Connect event. You can do stuff like publish, and know you'll get it.
                # Or just use the connected event to confirm you are subscribed for
                # UI / internal notifications, etc
                pubnub.ioloop.add_future(
                    pubnub.publish().channel("awesomeChannel").message("hello!!").future(),
                    my_publish_callback
                )
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # Happens as part of our regular operation. This event happens when
                # radio / connectivity is lost, then regained.
            elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
                pass
                # Handle message decryption error. Probably client configured to
                # encrypt messages and on live data feed it received plain text.

        def message(self, pubnub, message):
            # Handle new message stored in message.message
            pass

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels('awesomeChannel').execute()
    yield gen.sleep(10)


if __name__ == '__main__':
    IOLoop.current().run_sync(main)
