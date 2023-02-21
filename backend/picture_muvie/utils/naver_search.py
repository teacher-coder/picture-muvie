import json
import urllib.request
import urllib.parse
import logging

from enum import Enum
from django.conf import settings
from urllib.parse import unquote_plus

from .scraper import scrap_genie, scrap_bugs, scrap_melon, scrap_lyrics_site

MINIMUM_LYRICS_LENGTH = 30

CLIENT_ID = settings.NAVER_CLIENT_ID
CLIENT_SECRET = settings.NAVER_CLIENT_SECRET

logger = logging.getLogger(__name__)


class SourceType(Enum):
    genie = ("지니뮤직", "www.genie.co.kr", scrap_genie)
    melon = ("멜론", "www.melon.com", scrap_melon)
    bugs = ("벅스", "music.bugs.co.kr", scrap_bugs)
    lyrics = ("노래가사", "www.lyrics.co.kr", scrap_lyrics_site)

    def __init__(self, site, url, func):
        self.site = site
        self.url = url

    def __call__(self, *args):
        return self.value[2](*args)


def get_lyrics(title: str = "", artist: str = "") -> tuple[str]:
    lyrics, source = None, None

    lyrics_links = get_links_naver_search(title, artist)
    if len(lyrics_links) != 0:
        source, lyrics = scrap_lyrics(lyrics_links)

    return (source, lyrics)


def get_links_naver_search(title: str = "", artist: str = "") -> list[str]:
    lyrics_links = []

    encText = urllib.parse.quote(f"{title} {artist} 가사")
    url = (
        "https://openapi.naver.com/v1/search/webkr.json"
        + f"?query={encText}"
        + "&display=20"
    )
    logger.debug(
        f"0_get_links_naver_search()__url:{unquote_plus(url, encoding='utf-8', errors='replace')}"
    )

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = json.load(response)
        items = response_body["items"]
        for item in items:
            lyrics_links.append(item["link"])
    else:
        logger.debug(f"0_get_links_naver_search()__Error_Code:{rescode})")

    logger.debug(f"0_get_links_naver_search()__Success_lyrics_links:\n{lyrics_links}")
    return lyrics_links


def scrap_lyrics(lyrics_links: list[str]) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/76.0.3809.100 Version/16.2 Safari/605.1.15",
    }
    lyrics, source = None, None

    for link in lyrics_links:
        if SourceType.bugs.url in link:
            lyrics = SourceType.bugs(link, headers)
            source = SourceType.bugs.site

        if SourceType.genie.url in link:
            lyrics = SourceType.genie(link, headers)
            source = SourceType.genie.site

        elif SourceType.melon.url in link:
            lyrics = SourceType.melon(link, headers)
            source = SourceType.melon.site

        elif SourceType.lyrics.url in link:
            lyrics = SourceType.lyrics(link, headers)
            source = SourceType.lyrics.site

        if lyrics != None and len(lyrics) > MINIMUM_LYRICS_LENGTH:
            break

    return (source, lyrics)
