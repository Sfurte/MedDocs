from app.recs.recs_loader import recs_html_generator
from bs4 import BeautifulSoup, Tag
from app.recs.parsing_methods import plain_parsing, split_by_paragraphs, split_by_paragraphs_and_lists,\
                                     split_by_strong, split_by_headers, skip_parsing


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


gen = generate_all_paragraphs()
for pg in gen:
    print(pg)
