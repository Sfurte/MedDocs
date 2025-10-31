from fastapi import FastAPI
import os
from app.recs.router import router as router_recs


script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
path_to_json = os.path.join(parent_dir, 'recs.json')

app = FastAPI()


@app.get('/')
def home_page():
    return {'message': 'hello world'}


app.include_router(router_recs)
