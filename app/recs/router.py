from fastapi import APIRouter, Depends, BackgroundTasks
from app.recs.dao import ParagraphDAO
from app.recs.schemas import SParagraph
from app.recs.rb import RBParagraph
from app.recs.recs_service import recs_service


router = APIRouter(prefix='/recs', tags=['Работа с данными клинических рекомендаций'])


@router.get("/", summary="Получить все фрагменты клинических рекомендаций", response_model=list[SParagraph])
async def get_all_paragraphs(request_body: RBParagraph = Depends()) -> list[SParagraph]:
    return await ParagraphDAO.find_all(**request_body.to_dict())


@router.get("/count", summary="Получить число фрагментов клинических рекомендаций, удовлетворяющих фильтру")
async def get_all_paragraphs(request_body: RBParagraph = Depends()) -> int:
    return await ParagraphDAO.count(**request_body.to_dict())


@router.get("/by_filter", summary="Получить один фрагмент клинических рекомендаций, удовлетворяющий фильтру", response_model=SParagraph)
async def get_paragraph_by_filter(request_body: RBParagraph = Depends()) -> list[SParagraph]:
    result = await ParagraphDAO.find_one_or_none(**request_body.to_dict())
    if result is None:
        return {'message': f'Фрагмент с указанными параметрами не найден'}
    return result


@router.post("/reload/")
async def reload_recs(background_tasks: BackgroundTasks):
    await ParagraphDAO.clear()
    background_tasks.add_task(recs_service.reload_recs)
    return {"status": "reload_started"}


@router.get("/status/")
async def get_status():
    return {
        "loading": recs_service._is_loading,
    }
