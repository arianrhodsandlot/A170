# coding: utf-8
import re
import asyncio
import random
import itchat
from session import chatroom
from messager import (
    send_image_by_urls, send_stickers_by_query, send_animated_stickers_by_query
)


if not chatroom.memberList:
    chatroom.update(detailedMember=True)
chatroom_owner = chatroom.memberList[0]


async def reply_sharing(msg):
    print('{}：{} {}'.format(msg.actualNickName, msg.text, msg.url))
    chatroom.send('@{} 逮住个发广告的！'.format(chatroom_owner.nickName))
    sticker_urls = [
        'http://ww4.sinaimg.cn/bmiddle/6af89bc8gw1f8qr12jbhmg208c05ktrd.gif',
        'http://ww3.sinaimg.cn/bmiddle/6af89bc8gw1f8qkn6x1oog20b40b4474.gif',
        'http://ww4.sinaimg.cn/bmiddle/6af89bc8gw1f8r6bfidweg205m05owwm.gif',
        'http://ww4.sinaimg.cn/bmiddle/6af89bc8gw1f8r1cnnansj20ix0jt0t6.jpg',
        'http://ww2.sinaimg.cn/bmiddle/6af89bc8gw1f8rgjyw2nkj205i05ijr7.jpg',
        'http://ws2.sinaimg.cn/bmiddle/9150e4e5ly1ffua6th8zdj205i05i749.jpg',
        'http://wx3.sinaimg.cn/bmiddle/006APoFYly1fobpj18rnsj30dc0dcaaj.jpg',
        'http://ws1.sinaimg.cn/bmiddle/9150e4e5ly1fnrsxrym57j207806ddfy.jpg',
        'http://ww1.sinaimg.cn/bmiddle/6af89bc8gw1f8nur6xnswj209c06hdg4.jpg',
        'http://ws3.sinaimg.cn/large/9150e4e5ly1frx7a15j3hj205i05imxi.jpg',
        'http://ww3.sinaimg.cn/bmiddle/6af89bc8gw1f8spfp38vcg206y056tlk.gif',
        'http://image.bee-ji.com/59490',
        'http://image.bee-ji.com/25019',
        'http://image.bee-ji.com/59485',
    ]
    random.shuffle(sticker_urls)
    await send_image_by_urls(sticker_urls[:3])


async def reply_note(msg):
    if '红包' in msg.text:
        await send_stickers_by_query('谢谢老板')


current_reply_msg = None


def match_query_from_text(text):
    m = re.match(r'(求|有没有)\s*(?P<query>.+)\s*(?P<query_type>表情|动图)', text)
    if not m:
        return None, None
    m = m.groupdict()
    query = m.get('query', '')
    query_type = 'animated' if m.get('query_type') == '动图' else ''
    return query, query_type


async def reply_text(msg):
    print('{}说：{}'.format(msg.actualNickName, msg.text))
    global current_reply_msg

    if current_reply_msg:
        print('由于正在回复上一条，跳过回复此消息')
        return

    current_reply_msg = msg

    query, query_type = match_query_from_text(msg.text)
    if query_type == 'animated':
        await send_animated_stickers_by_query(query)
    else:
        await send_stickers_by_query(query)

    current_reply_msg = None


async def reply(msg):
    if msg.type == itchat.content.SHARING:
        await reply_sharing(msg)
    elif msg.type == itchat.content.NOTE:
        await reply_note(msg)
    elif msg.type == itchat.content.TEXT:
        await reply_text(msg)


supported_msg_types = [
    itchat.content.TEXT,
    itchat.content.SHARING,
    itchat.content.NOTE
]

loop = asyncio.get_event_loop()


@itchat.msg_register(supported_msg_types, isGroupChat=True)
def _(msg):
    if msg.user == chatroom:
        loop.run_until_complete(reply(msg))


def main():
    itchat.run(blockThread=False)
