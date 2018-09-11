#!/usr/bin/env python3
# coding: utf-8
import uuid
import time
import os
import random
import re
from wxpy import Bot, ensure_one, embed, SHARING, TEXT
from requests_html import HTMLSession
import urllib.request
import urllib.parse

group_name = os.environ.get('A170_GROUP_NAME', 'a170')
tmp_directory = 'tmp'
current_reply_msg = None

session = HTMLSession()
bot = Bot(console_qr=True)
group = ensure_one(bot.groups().search(group_name))


def get_sticker_name(msg):
    sticker_name = re.search('求(.*)表情', msg)
    if sticker_name:
        sticker_name = sticker_name.group(1)
        return sticker_name.strip()
    return ''


def get_sticker_urls(sticker_name):
    r = session.get('https://www.fabiaoqing.com/search/search/keyword/' + urllib.parse.quote(sticker_name))
    sticker_els = r.html.find('.searchbqppdiv .image')
    # r = session.get('https://www.doutula.com/search?keyword=' + urllib.parse.quote(sticker_name))
    # sticker_els = r.html.find('.random_picture .img-responsive')
    sticker_urls = [sticker_el.attrs.get('data-original') for sticker_el in sticker_els]
    sticker_urls = sticker_urls[:10]
    animate_sticker_urls = []
    static_sticker_urls = []
    for sticker_url in sticker_urls:
        if sticker_url.startswith('/'):
            sticker_url = 'https://www.fabiaoqing.com' + sticker_url
        ext = os.path.splitext(urllib.parse.urlparse(sticker_url).path)[1]
        if ext == '.gif':
            animate_sticker_urls.append(sticker_url)
        else:
            static_sticker_urls.append(sticker_url)
    final_stiker_urls = animate_sticker_urls + static_sticker_urls
    print('搜到{}张表情包，{}动图，{}不动图'.format(len(final_stiker_urls), len(animate_sticker_urls), len(static_sticker_urls)))
    random.shuffle(final_stiker_urls)
    return final_stiker_urls or []


def respond_stickers_with_keyword(sticker_name, count=3, silent=False):
    print('开始搜索：' + sticker_name)
    sticker_urls = get_sticker_urls(sticker_name)
    sent_count = 0
    for idx, sticker_url in enumerate(sticker_urls):
        if sent_count + 1 > count:
            return
        try:
            ext = os.path.splitext(urllib.parse.urlparse(sticker_url).path)[1]
            sticker = tmp_directory + '/' + str(uuid.uuid1()) + ext
            if not os.path.exists(tmp_directory):
                os.makedirs(tmp_directory)
            urllib.request.urlretrieve(sticker_url, sticker)
            sticker_size_in_mb = os.path.getsize(sticker) / 1024 / 1024
            if sticker_size_in_mb > 0.9:
                print('第' + str(idx + 1) + '张因大小可能超过微信限制跳过发送，原链接为 ' + sticker_url)
                continue
            print('开始发送第' + str(idx + 1) + '张，原链接为 ' + sticker_url)
            time.sleep(0.8)
            group.send_image(sticker)
            sent_count += 1
        except Exception as e:
            print('发送失败', e)
            if (e.err_code == 1205):
                print('已达到微信限制频率', e)
                if not silent:
                    group.send('我被封了，先休息会')
                return
    if not sent_count and not silent:
        group.send('我这没有{}表情'.format(sticker_name))


@bot.register(group, SHARING, False)
def reply_spam(msg):
    print('{}说：{}'.format(msg.sender.name, msg.text))
    group.send('@辛仝 逮住个发广告的')
    respond_stickers_with_keyword('发广告的', count=3)


@bot.register(group, TEXT, False)
def reply_message(msg):
    global current_reply_msg
    print('{}说：{}'.format(msg.sender.name, msg.text))
    sticker_name = get_sticker_name(msg.text)
    if not sticker_name:
        return
    if current_reply_msg:
        print('由于正在回复上一条{}，跳过回复此消息'.format(current_reply_msg.sender))
        group.send('我在找其他图，你等我发完再问')
        return
    current_reply_msg = msg
    respond_stickers_with_keyword(sticker_name)
    current_reply_msg = None


embed(shell='i')
