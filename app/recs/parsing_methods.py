from bs4 import BeautifulSoup, Tag
from collections import namedtuple
from typing import Callable, Generator
import re


Paragraph = namedtuple('Paragraph', ['rec_title', 'chapter_id', 'title', 'content'])
HTML_SEPARATOR = ' '


def title_and_content_for_paragraphs(func: Callable[[str], Generator]):
    def decorated(chapter_node, rec_title):
        title_node = chapter_node.select_one(f'h1')
        title = title_node.text.strip()
        chapter_id = title_node.get('id')
        content_node = chapter_node.select_one('#content')

        content_title_gen = func(content_node)
        for output in content_title_gen:
            content, sub_title = map(lambda s: s.strip() if s else '', output)
            full_title = title + '\n' + sub_title if not sub_title else title

            pg = Paragraph(rec_title, chapter_id, full_title, content)
            yield pg
    return decorated


@title_and_content_for_paragraphs
def skip_parsing(content_node: Tag):
    yield None, None


@title_and_content_for_paragraphs
def plain_parsing(content_node: Tag):
    content = content_node.get_text(separator=HTML_SEPARATOR)
    yield content, None


@title_and_content_for_paragraphs
def split_by_paragraphs(content_node: Tag):
    for p in content_node.select('p'):
        content = p.get_text(separator=HTML_SEPARATOR)
        yield content, None


@title_and_content_for_paragraphs
def split_by_paragraphs_and_lists(content_node: Tag):
    pg_nodes = [node for node in content_node.select('div > p, div > ul, div > ol')]
    i = 0
    while i < len(pg_nodes):
        if i + 1 < len(pg_nodes) and pg_nodes[i + 1].name in ['ul', 'ol']:
            content = '\n'.join([node.get_text(separator=HTML_SEPARATOR) for node in pg_nodes[i:i + 1]])
            yield content, None
            i += 1
        else:
            content = pg_nodes[i].get_text(separator=HTML_SEPARATOR)
            yield content, None
        i += 1


@title_and_content_for_paragraphs
def split_by_strong(content_node: Tag):
    content_raw = str(content_node)
    for raw_pg in re.findall(r'(?:<strong>|^).*?(?=<strong>|$)', content_raw):
        pg_soup = BeautifulSoup(raw_pg, features='lxml')
        content = pg_soup.get_text(separator=HTML_SEPARATOR)
        yield content, None


@title_and_content_for_paragraphs
def split_by_headers(content_node: Tag):
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
            full_title = '\n'.join([h1_title, h2_title])
            yield subpart.text, full_title
