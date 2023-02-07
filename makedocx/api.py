import io

from django.http import HttpResponse
from ninja import Router
from ninja import Schema

from docxcompose.composer import Composer
from .service import make_header, doc_compose


class Song(Schema):
    title: str
    artist: str
    lyrics: list[str]


router = Router()


@router.post("/")
def lyrics_post(request, song: Song):
    title = song.title
    artist = song.artist
    lyrics = song.lyrics

    if "\r" in lyrics:
        lyrics_list = lyrics.split("\r\n")
    elif "\n" in lyrics:
        lyrics_list = lyrics.split("\n")
    elif "," in lyrics:
        lyrics_list = lyrics.split(",")
    else:
        lyrics_list = lyrics

    master = make_header(title, artist)
    composer = Composer(master)
    for lyric in lyrics_list:
        doc_compose(composer, title, artist, lyric)

    buffer = io.BytesIO()
    composer.save(buffer)
    buffer.seek(0)

    return HttpResponse(
        buffer.getvalue(),
        headers={
            "Content-Disposition": 'attachment; filename="report.docx"',
            "Content-Type": "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
