import logging
import re

import requests
from bs4 import BeautifulSoup, Comment
from bs4.element import Tag
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
            elem_title = soup.select_one(
                "#body-content > div.song-main-infos > div.info-zone > h2"
            )
            elem_artist = soup.select_one(
                "#body-content > div.song-main-infos > div.info-zone > ul > li:nth-child(1) > span.value > a"
            )
            elem_lyrics = soup.select_one("#pLyrics > p")
            if not elem_title or not elem_lyrics:
                return
            logger.debug(
                f"1_scrap_genie()__Scrap_Success_Elemant:{elem_title}_{elem_artist}\n{elem_lyrics}"
            )
            return {
                "title": preprocess(elem_title),
                "artist": preprocess(elem_artist) if elem_artist else "Unknown",
                "lyrics": re.sub("\n+", "\n", elem_lyrics.text.replace("\r", "\n")),
            }
        except:
            logger.error(f"1_scrap_genie()__Scrap_Fail_URL:{url}")
            logger.error(
                f"1_scrap_genie()__Scrap_Fail_Error:{elem_title}_{elem_artist}\n{elem_lyrics}"
            )
            return
    except HTTPError as e:
        logger.error(f"1_scrap_genie()__HTTP_Error:{url}\n{str(e)}")


def scrap_melon(url: str, headers):
    if "songId" not in url:
        return
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            elem_title = soup.select_one(
                "#downloadfrm > div > div > div.entry > div.info > div.song_name"
            )
            elem_artist = soup.select_one(
                "#downloadfrm > div > div > div.entry > div.info > div.artist > a > span:nth-child(1)"
            )
            elem_lyrics = soup.select_one("#d_video_summary")
            if not elem_title or not elem_lyrics:
                return
            logger.debug(
                f"2_scrap_melon()__Scrap_Success_Elemant:{elem_title}_{elem_artist}\n{elem_lyrics}"
            )
            return {
                "title": preprocess(elem_title),
                "artist": preprocess(elem_artist) if elem_artist else "Unknown",
                "lyrics": text_with_newlines(elem_lyrics),
            }
        except:
            logger.error(f"2_scrap_melon()__Scrap_Fail_URL:{url}")
            logger.error(
                f"2_scrap_melon()__Scrap_Fail_Error:{elem_title}_{elem_artist}\n{elem_lyrics}"
            )
            return
    except HTTPError as e:
        logger.error(f"2_scrap_melon()__HTTP_Error:{url}\n{str(e)}")


def scrap_bugs(url: str, headers):
    if "track" not in url:
        return
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            elem_title = soup.select_one("#container > header > div > h1")
            elem_artist = soup.select_one(
                "#container > section.sectionPadding.summaryInfo.summaryTrack > div > div.basicInfo > table > tbody > tr:nth-child(1) > td > a"
            )
            elem_lyrics = soup.select_one(
                "#container > section.sectionPadding.contents.lyrics > div > div > p:nth-child(1) > xmp"
            )
            if not elem_title or not elem_lyrics:
                return
            logger.debug(
                f"3_scrap_bugs()__Scrap_Success_Elemant:{elem_title}_{elem_artist}\n{elem_lyrics}"
            )
            return {
                "title": preprocess(elem_title),
                "artist": preprocess(elem_artist) if elem_artist else "Unknown",
                "lyrics": re.sub("\n+", "\n", elem_lyrics.text.replace("\r", "\n")),
            }
        except:
            logger.error(f"3_scrap_bugs()__Scrap_Fail_URL:{url}")
            logger.error(
                f"3_scrap_bugs()__Scrap_Fail_Error:{elem_title}_{elem_artist}\n{elem_lyrics}"
            )
            return
    except HTTPError as e:
        logger.error(f"3_scrap_bugs()__HTTP_Error:{url}\n{str(e)}")


def scrap_lyrics_site(url: str, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            elem_songInfo = soup.select_one(
                "body > div.post-details-area.mb-80 > div > div > div.col-12.col-md-12.col-lg-8 > div.post-details-content > div > div.post-content.mt-0 > a"
            )
            elem_lyrics = soup.select_one(
                'div[style="font-size: 22px;word-break:break-all;"]'
            )
            if not elem_songInfo or not elem_lyrics:
                return
            logger.debug(
                f"4_scrap_lyrics_site()__Scrap_Success_Elemant:{elem_songInfo}\n{elem_lyrics}"
            )
            return {
                "title": preprocess(elem_songInfo),
                "artist": "",
                "lyrics": text_with_newlines(elem_lyrics),
            }
        except:
            logger.error(f"4_scrap_lyrics_site()__Scrap_Fail_URL:{url}")
            logger.error(
                f"4_scrap_lyrics_site()__Scrap_Fail_Error:{elem_songInfo}\n{elem_lyrics}"
            )
            return
    except HTTPError as e:
        logger.error(f"4_scrap_lyrics_site()__HTTP_Error:{url}\n{str(e)}")


def preprocess(elemant: Tag) -> str:
    remove_html_tag(elemant)
    text = remove_bracket(elemant.text)
    return text.strip()


def text_with_newlines(elemant):
    text = ""
    # remove html comments
    for e in elemant(text=lambda text: isinstance(text, Comment)):
        e.extract()
    # replace </br> or </p> tags with line_break
    for e in elemant.descendants:
        if isinstance(e, str):
            text += e.strip()
        elif e.name == "br" or e.name == "p":
            # if previous linebreaks exists, skip appending
            if text and text[-1] != "\n":
                text += "\n"
    return text


def remove_html_tag(elemant):
    for match in elemant.findAll(["strong", "span"]):
        match.extract()


def remove_bracket(elem_title):
    return re.sub(r"\([^)]*\)", "", elem_title)