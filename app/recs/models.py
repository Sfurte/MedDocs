from sqlalchemy import ForeignKey, text, Text, Integer
from sqlalchemy.orm import relationship, Mapped
from app.database import Base, int_pk
from datetime import date


class Paragraph(Base):
    id: Mapped[int_pk]
    rec_title: Mapped[str]
    chapter_id: Mapped[str]
    title: Mapped[str]
    content: Mapped[str]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"rec_title={self.rec_title!r},"
                f"chapter_title={self.chapter_title!r})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'rec_title': self.rec_title,
            'chapter_id': self.chapter_id,
            'title': self.title,
            'content': self.content
        }
