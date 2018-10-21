# coding: utf-8
import io
import asyncio
import itchat
from session import asession, chatroom
from cralwer import get_sticker_urls


async def send_image_by_url(url):
    print('开始下载 {}'.format(url))
    r = await asession.get(url, stream=True, timeout=5)
    f = io.BytesIO()
    for chunk in r.iter_content(1024):
        f.write(chunk)
    f.seek(0)
    print('开始上传 {}'.format(url))
    r = itchat.upload_file(fileDir='tmp.gif', isPicture=False, file_=f)
    try:
        chatroom.send_image(fileDir='tmp.gif', mediaId=r['MediaId'])
    except Exception as e:
        print('发送 {} 失败'.format(url), e)


async def send_image_by_urls(urls):
    await asyncio.wait([send_image_by_url(u) for u in urls])


async def send_stickers_by_query(query):
    sticker_urls = await get_sticker_urls(query)
    await send_image_by_urls(sticker_urls)


async def send_animated_stickers_by_query(query):
    sticker_urls = await get_sticker_urls(query, filetype='gif')
    await send_image_by_urls(sticker_urls)
