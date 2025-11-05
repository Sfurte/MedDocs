from app.recs.recs_loader import recs_html_generator
from bs4 import BeautifulSoup, Tag
from collections import namedtuple
import re


Paragraph = namedtuple('Paragraph', ['rec_title', 'chapter_id', 'title', 'content'])


def skip_parsing(chapter_node: Tag, rec_title: str):
    return None


def plain_parsing(chapter_node: Tag, rec_title: str):
    title_node = chapter_node.select_one(f'h1')
    title = title_node.text
    chapter_id = title_node.get('id')
    content_node = chapter_node.select_one('#content')
    content = content_node.get_text(separator='\n', strip=True)

    pg = Paragraph(rec_title, chapter_id, title, content)
    yield pg


def split_by_paragraphs(chapter_node: Tag, rec_title: str):
    title_node = chapter_node.select_one(f'h1')
    title = title_node.text
    chapter_id = title_node.get('id')
    content_node = chapter_node.select_one('#content')

    for p in content_node.select('p'):
        content = p.get_text(separator=' ', strip=True)
        pg = Paragraph(rec_title, chapter_id, title, content)
        yield pg


def split_by_paragraphs_and_lists(chapter_node: Tag, rec_title: str):
    title_node = chapter_node.select_one('h1')
    title = title_node.text
    chapter_id = title_node.get('id')
    content_node = chapter_node.select_one('#content')

    pg_nodes = [node for node in content_node.select('div > p, div > ul, div > ol')]
    contents = []
    i = 0
    while i < len(pg_nodes):
        if i + 1 < len(pg_nodes) and pg_nodes[i + 1].name in ['ul', 'ol']:
            contents.append(pg_nodes[i].get_text(separator='\n', strip=True) + '\n' + pg_nodes[i + 1].get_text(separator='\n', strip=True))
            i += 1
        else:
            contents.append(pg_nodes[i].get_text(separator='\n', strip=True))
        i += 1

    for content in contents:
        pg = Paragraph(rec_title, chapter_id, title, content)
        yield pg


def split_by_strong(chapter_node: Tag, rec_title: str):
    title_node = chapter_node.select_one(f'h1')
    title = title_node.text
    chapter_id = title_node.get('id')
    content_node = chapter_node.select_one('#content')

    content_raw = str(content_node)
    for raw_pg in re.findall(r'(?:<strong>|^).*?(?=<strong>|$)', content_raw):
        pg_soup = BeautifulSoup(raw_pg, features='lxml')
        pg = Paragraph(rec_title, chapter_id, title, pg_soup.get_text(separator='\n', strip=True))
        yield pg


def split_by_headers(chapter_node: Tag, rec_title: str):
    title_node = chapter_node.select_one(f'h1')
    title = title_node.text
    chapter_id = title_node.get('id')
    content_node = chapter_node.select_one('#content')

    def split_by_header(tag, header):
        tag_raw = str(tag)
        for raw_part in re.findall(rf'(?:<{header}>|^).*?(?=<{header}>|$)', tag_raw):
            yield BeautifulSoup(raw_part, features='lxml')

    for part in split_by_header(content_node, 'h1'):
        h1_header = part.select_one('h1')
        h1_title = h1_header.text if h1_header is not None else ''

        for subpart in split_by_header(part, 'h2'):
            h2_header = subpart.select_one('h2')
            h2_title = h2_header.text if h2_header is not None else ''
            full_title = '\n'.join([title, h1_title, h2_title])
            pg = Paragraph(rec_title, chapter_id, full_title, subpart.text)
            yield pg


PROCESSING_METHODS_FOR_CHAPTER_IDS = {
    'doc_abbreviation': plain_parsing,
    'doc_terms': split_by_paragraphs,
    'doc_1': skip_parsing,
    'doc_crat_info_1_1': split_by_paragraphs,
    'doc_crat_info_1_2': split_by_paragraphs_and_lists,
    'doc_crat_info_1_3': split_by_paragraphs_and_lists,
    'doc_crat_info_1_4': plain_parsing,
    'doc_crat_info_1_5': split_by_strong,
    'doc_crat_info_1_6': split_by_strong,
    'doc_diag_2': split_by_strong,
    'doc_diag_2_1': split_by_strong,
    'doc_diag_2_2': split_by_strong,
    'doc_diag_2_3': split_by_strong,
    'doc_diag_2_4': split_by_strong,
    'doc_diag_2_5': split_by_strong,
    'doc_3': split_by_headers,
    'doc_4': split_by_headers,
    'doc_5': split_by_headers,
    'doc_6': split_by_headers,
    'doc_7': split_by_headers,
}


def generate_paragraphs_from_html(rec_html):
    soup = BeautifulSoup(rec_html, features='lxml')
    title_node = soup.select_one('.title_content')
    rec_title = title_node.text

    for chapter_id, paragraph_gen_func in PROCESSING_METHODS_FOR_CHAPTER_IDS.items():
        chapter_node = soup.select_one(f'#{chapter_id}').parent.parent

        paragraph_gen = paragraph_gen_func(chapter_node, rec_title)
        if paragraph_gen is None:
            continue
        for pg in paragraph_gen:
            yield pg


def generate_all_paragraphs():
    html_gen = recs_html_generator(update_report=False)
    for html in html_gen:
        try:
            pg_gen = generate_paragraphs_from_html(html)
        except:
            print('Failed to generate paragraphs from html')
            continue
        for pg in pg_gen:
            yield pg._asdict()


#gen = generate_all_paragraphs()
#async for pg in gen:
#    print(f'SParagraph: ')
#    print(f'recommendation_title: {pg.rec_title}')
#    print(f'chapter_id: {pg.chapter_id}')
#    print(f'chapter_title: {pg.chapter_title}')
#    print(f'content: {pg.content}')
