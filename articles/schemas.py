from pydantic import BaseModel


class ArticleScheme(BaseModel):
    title: str
    description: str


class GetArticleScheme(ArticleScheme):
    id: int

    class Config:
        orm_mode = True
