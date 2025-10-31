from recs_loader import recs_html_generator
from bs4 import BeautifulSoup, Tag
from collections import namedtuple


Paragraph = namedtuple('Paragraph', ['rec_title', 'chapter_id', 'chapter_title', 'content'])


def plain_parsing(chapter_node: Tag, rec_title: str):
    title_node = chapter_node.select_one(f'h1')
    title = title_node.text
    chapter_id = title_node.get('id')
    content_node = chapter_node.select_one('#content')
    content = content_node.text

    pg = Paragraph(rec_title, chapter_id, title, content)
    yield pg


PROCESSING_METHODS_FOR_CHAPTER_IDS = {
    'doc_abbreviation': plain_parsing,
    'doc_terms': plain_parsing,
    'doc_1': plain_parsing,
    'doc_crat_info_1_1': plain_parsing,
    'doc_crat_info_1_2': plain_parsing,
    'doc_crat_info_1_3': plain_parsing,
    'doc_crat_info_1_4': plain_parsing,
    'doc_crat_info_1_5': plain_parsing,
    'doc_crat_info_1_6': plain_parsing,
    'doc_diag_2': plain_parsing,
    'doc_diag_2_1': plain_parsing,
    'doc_diag_2_2': plain_parsing,
    'doc_diag_2_3': plain_parsing,
    'doc_diag_2_4': plain_parsing,
    'doc_diag_2_5': plain_parsing,
    'doc_3': plain_parsing,
    'doc_4': plain_parsing,
    'doc_5': plain_parsing,
    'doc_6': plain_parsing,
    'doc_7': plain_parsing,
}


def generate_paragraph_from_html(rec_html):
    soup = BeautifulSoup(rec_html)
    title_node = soup.select_one('.title_content')
    rec_title = title_node.text

    for chapter_id, paragraph_gen_func in PROCESSING_METHODS_FOR_CHAPTER_IDS.items():
        chapter_node = soup.select_one(f'#{chapter_id}').parent.parent

        paragraph_gen = paragraph_gen_func(chapter_node, rec_title)
        for pg in paragraph_gen:
            yield pg


def generate_all_paragraphs():
    html_gen = recs_html_generator(update_report=False)
    for html in html_gen:
        pg_gen = generate_paragraph_from_html(html)
        for pg in pg_gen:
            yield pg



