import requests
import json
import urllib.request
import urllib.parse
import logging

from bs4 import BeautifulSoup
from django.conf import settings
from urllib.parse import unquote_plus

logger = logging.getLogger(__name__)

MINIMUM_LYRICS_LENGTH = 30

CLIENT_ID = settings.NAVER_CLIENT_ID
CLIENT_SECRET = settings.NAVER_CLIENT_SECRET


def get_lyrics(title: str = None, artist: str = None) -> str:
    lyrics_links = get_links_naver_search(title, artist)

    if len(lyrics_links) == 0:
        return

    return scrap_lyrics(lyrics_links)


def get_links_naver_search(title: str = None, artist: str = None) -> list[str]:
    lyrics_links = []

    if title is None:
        title = ""
    if artist is None:
        artist = ""
    encText = urllib.parse.quote(f"{title} {artist} 가사")
    url = (
        "https://openapi.naver.com/v1/search/webkr.json"
        + f"?query={encText}"
        + "&display=20"
    )
    logger.debug(f"0_get_links_naver_search()__url:{unquote_plus(url, encoding='utf-8', errors='replace')}")

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

    for url in lyrics_links:
        if "genie" in url:
            lyrics = scrap_genie(url, headers)
        elif "melon" in url:
            lyrics = scrap_melon(url, headers)
        elif "bugs" in url:
            lyrics = scrap_bugs(url, headers)
        elif "lyrics.co.kr" in url:
            lyrics = scrap_lyrics_site(url, headers)
        else:
            lyrics = None

        if lyrics != None and len(lyrics) > MINIMUM_LYRICS_LENGTH:
            return lyrics
    return


def scrap_genie(url: str, headers):
    if "songInfo" in url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            try:
                elem = soup.select_one("#pLyrics > p")
                logger.debug(f"1_scrap_genie()__Success_Elemant:\n{elem}")
                return elem.get_text()
            except:
                return
        logger.debug(f"1_scrap_genie()__Error_Code:{response.status_code}")
    else:
        return


def scrap_melon(url: str, headers):
    if "lyrics" in url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            try:
                elem = soup.select_one("#d_video_summary")
                logger.debug(f"2_scrap_melon()__Success_Elemant:\n{elem}")
                return elem.get_text()
            except:
                return
        logger.debug(f"2_scrap_melon()__Error_Code:{response.status_code}")
    else:
        return


def scrap_bugs(url: str, headers):
    if "track" in url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            try:
                elem = soup.select_one(
                    "#container > section.sectionPadding.contents.lyrics > div > div > p:nth-child(1) > xmp"
                )
                logger.debug(f"3_scrap_bugs()__Success_Elemant:\n{elem}")
                return elem.get_text()
            except:
                return
        logger.debug(f"3_scrap_bugs()__Error_Code:{response.status_code}")
    else:
        return


def scrap_lyrics_site(url: str, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            elem = soup.select_one('div[style="font-size: 22px;word-break:break-all;"]')
            logger.debug(f"4_scrap_lyrics_site()__Success_Elemant:\n{elem}")
            lyrics = text_with_newlines(elem)
            return lyrics
        except:
            return
    logger.debug(f"4_scrap_lyrics_site()__Error_Code:{response.status_code}")


def text_with_newlines(elem):
    text = ""
    for e in elem.descendants:
        if isinstance(e, str):
            text += e.strip()
        elif e.name == "br" or e.name == "p":
            text += "\n"
    return text
