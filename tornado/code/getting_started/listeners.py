import logging

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNubAsyncio(pnconfig)

logger = logging.getLogger("pubnub")


# > add listener snippet
class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass
        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if status.operation == PNOperationType.PNSubscribeOperation \
                or status.operation == PNOperationType.PNUnsubscribeOperation:
            if status.category == PNStatusCategory.PNConnectedCategory:
                pass
                # This is expected for a subscribe, this means there is no error or issue whatsoever
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # This usually occurs if subscribe temporarily fails but reconnects. This means
                # there was an error but there is no longer any issue
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                pass
                # This is the expected category for an unsubscribe. This means there
                # was no error in unsubscribing from everything
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # This means that PAM does allow this client to subscribe to this
                # channel and channel group configuration. This is another explicit error
            else:
                pass
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult <link to the PNCONFIGURATION heartbeart config>
            if status.is_error():
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            pass
            # Encountered unknown status type

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def message(self, pubnub, message):
        pass  # handle incoming messages


pubnub.add_listener(MySubscribeCallback())

# > remove listener snippet
my_listener = MySubscribeCallback()

pubnub.add_listener(my_listener)

# some time later
pubnub.remove_listener(my_listener)


# > handle disconnect snippet
class HandleDisconnectsCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            # internet got lost, do some magic and call reconnect when ready
            pubnub.reconnect()
        elif status.category == PNStatusCategory.PNTimeoutCategory:
            # do some magic and call reconnect when ready
            pubnub.reconnect()
        else:
            logger.debug(status)

    def presence(self, pubnub, presence):
        pass

    def message(self, pubnub, message):
        pass

disconnect_listener = HandleDisconnectsCallback()

pubnub.add_listener(disconnect_listener)
