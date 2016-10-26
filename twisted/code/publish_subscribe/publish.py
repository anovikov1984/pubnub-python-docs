from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_twisted import PubNubTwisted

from twisted.internet.defer import inlineCallbacks

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'

pubnub = PubNubTwisted(pnconfig)

@inlineCallbacks
def main():
    envelope = yield pubnub.publish() \
        .channel("my_channel") \
        .message(['hello', 'there']) \
        .should_store(True) \
        .use_post(True) \
        .deferred()

    print(envelope.result)

    pubnub.stop()

if __name__ == '__main__':
    main()
    pubnub.start()
