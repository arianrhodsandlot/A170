# coding: utf-8
import json
from a170.session import retry_session

session = retry_session()

tags_file_name = 'fabiaoqing_tags.json'
tag_page_url_template = 'https://fabiaoqing.com/tag/index/page/{}.html'
tag_url_template = 'https://fabiaoqing.com/tag/detail/id/{}.html'


def update_tags():
    with open(tags_file_name, 'r+') as f:
        tags = []
        current_page = 1
        max_page = 294

        try:
            tags = json.load(f)
        except Exception as e:
            print(e)
            pass
        if tags:
            return

        for page in range(current_page, max_page + 1):
            current_page = page
            current_tage_page_url = tag_page_url_template.format(current_page)
            print('开始抓取', current_tage_page_url)
            r = session.get(current_tage_page_url)
            tag_links = r.html.find('.segment > a')
            for tag_link in tag_links:
                tag_id = tag_link.attrs.get('href').split('/')[-1].split('.')[0]
                tag_name = tag_link.text
                tags.append({'id': tag_id, 'name': tag_name})

        json.dump(tags, fp=f, ensure_ascii=False)


def update_tag_page_counts():
    with open(tags_file_name, 'r+') as f:
        tags = json.load(f)

    for i, tag in enumerate(tags):
        page_count = tag.get('page_count')
        if page_count:
            continue

        page_count = 1
        tag_url = tag_url_template.format(tag['id'])
        print('开始抓取', tag_url)
        r = session.get(tag_url)
        pagination_items = r.html.find('.pagination > .item')
        if pagination_items:
            pagination_items.reverse()
            for pagination_item in pagination_items:
                page_count_text = pagination_item.text.strip()
                if page_count_text.isdigit():
                    page_count = int(page_count_text)
                    break
        print('更新 {} 最大页数为 {}'.format(tag['name'], page_count))
        tag['page_count'] = page_count
        tags[i] = tag

        if i and i % 20 == 0:
            with open(tags_file_name, 'w+') as f:
                json.dump(tags, fp=f, ensure_ascii=False)

    with open(tags_file_name, 'w+') as f:
        json.dump(tags, fp=f, ensure_ascii=False)


def main():
    update_tags()
    update_tag_page_counts()


if __name__ == '__main__':
    main()
