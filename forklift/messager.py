# coding: utf-8
import asyncio
import itchat
from .config import (LOG_TEMPLATE_START_SEND, LOG_TEMPLATE_SEND_FAILED,
                     LOG_TEMPLATE_UPLOAD_FAILED, LOG_TEMPLATE_DOWNLOAD_FAILED)
from .logger import logger
from .chatroom import chatroom
from .cralwer import get_sticker_urls
from .util import get_file


async def send_image_by_url(url):
    logger.verbose(LOG_TEMPLATE_START_SEND.format(url))
    try:
        f = await get_file(url)
    except Exception as e:
        logger.error(LOG_TEMPLATE_DOWNLOAD_FAILED.format(url))
        logger.error(e)
        return

    try:
        r = itchat.upload_file(fileDir='tmp.gif', isPicture=False, file_=f)
    except Exception as e:
        logger.error(LOG_TEMPLATE_UPLOAD_FAILED.format(url))
        logger.error(e)
        return

    try:
        chatroom.send_image(fileDir='tmp.gif', mediaId=r['MediaId'])
    except Exception as e:
        logger.error(LOG_TEMPLATE_SEND_FAILED.format(url))
        logger.error(e)


async def send_image_by_urls(urls):
    await asyncio.wait([send_image_by_url(u) for u in urls])


async def send_stickers_by_query(query):
    sticker_urls = await get_sticker_urls(query)
    await send_image_by_urls(sticker_urls)


async def send_animated_stickers_by_query(query):
    sticker_urls = await get_sticker_urls(query, filetype='gif')
    await send_image_by_urls(sticker_urls)
