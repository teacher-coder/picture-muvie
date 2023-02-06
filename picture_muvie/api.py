from ninja import NinjaAPI
from ninja.errors import HttpError

from .utils.search_lyrics import get_lyrics_from_song_artist, search_song

api = NinjaAPI()


@api.get("/lyrics")
def get_lyrics(request, search: str):
    tracks = search_song(search)
    if tracks:
        lyrics = get_lyrics_from_song_artist(
            tracks[0].track_name, tracks[0].artist_name
        )
        return {"lyrics": lyrics}
    else:
        raise HttpError(404, "Couldn't find the lyrics")
