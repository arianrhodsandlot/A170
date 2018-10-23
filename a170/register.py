# coding: utf-8
import re
import random
import itchat
from .config import STICKERS_FOR_SPAM, EVERY_REPLY_SEND_COUNT
from .logger import logger
from .chatroom import chatroom
from .messager import send_image_by_urls, send_stickers_by_query, send_animated_stickers_by_query


if not chatroom.memberList:
    chatroom.update(detailedMember=True)
chatroom_owner = chatroom.memberList[0]


async def reply_sharing(msg):
    logger.debug('{}：{} {}'.format(msg.actualNickName, msg.text, msg.url))
    chatroom.send('@{} 逮住个发广告的！'.format(chatroom_owner.nickName))
    sticker_urls = random.sample(STICKERS_FOR_SPAM, EVERY_REPLY_SEND_COUNT)
    await send_image_by_urls(sticker_urls)


async def reply_note(msg):
    if '红包' in msg.text:
        await send_stickers_by_query('谢谢老板')


current_reply_msg = None


def match_query_from_text(text):
    m = re.match(r'(求|有没有|谁有)\s*(?P<query>.+)\s*(?P<query_type>表情|动图)', text)
    if not m:
        return None, None
    m = m.groupdict()
    query = m.get('query', '')
    query_type = 'animated' if m.get('query_type') == '动图' else ''
    return query, query_type


async def reply_text(msg):
    logger.info('{}说：{}'.format(msg.actualNickName, msg.text))
    global current_reply_msg

    if current_reply_msg:
        logger.debug('由于正在回复上一条，跳过回复此消息')
        return

    current_reply_msg = msg

    query, query_type = match_query_from_text(msg.text)
    if query:
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
