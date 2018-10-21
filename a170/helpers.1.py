# coding: utf-8
import json
import os
import random
import time
import urllib
from imgpy import Img
from requests_html import HTMLSession
from slugify import slugify
from tempfile import gettempdir
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def retry_session(retries, session, backoff_factor=0, status_forcelist=(500, 502, 503, 504)):
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


session = retry_session(5, HTMLSession())

if os.path.exists('tmp'):
    tempdir = 'tmp'
else:
    tempdir = gettempdir()


def get_sticker_urls_from_fabiaoqing(sticker_name, limit=10):
    if not limit:
        return []
    url = 'https://www.fabiaoqing.com/search/search/keyword/{}'.format(urllib.parse.quote(sticker_name))
    print('开始请求{}'.format(url))
    try:
        r = session.get(url, timeout=1.5)
    except Exception as e:
        print(e)
        return []
    sticker_els = r.html.find('.searchbqppdiv .image')[:limit]
    if not sticker_els:
        return []
    sticker_urls = [sticker_el.attrs.get('data-original') for sticker_el in sticker_els]
    for idx, sticker_url in enumerate(sticker_urls):
        if sticker_url.startswith('/'):
            sticker_urls[idx] = 'https://www.fabiaoqing.com' + sticker_url
    return sticker_urls


def get_sticker_urls_from_beeji(sticker_name, limit=10):
    if not limit:
        return []
    url = 'http://www.bee-ji.com/s?w={}'.format(urllib.parse.quote(sticker_name))
    print('开始请求{}'.format(url))
    try:
        r = session.get(url, timeout=1.5)
    except Exception as e:
        print(e)
        return []
    sticker_urls = r.html.find('body > script:nth-child(2)')[0].text
    sticker_urls = sticker_urls.split(';')[0]
    sticker_urls = sticker_urls.replace('__NEXT_DATA__ =', '')
    sticker_urls = json.loads(sticker_urls).get('props', {}).get('pageProps', {}).get('images', {})
    sticker_urls = ['http://image.bee-ji.com/{}?desc={}'.format(sticker_url.get('id'), urllib.parse.quote(sticker_url.get('desc'))) for sticker_url in sticker_urls]
    return sticker_urls


def get_sticker_urls_from_doutula(sticker_name, limit=10):
    if not limit:
        return []
    url = 'https://www.doutula.com/search?keyword={}'.format(urllib.parse.quote(sticker_name))
    print('开始请求{}'.format(url))
    try:
        r = session.get(url, timeout=1.5)
    except Exception as e:
        print(e)
        return []
    sticker_els = r.html.find('.random_picture .img-responsive')[:limit]
    if not sticker_els:
        return []
    sticker_urls = [sticker_el.attrs.get('data-original') for sticker_el in sticker_els]
    for idx, sticker_url in enumerate(sticker_urls):
        if sticker_url.startswith('/'):
            sticker_urls[idx] = 'https://www.doutula.com/' + sticker_url
    return sticker_urls


def get_sticker_urls_from_google(sticker_name, limit=10):
    if not limit:
        return []
    q = '{} 表情包'.format(urllib.parse.quote(sticker_name))
    url = 'https://www.google.com/search?tbs=itp%3Aanimated&tbm=isch&q={}'.format(q)
    print('开始请求{}'.format(url))
    try:
        r = session.get(url, timeout=1.5)
    except Exception as e:
        print(e)
        return []
    sticker_els = r.html.find('.rg_el .rg_meta')[:limit]
    if not sticker_els:
        return []
    sticker_urls = [json.loads(sticker_el.text).get('ou') for sticker_el in sticker_els]
    sticker_urls = [sticker_url if sticker_url.endswith('.gif') else '{}#.gif'.format(sticker_url) for sticker_url in sticker_urls]
    return sticker_urls


def get_sticker_urls_from_sogou(sticker_name, limit=10):
    if not limit:
        return []
    url = 'http://biaoqing.sogou.com/anonymous/call/tugele/getSearchForOfficial?keyword={}'.format(urllib.parse.quote(sticker_name))
    print('开始请求{}'.format(url))
    try:
        r = session.get(url, timeout=1.5)
    except Exception as e:
        print(e)
        return []
    sticker_els = r.json().get('data')[:20]
    if not sticker_els:
        return []
    sticker_urls = [sticker_el.get('url') for sticker_el in sticker_els]
    gif_sticker_urls = [sticker_url for sticker_url in sticker_urls if sticker_url.endswith('.gif')]
    if len(gif_sticker_urls) > limit:
        return gif_sticker_urls[:limit]
    normal_sticker_urls = [sticker_url for sticker_url in sticker_urls if not sticker_url.endswith('.gif')]
    sticker_urls = gif_sticker_urls + normal_sticker_urls
    return sticker_urls[:limit]


def get_sticker_urls(sticker_name, limit=20, shuffle=True):
    sticker_urls = []

    sticker_urls += get_sticker_urls_from_beeji(sticker_name, limit=12)
    if len(sticker_urls) < limit:
        print(len(sticker_urls))
        sticker_urls += get_sticker_urls_from_fabiaoqing(sticker_name, limit=8)
    if len(sticker_urls) < limit:
        print(len(sticker_urls))
        sticker_urls += get_sticker_urls_from_sogou(sticker_name, limit=6)
    if len(sticker_urls) < limit:
        print(len(sticker_urls))
        sticker_urls += get_sticker_urls_from_doutula(sticker_name, limit=6)
    if len(sticker_urls) < limit:
        print(len(sticker_urls))
        sticker_urls += get_sticker_urls_from_google(sticker_name, limit=6)

    sticker_urls = sticker_urls[:limit] or []
    if shuffle:
        random.shuffle(sticker_urls)
    return sticker_urls


def send_stickers_with_keyword_to_chat(sticker_name, chat, count=3, send_fail_message=True):
    print('开始搜索：{}'.format(sticker_name))
    sticker_urls = get_sticker_urls(sticker_name)
    sent_count = 0
    for idx, sticker_url in enumerate(sticker_urls):
        if sent_count + 1 > count:
            return
        print('开始发送第{}张，原链接为 {}'.format(idx + 1, sticker_url))
        try:
            if sticker_url.endswith('.gif'):
                ext = 'gif'
            else:
                ext = os.path.splitext(urllib.parse.urlparse(sticker_url).path)[1].lstrip('.')
            base = slugify('{}-{}-{}'.format(__name__, time.time(), sticker_name))
            sticker = '{}.{}'.format(base, ext)
            sticker = os.path.join(tempdir, sticker)
            urllib.request.urlretrieve(sticker_url, sticker)
            sticker_size_in_mb = os.path.getsize(sticker) / 1024 / 1024
            if ext == 'gif' and sticker_size_in_mb < 0.04:
                print('动图文件大小{}MB太小，质量高几率较差，跳过发送'.format(round(sticker_size_in_mb, 2)))
                continue
            with Img(fp=sticker) as im:
                w, h = im.size
                if w < 180:
                    print('图片尺寸{}×{}太小，质量高几率较差，跳过发送'.format(w, h))
                    continue
            time.sleep(0.8)
            chat.send_image(sticker)
            sent_count += 1
        except Exception as e:
            print('发送{}失败'.format(sticker), e)
            if (getattr(e, 'err_code', None) == 1205):
                print('已达到微信限制频率', e)
                if send_fail_message:
                    chat.send('我被封了，先休息会')
                return
    if sent_count == 0:
        print('未发送任何表情')
        if send_fail_message:
            chat.send('我这没有{}表情'.format(sticker_name))


def send_gif_stickers_with_keyword_to_chat(sticker_name, chat, count=3, send_fail_message=True):
    print('开始搜索：{}'.format(sticker_name))
    sticker_urls = get_sticker_urls(sticker_name, limit=240, shuffle=True)
    sent_count = 0
    sticker_urls = filter(lambda u: u.endswith('.gif'), sticker_urls)
    for idx, sticker_url in enumerate(sticker_urls):
        if sent_count + 1 > count and sticker_name != '加油':
            return
        try:
            if not sticker_url.endswith('.gif'):
                continue

            print('开始发送第{}张，原链接为 {}'.format(idx + 1, sticker_url))
            ext = 'gif'
            base = slugify('{}-{}-{}'.format(__name__, time.time(), sticker_name))
            sticker = '{}.{}'.format(base, ext)
            sticker = os.path.join(tempdir, sticker)
            urllib.request.urlretrieve(sticker_url, sticker)
            sticker_size_in_mb = os.path.getsize(sticker) / 1024 / 1024
            if ext == 'gif' and sticker_size_in_mb < 0.04:
                print('动图文件大小{}MB太小，质量高几率较差，跳过发送'.format(round(sticker_size_in_mb, 2)))
                continue
            chat.send_image(sticker)
            sent_count += 1
        except Exception as e:
            print('发送{}失败'.format(sticker), e)
            if (getattr(e, 'err_code', None) == 1205):
                print('已达到微信限制频率', e)
                if send_fail_message:
                    chat.send('我被封了，先休息会')
                return
    if sent_count == 0:
        print('未发送任何动图')
        if send_fail_message:
            chat.send('我这没有{}动图'.format(sticker_name))
