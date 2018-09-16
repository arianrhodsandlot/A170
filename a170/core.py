# coding: utf-8
import os
import re
import time
import urllib
from wxpy import Bot, ensure_one, embed, SHARING, TEXT
from a170.helpers import send_stickers_with_keyword_to_chat


group_name = os.environ.get('A170_GROUP_NAME', 'a170')
current_reply_msg = None

bot = Bot(console_qr=True)
group = ensure_one(bot.groups().search(group_name))


@bot.register(group, SHARING, False)
def reply_spam(msg):
    print('{}说：{}'.format(msg.sender.name, msg.text))
    group.send('@辛仝 逮住个发广告的')
    send_stickers_with_keyword_to_chat(sticker_name='发广告的', chat=group, send_fail_message=True)


@bot.register(group, TEXT, False)
def reply_stickers(msg):
    global current_reply_msg
    print('{}说：{}'.format(msg.sender.name, msg.text))
    sticker_name = re.search('求(.*)表情', msg.text)
    if sticker_name:
        sticker_name = sticker_name.group(1).strip()
    if not sticker_name:
        return
    if current_reply_msg:
        print('由于正在回复上一条{}，跳过回复此消息'.format(current_reply_msg.sender))
        return
    current_reply_msg = msg
    send_stickers_with_keyword_to_chat(sticker_name, chat=group)
    current_reply_msg = None


def run():
    embed(shell='i')
