import logging
import re
import urllib.parse
from urllib.parse import unquote_plus

import requests
from django.conf import settings
from thefuzz import fuzz
from requests.exceptions import HTTPError

from .scraper import scrap_bugs, scrap_genie, scrap_lyrics_site, scrap_melon

MINIMUM_LYRICS_LENGTH = 30
QUERY_DISPLAY_SIZE = 40
SIMILARITY_SCORE_OFFSET = 60

CLIENT_ID = settings.NAVER_CLIENT_ID
CLIENT_SECRET = settings.NAVER_CLIENT_SECRET

logger = logging.getLogger(__name__)


def get_lyrics(query: str = "") -> tuple[str]:
    source, title, artist, lyrics = None, None, None, None

    lyrics_links = get_links_naver_search(query)
    if lyrics_links:
        source, title, artist, lyrics = scrap_lyrics(query, lyrics_links)

    return (source, title, artist, lyrics)


def get_links_naver_search(query: str = "") -> list[str]:
    lyrics_links = []

    encText = urllib.parse.quote(f"{query} 가사")
    url = (
        "https://openapi.naver.com/v1/search/webkr.json"
        + f"?query={encText}"
        + f"&display={QUERY_DISPLAY_SIZE}"
    )
    logger.debug(
        f"0_get_links_naver_search()__query:{unquote_plus(query, encoding='utf-8', errors='replace')}"
    )

    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        items = response.json()["items"]
        for item in items:
            lyrics_links.append(item["link"])
    except HTTPError as e:
        logger.error(f"0_get_links_naver_search()__Error_Code:{str(e)})")
    except KeyError as e:
        logger.error(f"0_get_links_naver_search()__Error_Code:{str(e)})")

    logger.debug(f"0_get_links_naver_search()__Success_lyrics_links:\n{lyrics_links}")
    return lyrics_links


def scrap_lyrics(query: str, lyrics_links: list[str]) -> tuple[str]:
    host_dict = {
        "genie": {"source": "지니뮤직", "scrap_lyrics": scrap_genie},
        "melon": {"source": "멜론", "scrap_lyrics": scrap_melon},
        "bugs": {"source": "벅스", "scrap_lyrics": scrap_bugs},
        "lyrics": {"source": "노래가사", "scrap_lyrics": scrap_lyrics_site},
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/76.0.3809.100 Version/16.2 Safari/605.1.15",
    }
    source, title, artist, lyrics = None, None, None, None

    for link in lyrics_links:
        host = get_site_host(link)
        if host and host in host_dict:
            search_data = host_dict[host]["scrap_lyrics"](link, headers)
            if not search_data or not search_data["lyrics"] or (len(search_data["lyrics"]) <= MINIMUM_LYRICS_LENGTH):
                continue

            source = host_dict[host]["source"]
            title = search_data["title"]
            artist = search_data["artist"]
            cur_score = fuzz.partial_token_set_ratio(query, title + " " + artist)
            if cur_score >= SIMILARITY_SCORE_OFFSET:
                lyrics = search_data["lyrics"]
                break

    return (source, title, artist, lyrics)


def get_site_host(link):
    p = re.compile("(?<=\.)(.*)(?=\.co)")
    result = p.search(link)
    if not result:
        return
    return result.group(1)
