# coding: utf-8
from requests_html import AsyncHTMLSession, HTMLSession, requests


def retry_session(retries=5, session=HTMLSession()):
    retry = requests.urllib3.util.retry.Retry(
        total=retries,
        read=retries,
        connect=retries,
        status_forcelist=(500, 502, 503, 504),
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    requests.urllib3.disable_warnings()
    return session


def get_asession():
    return retry_session(session=AsyncHTMLSession())


def asession_get(url, params=None):
    ua = 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+'
    return get_asession().get(url=url, params=params, timeout=3, verify=False, headers={'user-agent': ua})
