import logging

from django.http import HttpResponse
from ninja import NinjaAPI, Schema

from .docs import make_picmuvie_doc
from .utils.naver_search import get_lyrics

logger = logging.getLogger(__name__)

api = NinjaAPI()


class Song(Schema):
    title: str
    lyrics: list[str]


@api.post("/makedocx")
def lyrics_post(request, song: Song):
    logger.debug(f"lyrics_post()__song:{song}")
    picmuvie_doc = make_picmuvie_doc(song)

    return HttpResponse(
        picmuvie_doc,
        headers={
            "Content-Disposition": 'attachment; filename="report.docx"',
            "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@api.get("/lyrics")
def search_lyrics(request, query: str):
    source, title, artist, lyrics = get_lyrics(query)
    if not lyrics:
        lyrics = f"{query}에 대한 검색 결과를 발견하지 못했습니다.\n다른 검색 사이트를 이용해서 복사/붙여넣기를 해주세요."
    return {
        "source": source,
        "title": title,
        "artist": artist,
        "lyrics": lyrics
    }
