import io
import logging

from django.http import HttpResponse
from ninja import NinjaAPI, Schema
from ninja.errors import ValidationError

from .docs import make_doc
# from .utils.search_lyrics import get_lyrics
from .utils.naver_search import get_lyrics

logger = logging.getLogger(__name__)

api = NinjaAPI()


class Song(Schema):
    title: str
    lyrics: list[str]


@api.post("/makedocx")
def lyrics_post(request, song: Song):
    logger.debug(f"lyrics_post()__song:{song}")
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
            "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@api.get("/lyrics")
def search_lyrics(request, title: str):
    source, lyrics = get_lyrics(title)

    if not lyrics:
        lyrics = (
            f"{title}에 대한 검색 결과를 발견하지 못했습니다.\n다른 검색 사이트를 이용해서 복사/붙여넣기를 해주세요."
        )
    return {"source": source, "lyrics": lyrics}
