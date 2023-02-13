import re
import time
import urllib

import itunespy
import requests
from bs4 import BeautifulSoup
from django.conf import settings

api = settings.MUSIXMATCH_API_KEY


def get_lyrics(title, artist):
    tracks = search_song(f"{title} {artist}")

    url = get_musixmatch_url(tracks[0].track_name, tracks[0].artist_name) if tracks else None
    url = get_musixmatch_url(title, artist) if not url else url
    if not url: return

    return scrap_lyrics(url)


def search_song(term):
    try:
        tracks = itunespy.search_track(term)
    except LookupError:
        return None
    except ConnectionError:
        print("connection error")

    return tracks


def get_musixmatch_url(song, artist):
    pattern = r"\(feat(.*?)\)"
    song = re.sub(pattern, "", song).strip()
    url = (
        "http://api.musixmatch.com/ws/1.1/track.search?format=json&q_artist={}&q_track={}&page_size=3&page=1&s_track_rating=desc"
        "&apikey={}".format(
            urllib.parse.quote_plus(artist), urllib.parse.quote_plus(song), api
        )
    )
    response = requests.get(url).json()
    try:
        lyrics_url = response["message"]["body"]["track_list"][0]["track"][
            "track_share_url"
        ]
    except IndexError:
        return None
    pattern = r"\?.*"
    lyrics_url = re.sub(pattern, "", lyrics_url)
    return lyrics_url


def scrap_lyrics(lyrics_url, try_num=0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    }
    response = requests.get(lyrics_url, headers=headers)
    html = response.text
    while html == "Unauthorized":
        print("Musixmatch Internal Error")
        try_num += 1
        time.sleep(5)
        if try_num > 5:
            return
        return scrap_lyrics(lyrics_url, try_num)

    soup = BeautifulSoup(html, "html.parser")
    lyrics = "\n".join(
        [s.text for s in soup.select("[class] span:nth-child(3) .mxm-lyrics__content")]
    )
    return lyrics
