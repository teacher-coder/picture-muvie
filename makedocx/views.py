from django.shortcuts import render
from django.http import HttpResponse

from docxtpl import DocxTemplate, RichText
from docxcompose.composer import Composer
from docx import Document as Document_compose

from .forms import LyricForm

import io


def lyrics_post(request):
    if request.method == "POST":
        form = LyricForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            artist = form.cleaned_data["artist"]
            lyrics = form.cleaned_data["lyrics"]

            lyrics_list = lyrics.split("\r\n")

            make_header(title, artist)
            master = Document_compose("output/lyrics_header.docx")
            for lyric in lyrics_list:
                doc_compose(master, title, artist, lyric)

            doc = Document_compose("output/combined.docx")
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
    else:
        form = LyricForm()
    return render(request, "html/lyrics.html", {"form": form})


def make_header(title: str, artist: str):
    doc = DocxTemplate("makedocx/templates/lyrics_header_form.docx")

    context = {
        "title": title,
        "artist": artist,
    }

    doc.render(context)
    doc.save("output/lyrics_header.docx")


def make_body(title: str, artist: str, line: str):
    doc = DocxTemplate("makedocx/templates/lyrics_body_form.docx")

    rt = reform_size(line)

    # create context dictionary
    context = {
        "title": title,
        "artist": artist,
        "lyrics": rt,
    }

    # render context into the document object
    doc.render(context)

    # save the document object as a word file
    doc.save("output/lyrics_body.docx")


def doc_compose(master: Document_compose, title: str, artist: str, lyric: str):
    composer = Composer(master)
    make_body(title, artist, lyric)

    doc2 = Document_compose("output/lyrics_body.docx")
    composer.append(doc2)
    composer.save("output/combined.docx")


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
