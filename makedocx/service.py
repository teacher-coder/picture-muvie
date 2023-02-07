from docxtpl import DocxTemplate, RichText
from docxcompose.composer import Composer
from docx import Document


def make_header(title: str) -> Document:
    doc = DocxTemplate("makedocx/templates/lyrics_header_form.docx")

    context = {
        "title": title,
    }
    doc.render(context)
    return doc


def make_body(line: str) -> Document:
    doc = DocxTemplate("makedocx/templates/lyrics_body_form.docx")

    rt = reform_font_size(line)
    context = {
        "lyrics": rt,
    }
    doc.render(context)

    return doc


def make_doc(title: str, lyrics: list[str]) -> Document:
    master = make_header(title)
    composer = Composer(master)

    for lyric in lyrics:
        doc2 = make_body(lyric)
        composer.append(doc2)

    return master


def reform_font_size(lyric: str):
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
