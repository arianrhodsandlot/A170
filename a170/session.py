# coding: utf-8
import os
import itchat
from urllib3.util.retry import Retry
from requests_html import AsyncHTMLSession, requests

chatroom_name = os.getenv('A170_CHATROOM_NAME', 'a170')


def retry_session(session, retries):
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=0,
        status_forcelist=(500, 502, 503, 504),
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


asession = retry_session(session=AsyncHTMLSession(), retries=5)

itchat.auto_login(enableCmdQR=2, hotReload=True)
chatroom = itchat.search_chatrooms(chatroom_name)[0]
