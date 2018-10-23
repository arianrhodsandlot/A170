# coding: utf-8
import json
import random
from os import path
from .config import EVERY_REPLY_SEND_COUNT
from .logger import logger
from .session import asession_get
from .assets.fabiaoqing.updater import tags_file_name, tag_url_template

fabiaoqing_tags = []
fabiaoqing_tags_file_path = path.join('a170/assets/fabiaoqing', tags_file_name)
with open(fabiaoqing_tags_file_path) as f:
    fabiaoqing_tags = json.load(f)


def get_tag_from_fabiaoqing(query):
    for tag in fabiaoqing_tags:
        if query == tag['name']:
            return tag


async def get_sticker_urls_by_fabiaoqing_tag(tag, filetype):
    page = 1
    page_count = tag['page_count']
    if page_count > 2:
        page = random.randint(page, page_count - 1)
    url = tag_url_template.format(tag['id'], page)
    r = await asession_get(url)
    sticker_urls = [sticker_el.attrs.get('data-original') for sticker_el in r.html.find('.tagbqppdiv .image')]
    if filetype:
        sticker_urls = [u for u in sticker_urls if u.endswith('.{}'.format(filetype))]
    logger.debug('从 {} 搜索到{}个图片'.format(r.url, len(sticker_urls)))
    if len(sticker_urls) < 10:
        logger.debug('数量太少跳过')
        return []

    sticker_urls = random.sample(sticker_urls, EVERY_REPLY_SEND_COUNT)
    return sticker_urls


async def get_sticker_urls_from_google(query, filetype):
    url = 'https://www.google.com/search'
    params = {
        'q': '{} 表情包'.format(query),
        'hl': 'zh-CN',
        'gws_rd': 'cr',
        'tbm': 'isch',
        'tbs': 'ift:{}'.format(filetype) if filetype else None
    }
    r = await asession_get(url, params=params)
    tags = r.html.find('.rg_el .rg_meta')
    logger.debug('从 {} 搜索到{}个图片'.format(r.url, len(tags)))

    sticker_urls = []
    for tag in tags:
        meta = json.loads(tag.text)
        if meta.get('ow') < 700 and meta.get('oh') < 700:
            sticker_urls.append(meta.get('ou'))

    sticker_urls = sticker_urls[:15]
    sticker_urls = random.sample(sticker_urls, EVERY_REPLY_SEND_COUNT)

    return sticker_urls


async def get_sticker_urls(query, filetype=None):
    sticker_urls = []

    tag = get_tag_from_fabiaoqing(query)
    if tag:
        try:
            sticker_urls = await get_sticker_urls_by_fabiaoqing_tag(tag, filetype)
        except Exception as e:
            logger.error(e)

    if not sticker_urls:
        sticker_urls = await get_sticker_urls_from_google(query, filetype)

    return sticker_urls
