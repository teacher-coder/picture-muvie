from docxtpl import DocxTemplate, RichText
from docxcompose.composer import Composer
from docx import Document


def make_header(title: str, artist: str) -> Document:
    doc = DocxTemplate("makedocx/templates/lyrics_header_form.docx")

    context = {
        "title": title,
        "artist": artist,
    }

    doc.render(context)

    return doc


def make_body(title: str, artist: str, line: str) -> Document:
    doc = DocxTemplate("makedocx/templates/lyrics_body_form.docx")

    rt = reform_size(line)

    context = {
        "title": title,
        "artist": artist,
        "lyrics": rt,
    }
    doc.render(context)

    return doc


def doc_compose(composer: Composer, title: str, artist: str, lyric: str) -> Composer:
    doc2 = make_body(title, artist, lyric)
    composer.append(doc2)


def reform_size(lyric: str):
    rt = RichText()
    lyric.strip()

    length = len(lyric)
    if length > 30:
        rt.add(lyric, size=50)
    elif length > 20:
        rt.add(lyric, size=65)
        rt.add("\n", size=10)
    else:
        rt.add(lyric, size=75)
        rt.add("\n", size=10)

    return rt
