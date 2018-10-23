# coding: utf-8
import asyncio
import itchat
from .chatroom import chatroom
from .register import reply

loop = asyncio.get_event_loop()


@itchat.msg_register(itchat.content.INCOME_MSG, isGroupChat=True)
def _(msg):
    if msg.user.userName == chatroom.userName:
        loop.run_until_complete(reply(msg))


def run():
    itchat.run(blockThread=False)
