from fastapi import APIRouter
from app.recs.dao import ParagraphDAO
from app.recs_parser import generate_all_paragraphs


router = APIRouter(prefix='/recs', tags=['Работа с данными клинических рекомендаций'])


@router.get("/", summary="Получить все параграфы клинических рекомендаций")
async def get_all_recs():
    return await ParagraphDAO.get_all_recs()


@router.post('/reload')
async def reload_recs():
    gen = generate_all_paragraphs()
    for pg in gen:
        await ParagraphDAO.add_paragraph(pg._asdict())
