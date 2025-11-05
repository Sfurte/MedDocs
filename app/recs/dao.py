from app.recs.models import Paragraph
from app.database import async_session_maker
from app.dao.base import BaseDAO


class ParagraphDAO(BaseDAO):
    model = Paragraph
