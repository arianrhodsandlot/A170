# coding: utf-8
import random
import json
import asyncio
import itchat
from threading import Thread
from .config import (STICKERS_FOR_SPAM, EVERY_REPLY_SEND_COUNT, REPLY_TEMPLATE_SPAM,
                     ANIMATED_QUERY_TYPE, GIFT_MONEY_KEYWORD, GIFT_MONEY_STICKER_QUERY)
from .logger import logger
from .chatroom import chatroom
from .messager import send_image_by_urls, send_stickers_by_query, send_animated_stickers_by_query
from .util import match_query_from_text, is_spam_msg


if not chatroom.memberList:
    chatroom.update(detailedMember=True)
chatroom_owner = chatroom.memberList[0]


async def reply_spam():
    chatroom.send(REPLY_TEMPLATE_SPAM.format(chatroom_owner.nickName))
    sticker_urls = random.sample(STICKERS_FOR_SPAM, EVERY_REPLY_SEND_COUNT)
    await send_image_by_urls(sticker_urls)


async def reply_note(msg):
    if GIFT_MONEY_KEYWORD in msg.text:
        await send_stickers_by_query(GIFT_MONEY_STICKER_QUERY)


async def reply_text(msg):
    query, query_type = match_query_from_text(msg.text)
    if not query:
        return

    if query_type == ANIMATED_QUERY_TYPE:
        await send_animated_stickers_by_query(query)
    else:
        await send_stickers_by_query(query)


def serialize_msg(msg):
    return {
        'msgId': msg.msgId,
        'createTime': msg.createTime,
        'fromUserName': msg.fromUserName,
        'toUserName': msg.toUserName,
        'msgType': msg.msgType,
        'type': msg.type,
        'text': msg.text if isinstance(msg.text, str) else '',
        'url': msg.url,
        'content': msg.content,
        'actualUserName': msg.actualUserName,
        'actualNickName': msg.actualNickName,
        'isAt': msg.isAt,
    }


def log_msg(msg):
    serialized_msg = serialize_msg(msg)
    serialized_msg_text = serialized_msg['text']

    if msg.type == itchat.content.SYSTEM:
        should_log_msg = any([serialized_msg_text, msg.content, msg.url])
        if not should_log_msg:
            return

    query, _ = match_query_from_text(serialized_msg_text)
    logger.notice(json.dumps(serialized_msg, ensure_ascii=False))
    debug_log = '{} {} {} ({})'.format(msg.actualNickName, serialized_msg_text, msg.url, msg.type)
    if query:
        logger.info(debug_log)
    else:
        logger.spam(debug_log)


async def reply(msg):
    try:
        log_msg(msg)
    except Exception as e:
        logger.critical(e)

    if is_spam_msg(msg):
        await reply_spam()
    elif msg.type == itchat.content.NOTE:
        await reply_note(msg)
    elif msg.type == itchat.content.TEXT:
        await reply_text(msg)


def sync_reply(msg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(reply(msg))
    loop.close()


def reply_in_background(msg):
    t = Thread(target=sync_reply, kwargs={'msg': msg})
    t.start()
