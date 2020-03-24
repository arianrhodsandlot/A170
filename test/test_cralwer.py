import aiounittest
from forklift.cralwer import (get_tag_from_fabiaoqing, get_sticker_urls_by_fabiaoqing_tag,
                          get_sticker_urls_from_google, get_sticker_urls)


class TestCralwer(aiounittest.AsyncTestCase):
    async def test_get_sticker_urls_from_google(self):
        sticker_urls = await get_sticker_urls_from_google('百度', '')
        self.assertEqual(len(sticker_urls), 3)

        sticker_urls = await get_sticker_urls_from_google('百度', 'gif')
        self.assertEqual(len(sticker_urls), 3)

    async def test_get_sticker_urls(self):
        sticker_urls = await get_sticker_urls('水果')
        self.assertEqual(len(sticker_urls), 3)

        sticker_urls = await get_sticker_urls(query='跳舞', filetype='gif')
        self.assertEqual(len(sticker_urls), 3)
        for sticker_url in sticker_urls:
            self.assertTrue(sticker_url.endswith('.gif'))
