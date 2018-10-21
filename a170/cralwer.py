# coding: utf-8
import json
import random
from session import asession


async def get_sticker_urls_from_google(query, filetype):
    url = 'https://www.google.com/search'
    params = {
        'q': '{} 表情包'.format(query),
        'hl': 'zh-CN',
        'gws_rd': 'cr',
        'tbm': 'isch',
        'tbs': 'ift:{}'.format(filetype) if filetype else ''
    }
    r = await asession.get(url, params=params, timeout=3, verify=False)
    tags = r.html.find('.rg_el .rg_meta')
    print('从 {} 搜索到{}个图片'.format(r.url, len(tags)))
    tags = tags[:12] or []

    sticker_urls = []
    for tag in tags:
        meta = json.loads(tag.text)
        if meta.get('ow') < 800 and meta.get('oh') < 800:
            sticker_urls.append(meta.get('ou'))

    random.shuffle(sticker_urls)
    sticker_urls = sticker_urls[:3]
    return sticker_urls


async def get_sticker_urls(query, filetype=''):
    return await get_sticker_urls_from_google(query, filetype)
