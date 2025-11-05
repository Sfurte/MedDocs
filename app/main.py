from fastapi import FastAPI
import os
from app.recs.router import router as router_recs

app = FastAPI()


@app.get('/')
def home_page():
    return {'message': 'hello world'}


app.include_router(router_recs)
