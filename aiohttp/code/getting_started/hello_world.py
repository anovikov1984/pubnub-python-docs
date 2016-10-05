import asyncio
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNubAsyncio(pnconfig)


async def main():
    def my_publish_callback(task):
        # Check whether request successfully completed or not
        exception = task.exception()
        if exception is None:
            envelope = task.result()
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
                asyncio.ensure_future(pubnub.publish()
                                      .channel("awesomeChannel")
                                      .message("hello!!").future())\
                    .add_done_callback(my_publish_callback)
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
    await asyncio.sleep(10)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
