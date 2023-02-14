from docx import Document
from docx.enum.section import WD_ORIENTATION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.text.paragraph import Paragraph
from docx.shared import Mm, Pt

from docxtpl import DocxTemplate

def make_a4_landscape_section(doc : Document) -> Document:
    sections = doc.sections
    section = sections[1]
    # a4 size in 'mm' unit
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    # portrait -> landscape
    section.page_width, section.page_height = section.page_height, section.page_width
    section.orientation = WD_ORIENTATION.LANDSCAPE
    # margin setting
    section.top_margin = Mm(165)
    section.bottom_margin = Mm(15)
    section.left_margin = Mm(25)
    section.right_margin = Mm(25)


# def isHangeul(ch) -> bool:
#     JAMO_START_LETTER = 44032
#     JAMO_END_LETTER = 55203
#     return ord(ch) >= JAMO_START_LETTER and ord(ch) <= JAMO_END_LETTER

# def isAlphabet(ch) -> bool:
#     UPPER_A_LETTER = 65
#     UPPER_Z_LETTER = 90
#     LOWER_A_LETTER = 97
#     LOWER_Z_LETTER = 122
#     return (ord(ch) >= UPPER_A_LETTER and ord(ch) <= UPPER_Z_LETTER) or (ord(ch) >= LOWER_A_LETTER and ord(ch) <= LOWER_Z_LETTER)

# def isSpace(ch) -> bool:
#     return ord(ch) == 32

# def count_lyric_language(lyric : str) -> dict:
#     chr_dict = {'alphabet':0, 'hangeul':0, 'space':0, 'special':0}
#     for c in lyric:
#         if isAlphabet(c):
#             chr_dict['alphabet'] += 1
#         elif isHangeul(c):
#             chr_dict['hangeul'] += 1
#         elif isSpace(c):
#             chr_dict['space'] += 1
#         else:
#             chr_dict['special'] += 1
    
#     return chr_dict


def add_formatted_lyric(paragraph : Paragraph, lyric : str):
    run = paragraph.add_run(lyric)
    run.bold = True
    font = run.font
    font.name = 'malgun gothic'
    font.size = Pt(45)

    # chr_dict = count_lyric_language(lyric)

    # lyric_length = int(chr_dict['alphabet'] * 0.4 + chr_dict['hangeul'] + chr_dict['space'] * 0.7 + chr_dict['special'] * 0.3)

    # length = lyric_length
    # if length > 25:
    #     font.size = Pt(20)
    # elif length > 20:
    #     font.size = Pt(25)
    # elif length > 15:
    #     font.size = Pt(30)
    # elif length > 10:
    #     font.size = Pt(40)
    # else:
    #     font.size = Pt(50)


def make_doc_title(doc : Document, title : str):
    # paragraph = doc.add_paragraph()
    # paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    context = {
        "title": title,
        "school": "서울묘곡초등학교",
        "class": "6학년 5반",
    }
    doc.render(context)


def make_doc(title : str, lyrics : list[str]) -> Document:
    doc = DocxTemplate("./picture_muvie/templates/title.docx")
    make_doc_title(doc, title)
    doc.add_section()
    make_a4_landscape_section(doc)

    for i in range(len(lyrics)):
        # doc.sections[i + 1].footer.is_linked_to_previous = False
        paragraph = doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        add_formatted_lyric(paragraph, lyrics[i])
        if i < len(lyrics) - 1:
            doc.add_section()
    return doc