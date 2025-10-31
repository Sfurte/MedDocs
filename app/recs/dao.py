from sqlalchemy import select
from app.recs.models import Paragraph
from app.database import async_session_maker


class ParagraphDAO:
    @classmethod
    async def get_all_recs(cls):
        async with async_session_maker() as session:
            query = select(Paragraph)
            recs = await session.execute(query)
            return recs.scalars().all()

    @classmethod
    async def add_paragraph(cls, paragraph_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_paragraph = Paragraph(id=paragraph_data['id'], rec_title=paragraph_data['chapter'], chapter_id=paragraph_data['chapter_id'], chapter_title=paragraph_data['chapter_title'], chapter_content=paragraph_data['content'])
                session.add()

                await session.commit()

                return new_paragraph.id
