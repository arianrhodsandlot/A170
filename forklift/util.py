import io
import re
import itchat
from .config import QUERY_AND_QUERY_TYPE_REG
from .session import get_asession


async def get_file(url):
    r = await get_asession().get(url, stream=True, timeout=5, verify=False)
    f = io.BytesIO()
    for chunk in r.iter_content(1024):
        f.write(chunk)
    f.seek(0)
    return f


def match_query_from_text(text):
    m = re.match(QUERY_AND_QUERY_TYPE_REG, text)
    if not m:
        return None, None
    m = m.groupdict()
    query = m.get('query', '')
    query_type = m.get('query_type', '')
    return query, query_type


def is_spam_msg(msg):
    if msg.type == itchat.content.SHARING:
        return True

    if msg.type == itchat.content.TEXT:
        if 'http://' in msg.text or 'https://' in msg.text:
            return True

    return False
