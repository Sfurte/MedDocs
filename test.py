import requests


BASE_URL = 'http://127.0.0.1:8000/'


def get_all_recs():
    url = BASE_URL + 'recs'
    response = requests.get(url)
    return response.json()


def get_rec_by_id(rec_id):
    url = BASE_URL + f'recs?rec_id={rec_id}'
    response = requests.get(url)
    return response.json()


rec399 = get_rec_by_id('399')
print(rec399)
