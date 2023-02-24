import logging
import re

import requests
from bs4 import BeautifulSoup, Comment
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


def scrap_genie(url: str, headers):
    if "songInfo" not in url:
        return
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            elem = soup.select_one("#pLyrics > p")
            logger.debug(f"1_scrap_genie()__Scrap_Success_Elemant:\n{elem}")
            return re.sub("\n+", "\n", elem.text.replace("\r", "\n"))
        except:
            logger.error(f"1_scrap_genie()__Scrap_Fail_Error:\n{elem}")
            return
    except HTTPError as e:
        logger.error(f"1_scrap_genie()__HTTP_Error:{str(e)}")


def scrap_melon(url: str, headers):
    if "lyrics" not in url:
        return
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            elem = soup.select_one("#d_video_summary")
            logger.debug(f"2_scrap_melon()__Scrap_Success_Elemant:\n{elem}")
            return text_with_newlines(elem)
        except:
            logger.error(f"2_scrap_melon()__Scrap_Fail_Error:\n{elem}")
            return
    except HTTPError as e:
        logger.error(f"2_scrap_melon()__HTTP_Error:{str(e)}")


def scrap_bugs(url: str, headers):
    if "track" not in url:
        return
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            elem = soup.select_one(
                "#container > section.sectionPadding.contents.lyrics > div > div > p:nth-child(1) > xmp"
            )
            logger.debug(f"3_scrap_bugs()__Scrap_Success_Elemant:\n{elem}")
            return re.sub("\n+", "\n", elem.text.replace("\r", "\n"))
        except:
            logger.error(f"3_scrap_bugs()__Scrap_Fail_Error:\n{elem}")
            return
    except HTTPError as e:
        logger.error(f"3_scrap_bugs()__HTTP_Error:{str(e)}")


def scrap_lyrics_site(url: str, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            elem = soup.select_one('div[style="font-size: 22px;word-break:break-all;"]')
            logger.debug(f"4_scrap_lyrics_site()__Scrap_Success_Elemant:\n{elem}")
            lyrics = text_with_newlines(elem)
            return lyrics
        except:
            logger.error(f"4_scrap_lyrics_site()__Scrap_Fail_Error:\n{elem}")
            return
    except HTTPError as e:
        logger.error(f"4_scrap_lyrics_site()__HTTP_Error:{str(e)}")


def text_with_newlines(elem):
    text = ""
    # remove html comments
    for element in elem(text=lambda text: isinstance(text, Comment)):
        element.extract()
    # replace </br> or </p> tags with line_break
    for e in elem.descendants:
        if isinstance(e, Comment):
            e.extract()
        elif isinstance(e, str):
            text += e.strip()
        elif e.name == "br" or e.name == "p":
            text += "\n"
    return text
