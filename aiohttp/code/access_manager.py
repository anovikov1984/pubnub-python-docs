import logging

import asyncio
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

logger = logging.getLogger("pubnub")

pnconfig = PNConfiguration()

pnconfig.publish_key = "pub-c-98863562-19a6-4760-bf0b-d537d1f5c582"
pnconfig.subscribe_key = "sub-c-7ba2ac4c-4836-11e6-85a4-0619f8945a4f"
pnconfig.secret_key = "sec-c-MGFkMjQxYjMtNTUxZC00YzE3LWFiZGYtNzUwMjdjNmM3NDhk"
pnconfig.ssl = True
# pnconfig.enable_subscribe = False

pubnub = PubNubAsyncio(pnconfig)

#
pnconfig = PNConfiguration()

# pnconfig.auth_key = "my_authkey"


async def operations_level():
    envelope = await pubnub.grant()\
        .read(False)\
        .write(False)\
        .manage(False)\
        .ttl(60)\
        .future()

    print(envelope.result)
    pubnub.stop()


async def operations_level2():
    envelope = await pubnub.revoke().future()

    print(envelope.result)
    pubnub.stop()


async def operations_level3():
    envelope = await pubnub.grant()\
        .read(True)\
        .write(False)\
        .channels('public_chat')\
        .ttl(60)\
        .future()

    print(envelope.result)
    pubnub.stop()


async def operations_level4():
    envelope = await pubnub.grant()\
        .read(True)\
        .write(True)\
        .channels('public_chat')\
        .auth_keys('authenticateduser')\
        .ttl(60)\
        .future()

    print(envelope.result)
    pubnub.stop()


async def permission_denied():
    class MyListener(SubscribeCallback):
        def presence(self, pubnub, presence):
            pass

        def message(self, pubnub, message):
            pass

        def status(self, pubnub, status):
            if status.is_error():
                if status.category == PNStatusCategory.PNAccessDeniedCategory:
                    print("handle permissions here")
                    pubnub.stop()

    my_listener = MyListener()
    pubnub.add_listener(my_listener)

    pubnub.subscribe().channels("private_chat").execute()


async def grant_channel_group():
    envelope = await pubnub.grant()\
        .manage(True)\
        .channel_groups(['cg1', 'cg2', 'cg3'])\
        .auth_keys(['key1', 'key2', 'key3'])\
        .ttl(60)\
        .future()

    pubnub.stop()
    print(envelope.result)


async def revoke_channel_group():
    envelope = await pubnub.revoke()\
        .channel_groups(['cg1', 'cg2', 'cg3'])\
        .auth_keys(['key1', 'key2', 'key3'])\
        .future()

    pubnub.stop()
    print(envelope.result)


def cipher():
    pnconfig = PNConfiguration()

    pnconfig.publish_key = "my_pub_key"
    pnconfig.subscribe_key = "my_sub_key"
    pnconfig.cipher_key = "my_cipher_key"

    pubnub = PubNubAsyncio(pnconfig)

async def sleeper():
    await asyncio.sleep(2)

func = cipher

loop = asyncio.get_event_loop()
loop.run_until_complete(func())
