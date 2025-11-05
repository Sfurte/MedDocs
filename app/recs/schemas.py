from pydantic import BaseModel, Field, ConfigDict


class SParagraph(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    rec_title: str = Field(..., description='Название исходного документа')
    chapter_id: str = Field(..., description='ID главы исходного документа')
    title: str = Field(..., description='Заголовок, ассоциированный с фрагментом')
    content: str = Field(..., description='Содержание фрагмента')


class SParagraphAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    rec_title: str = Field(..., description='Название исходного документа')
    chapter_id: str = Field(..., description='ID главы исходного документа')
    title: str = Field(..., description='Заголовок, ассоциированный с фрагментом')
    content: str = Field(..., description='Содержание фрагмента')
