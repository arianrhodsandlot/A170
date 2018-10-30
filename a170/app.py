# coding: utf-8
import itchat
from .chatroom import chatroom
from .register import reply_in_background


@itchat.msg_register(itchat.content.INCOME_MSG, isGroupChat=True)
def _(msg):
    if msg.user.userName == chatroom.userName:
        reply_in_background(msg)


def run():
    itchat.run(blockThread=False)
