import aiounittest
from a170.cralwer import (get_tag_from_fabiaoqing, get_sticker_urls_by_fabiaoqing_tag,
                          get_sticker_urls_from_google, get_sticker_urls)


class TestCralwer(aiounittest.AsyncTestCase):
    def test_get_tag_from_fabiaoqing(self):
        tag = get_tag_from_fabiaoqing('呵呵')
        self.assertIsNotNone(tag)

    def test_get_tag_from_fabiaoqing_none(self):
        tag = get_tag_from_fabiaoqing('asdf')
        self.assertIsNone(tag)

    async def test_get_sticker_urls_by_fabiaoqing_tag(self):
        tag = get_tag_from_fabiaoqing('水果')
        sticker_urls = await get_sticker_urls_by_fabiaoqing_tag(tag=tag, filetype=None)
        self.assertEqual(len(sticker_urls), 3)

    async def test_get_sticker_urls_by_fabiaoqing_tag_gif(self):
        tag = get_tag_from_fabiaoqing('跳舞')
        sticker_urls = await get_sticker_urls_by_fabiaoqing_tag(tag=tag, filetype='gif')
        self.assertEqual(len(sticker_urls), 3)
        for sticker_url in sticker_urls:
            self.assertTrue(sticker_url.endswith('.gif'))

    async def test_get_sticker_urls_from_google(self):
        sticker_urls = await get_sticker_urls_from_google('asdfasdf', '')
        self.assertEqual(len(sticker_urls), 3)

    async def test_get_sticker_urls_from_google_gif(self):
        sticker_urls = await get_sticker_urls_from_google('asdfasdf', 'gif')
        self.assertEqual(len(sticker_urls), 3)

    async def test_get_sticker_urls(self):
        sticker_urls = await get_sticker_urls('水果')
        self.assertEqual(len(sticker_urls), 3)

    async def test_get_sticker_urls_gif(self):
        sticker_urls = await get_sticker_urls(query='跳舞', filetype='gif')
        self.assertEqual(len(sticker_urls), 3)
        for sticker_url in sticker_urls:
            self.assertTrue(sticker_url.endswith('.gif'))
