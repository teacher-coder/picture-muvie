from ninja import NinjaAPI
from ninja.errors import HttpError

from .utils.search_lyrics import get_lyrics_from_song_artist, search_song

api = NinjaAPI()


@api.get("/lyrics")
def get_lyrics(request, search: str):
    tracks = search_song(search)

    lyrics = ""
    for i, track in enumerate(tracks):
        lyrics = get_lyrics_from_song_artist(track.track_name, track.artist_name)
        if lyrics or i > 5:
            break

    if lyrics:
        return {"lyrics": lyrics}
    else:
        raise HttpError(404, f"Couldn't find the lyrics of {search}")
