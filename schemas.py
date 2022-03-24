from pydantic import BaseModel


class ArticleScheme(BaseModel):
    title: str
    description: str


class GetArticleScheme(ArticleScheme):
    id: int

    class Config:
        orm_mode = True


class UserScheme(BaseModel):
    username: str
    password: str


class GetUserScheme(BaseModel):
    id: int
    username: str


class LoginScheme(UserScheme):
    pass


class TokenDataScheme(GetUserScheme):
    pass
