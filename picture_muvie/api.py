from ninja import NinjaAPI
from .utils.search_lyrics import get_lyrics_from_search

api = NinjaAPI()

@api.get("/lyrics")
def get_lyrics(request, search):
    lyrics = get_lyrics_from_search(search)
    return {"lyrics": lyrics}

@api.post("/lyrics/download")
def download_lyrics(request):
    pass
