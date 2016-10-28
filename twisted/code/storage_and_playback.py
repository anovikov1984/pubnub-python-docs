import logging

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_twisted import PubNubTwisted
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

pnconfig = PNConfiguration()

pnconfig.publish_key = "pub-c-98863562-19a6-4760-bf0b-d537d1f5c582"
pnconfig.subscribe_key = "sub-c-7ba2ac4c-4836-11e6-85a4-0619f8945a4f"
pnconfig.secret_key = "sec-c-MGFkMjQxYjMtNTUxZC00YzE3LWFiZGYtNzUwMjdjNmM3NDhk"
pnconfig.auth_key = "blah"
pnconfig.enable_subscribe = False

pubnub = PubNubTwisted(pnconfig)


@inlineCallbacks
def grant():
    envelope = yield pubnub.grant().auth_keys("blah").channels("history_channel").read(True).write(True).ttl(
        0).deferred()
    print("Grant access: %r" % envelope.status.is_error())


logger = logging.getLogger("pubnub")


@inlineCallbacks
def publish500():
    for i in range(0, 500):
        envelope = yield pubnub.publish() \
            .message(['message#', i]) \
            .channel('history_channel') \
            .should_store(True) \
            .deferred()

        print("%d: %s" % (i, envelope.status.is_error()))


@inlineCallbacks
def get_all_messages(start_tt):
    envelope = yield pubnub.history() \
        .channel('history_channel') \
        .count(100) \
        .start(start_tt) \
        .deferred()

    msgs = envelope.result.messages
    start = envelope.result.start_timetoken
    end = envelope.result.end_timetoken
    count = len(msgs)

    if count > 0:
        print("%d" % count)
        print("start %d" % start)
        print("end %d" % end)

    if count == 100:
        yield get_all_messages(start)
    elif count == 0:
        pubnub.stop()

if __name__ == '__main__':
    grant()
    # get_all_messages(14759343456292767)
    pubnub.start()

