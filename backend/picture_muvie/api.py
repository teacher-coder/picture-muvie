import io

from django.http import HttpResponse
from ninja import NinjaAPI, Schema
from ninja.errors import HttpError

from .docs import make_doc
from .utils.search_lyrics import get_lyrics_from_song_artist, search_song

api = NinjaAPI()


class Song(Schema):
    title: str
    lyrics: list[str]


@api.post("/makedocx")
def lyrics_post(request, song: Song):
    title = song.title
    lyrics = song.lyrics
    doc = make_doc(title, lyrics)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return HttpResponse(
        buffer.getvalue(),
        headers={
            "Content-Disposition": "attachment",
            "Content-Type": "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


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
