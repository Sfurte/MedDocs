from fastapi import FastAPI
from utils import json_to_dict_list
import os
import logging
from typing import Optional

from app.recs_parser import generate_all_paragraphs


script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
path_to_json = os.path.join(parent_dir, 'recs.json')

app = FastAPI()

logger = logging.getLogger('uvicorn')
logger.setLevel(logging.DEBUG)


@app.get('/')
def home_page():
    return {'message': 'hello world'}


@app.get('/recs')
def get_all_recs(rec_id: Optional[str] = None):
    recs = json_to_dict_list(path_to_json)
    if rec_id is None:
        return recs
    return [rec for rec in recs if rec["rec_id"] == rec_id]


@app.post('/recs/reload')
def reload_recs():
    gen = generate_all_paragraphs()
    for pg in gen:
        logger.debug(pg)
