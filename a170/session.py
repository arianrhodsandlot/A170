# coding: utf-8
from requests_html import AsyncHTMLSession, HTMLSession, requests

requests.urllib3.disable_warnings()


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
    return session


def get_asession():
    return retry_session(session=AsyncHTMLSession())


def asession_get(url, params=None):
    return get_asession().get(url=url, params=params, timeout=3, verify=False)
