import logging

import time
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

logger = logging.getLogger("pubnub")

pnconfig = PNConfiguration()

pnconfig.publish_key = "pub-c-98863562-19a6-4760-bf0b-d537d1f5c582"
pnconfig.subscribe_key = "sub-c-7ba2ac4c-4836-11e6-85a4-0619f8945a4f"
pnconfig.secret_key = "sec-c-MGFkMjQxYjMtNTUxZC00YzE3LWFiZGYtNzUwMjdjNmM3NDhk"
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

#
pnconfig = PNConfiguration()

# pnconfig.auth_key = "my_authkey"


def operations_level():
    envelope = pubnub.grant()\
        .read(False)\
        .write(False)\
        .manage(False)\
        .ttl(60)\
        .sync()

    print(envelope.result)


def operations_level2():
    envelope = pubnub.revoke().sync()

    print(envelope.result)


def operations_level3():
    envelope = pubnub.grant()\
        .read(True)\
        .write(False)\
        .channel('public_chat')\
        .ttl(60)\
        .sync()

    print(envelope.result)


def operations_level4():
    envelope = pubnub.grant()\
        .read(True)\
        .write(True)\
        .channel('public_chat')\
        .auth_keys('authenticateduser')\
        .ttl(60)\
        .sync()

    print(envelope.result)


def permission_denied():
    class MyListener(SubscribeCallback):
        def presence(self, pubnub, presence):
            pass

        def message(self, pubnub, message):
            pass

        def status(self, pubnub, status):
            if status.is_error():
                if status.category == PNStatusCategory.PNAccessDeniedCategory:
                    print("handle permissions here")

    my_listener = MyListener()
    pubnub.add_listener(my_listener)

    pubnub.subscribe().channels("private_chat").execute()


def grant_channel_group():
    envelope = pubnub.grant()\
        .manage(True)\
        .channel_groups(['cg1', 'cg2', 'cg3'])\
        .auth_keys(['key1', 'key2', 'key3'])\
        .ttl(60)\
        .sync()

    print(envelope.result)


def revoke_channel_group():
    envelope = pubnub.revoke()\
        .channel_groups(['cg1', 'cg2', 'cg3'])\
        .auth_keys(['key1', 'key2', 'key3'])\
        .sync()

    print(envelope.result)


def cipher():
    pnconfig = PNConfiguration()

    pnconfig.publish_key = "my_pub_key"
    pnconfig.subscribe_key = "my_sub_key"
    pnconfig.cipher_key = "my_cipher_key"

    pubnub = PubNub(pnconfig)

revoke_channel_group()