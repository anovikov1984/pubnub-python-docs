from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_twisted import PubNubTwisted

def main():
    pnconfig = PNConfiguration()

    pnconfig.publish_key = "demo"
    pnconfig.subscribe_key = "demo"

    pubnub = PubNubTwisted(pnconfig)

    def publish_callback(envelope):
        print('Publish Callback!')
        pubnub.stop()

    class MyListener(SubscribeCallback):
        def status(self, pubnub, status):
            if status.category == PNStatusCategory.PNConnectedCategory:
                d = pubnub.publish().channel("awesomeChannel").message({'fieldA': 'awesome', 'fieldB': 10}).deferred()
                d.addCallback(publish_callback)

        def message(self, pubnub, message):
            pass

        def presence(self, pubnub, presence):
            pass

    my_listener = MyListener()
    pubnub.add_listener(my_listener)
    pubnub.subscribe().channels("awesomeChannel").execute()
    pubnub.start()

if __name__ == '__main__':
    main()
