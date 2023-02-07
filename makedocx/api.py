import io

from django.http import HttpResponse
from ninja import Router
from ninja import Schema

from .service import make_doc


class Song(Schema):
    title: str
    lyrics: list[str]


router = Router()


@router.post("/")
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
            "Content-Disposition": 'attachment; filename="report.docx"',
            "Content-Type": "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
