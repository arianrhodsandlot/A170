import io
import random
import aiounittest
import itchat
from collections import namedtuple
from forklift.config import STICKERS_FOR_SPAM, ANIMATED_QUERY_TYPE
from forklift.util import get_file, match_query_from_text, is_spam_msg


class TestUtil(aiounittest.AsyncTestCase):
    async def test_get_file(self):
        file = await get_file(random.choice(STICKERS_FOR_SPAM))
        self.assertIsInstance(file, io.BytesIO)

    def test_match_query_from_text(self):
        query, query_type = match_query_from_text('求水果表情')
        self.assertEqual(query, '水果')
        self.assertNotEqual(query_type, ANIMATED_QUERY_TYPE)

        query, query_type = match_query_from_text('有没有水果表情')
        self.assertEqual(query, '水果')
        self.assertNotEqual(query_type, ANIMATED_QUERY_TYPE)

        query, query_type = match_query_from_text('谁有水果表情')
        self.assertEqual(query, '水果')
        self.assertNotEqual(query_type, ANIMATED_QUERY_TYPE)

        query, query_type = match_query_from_text('有没有水果动图')
        self.assertEqual(query, '水果')
        self.assertEqual(query_type, ANIMATED_QUERY_TYPE)

    def test_is_spam_msg(self):
        Msg = namedtuple('Msg', ['type', 'text'])

        msg = Msg(type=itchat.content.SHARING, text='')
        self.assertTrue(is_spam_msg(msg))

        text = '''
        【我正在PK人气赢能量，快来为我点赞】，復·制这段描述￥VNEkbhtJMv0￥后咑閞👉手机淘宝👈或者用浏览器咑閞https://m.tb.cn/h.3846eWj 查看
        '''.strip()
        msg = Msg(type=itchat.content.TEXT, text=text)
        self.assertTrue(is_spam_msg(msg))

        msg = Msg(type=itchat.content.TEXT, text='asdfasdf')
        self.assertFalse(is_spam_msg(msg))
