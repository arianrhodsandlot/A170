# coding: utf-8
import asyncio
import itchat
from .chatroom import chatroom
from .register import reply

supported_msg_types = [
    itchat.content.TEXT,
    itchat.content.SHARING,
    itchat.content.NOTE
]

loop = asyncio.get_event_loop()


@itchat.msg_register(supported_msg_types, isGroupChat=True)
def _(msg):
    if msg.user.userName == chatroom.userName:
        loop.run_until_complete(reply(msg))


def run():
    itchat.run(blockThread=False)
