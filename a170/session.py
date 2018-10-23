# coding: utf-8
import urllib3
from urllib3.util.retry import Retry
from requests_html import AsyncHTMLSession, HTMLSession, requests

urllib3.disable_warnings()


def retry_session(retries=5, session=HTMLSession()):
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


asession = retry_session(session=AsyncHTMLSession())


def asession_get(url, params=None):
    return asession.get(url=url, params=params, timeout=3, verify=False)
