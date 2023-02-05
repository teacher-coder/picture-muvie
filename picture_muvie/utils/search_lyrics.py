import re
import urllib

import requests
from bs4 import BeautifulSoup
from django.conf import settings
import itunespy

api = settings.MUSIXMATCH_API_KEY


def get_lyrics_from_search(term):
    tracks = search_song(term)
    if tracks:
        return get_lyrics_from_song_artist(tracks[0].track_name, tracks[0].artist_name)


def search_song(term):
    try:
        tracks = itunespy.search_track(term)
    except LookupError:
        return None
    except ConnectionError:
        print("connection error")

    return tracks

def get_lyrics_from_song_artist(song, artist):
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    }
    response = requests.get(lyrics_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    lyrics = "\n".join(
        [s.text for s in soup.select("[class] span:nth-child(3) .mxm-lyrics__content")]
    )
    return lyrics
