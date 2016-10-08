import logging

import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pnconfig = PNConfiguration()

pnconfig.publish_key = "pub-c-98863562-19a6-4760-bf0b-d537d1f5c582"
pnconfig.subscribe_key = "sub-c-7ba2ac4c-4836-11e6-85a4-0619f8945a4f"
pnconfig.secret_key = "sec-c-MGFkMjQxYjMtNTUxZC00YzE3LWFiZGYtNzUwMjdjNmM3NDhk"
pnconfig.auth_key = "blah"
pnconfig.enable_subscribe = False

pubnub = PubNub(pnconfig)

# envelope = pubnub.grant().auth_keys("blah").channels("history_channel").read(True).write(True).ttl(50).sync()
# print("Grant access: %r" % envelope.status.is_error())

logger = logging.getLogger("pubnub")


def publish500():
    for i in range(0, 500):
        envelope = pubnub.publish()\
            .message(['message#', i])\
            .channel('history_channel')\
            .should_store(True)\
            .sync()

        print("%d: %s" % (i, envelope.status.is_error()))


def pulling_history():
    envelope = pubnub.history()\
        .channel("history_channel")\
        .count(2)\
        .sync()

    print(envelope)


def time_interval():
    envelope = pubnub.history()\
        .channel("history_channel")\
        .count(100) \
        .start(13847168620721752)\
        .end(13847168819178600)\
        .sync()

    print(envelope)


def include_tt():
    envelope = pubnub.history()\
        .channel("history_channel")\
        .count(100) \
        .include_timetoken(True)\
        .sync()

    print(envelope)


def get_all_messages(start_tt):
    def history_callback(result, status):
        msgs = result.messages
        start = result.start_timetoken
        end = result.end_timetoken
        count = len(msgs)

        if count > 0:
            print("%d" % count)
            print("start %d" % start)
            print("end %d" % end)

        if count == 100:
            get_all_messages(start)

    pubnub.history()\
        .channel('history_channel')\
        .count(100)\
        .start(start_tt)\
        .async(history_callback)


get_all_messages(14759343456292767)
time.sleep(100)
