import re
import urllib

import itunespy
import requests
import logging
from bs4 import BeautifulSoup
from django.conf import settings
from ninja.errors import HttpError

logger = logging.getLogger(__name__)

api = settings.MUSIXMATCH_API_KEY


def get_lyrics(title, artist):
    logger.debug(f"0_get_lyrics()__title:({title})_artist:({artist})")
    tracks = search_song(f"{title} {artist}")
    logger.debug(f"1_2_search_song()__tracks:\n{tracks}")

    url = (
        get_musixmatch_url(tracks[0].track_name, tracks[0].artist_name)
        if tracks
        else None
    )
    url = get_musixmatch_url(title, artist) if not url else url
    if not url:
        return

    return scrap_lyrics(url)


def search_song(term):
    logger.debug(f"1_1_search_song()__term:({term})")
    try:
        tracks = itunespy.search_track(term)
    except LookupError:
        return None
    except ConnectionError:
        print("connection error")

    return tracks


def get_musixmatch_url(title, artist):
    pattern = r"\(feat(.*?)\)"
    title = re.sub(pattern, "", title).strip()
    url = (
        "http://api.musixmatch.com/ws/1.1/track.search?format=json&q_artist={}&q_track={}&page_size=3&page=1&s_track_rating=desc"
        "&apikey={}".format(
            urllib.parse.quote_plus(artist), urllib.parse.quote_plus(title), api
        )
    )
    logger.debug(f"2_1_get_musixmatch_url()__api_url:{url}")
    response = requests.get(url).json()
    try:
        lyrics_url = response["message"]["body"]["track_list"][0]["track"][
            "track_share_url"
        ]
    except IndexError:
        return None
    pattern = r"\?.*"
    lyrics_url = re.sub(pattern, "", lyrics_url)
    logger.debug(f"2_2_get_musixmatch_url()__lyrics_url:{lyrics_url}")
    return lyrics_url


def scrap_lyrics(lyrics_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    }
    response = requests.get(lyrics_url, headers=headers)
    html = response.text
    logger.debug(f"3_1_scrap_lyrics()__html:\n{html}")
    if html == "Unauthorized":
        raise HttpError(502, "Bad Gateway. Musixmatch not responding.")

    soup = BeautifulSoup(html, "html.parser")
    lyrics = "\n".join(
        [s.text for s in soup.select("[class] span:nth-child(3) .mxm-lyrics__content")]
    )
    logger.debug(f"3_2_scrap_lyrics()__lyrics:\n{lyrics}")
    return lyrics
