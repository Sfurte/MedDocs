from playwright.sync_api import sync_playwright, Page
import openpyxl
import os


REPORT_BUTTON_PAGE_URL = 'https://cr.minzdrav.gov.ru/clin-rec/'
VIEW_REC_URL_BASE = 'https://cr.minzdrav.gov.ru/view-cr/'
REPORT_DOWNLOAD_PATH = '../temp/recs_report.xlsx'


def download_report_xlsx(page: Page, path=REPORT_DOWNLOAD_PATH):
    page.goto(REPORT_BUTTON_PAGE_URL)
    page.wait_for_load_state('networkidle')

    with page.expect_download() as download_info:
        page.locator('button:has-text("Получить отчет")').click()
    download = download_info.value
    download.save_as(path)
    return


def read_rec_ids_from_report(path=REPORT_DOWNLOAD_PATH):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    id_column = [cell.value for cell in sheet['A']]
    return id_column[1:]


def get_rec_html(page: Page, rec_id):
    page.goto(VIEW_REC_URL_BASE + rec_id)
    page.wait_for_selector('#doc_7')

    return page.content()


def recs_html_generator(update_report=True):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        if update_report or not os.path.isfile(REPORT_DOWNLOAD_PATH):
            try:
                download_report_xlsx(page)
            except:
                print('Failed to download recommendations report')

        try:
            rec_ids = read_rec_ids_from_report()
        except:
            print('Failed to read recommendation ids from report')
            rec_ids = []

        for rec_id in rec_ids:
            try:
                html_content = get_rec_html(page, rec_id)
                yield html_content
            except:
                print(f'Failed to get clinical recommendation HTML file by id {rec_id}')
        browser.close()
