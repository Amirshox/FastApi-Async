from pydantic import BaseModel


class ArticleSchema(BaseModel):
    title: str
    description: str


class GetArticleSchema(ArticleSchema):
    id: int

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    username: str
    password: str


class GetUserSchema(BaseModel):
    id: int
    username: str


class LoginSchema(UserSchema):
    pass


class TokenDataSchema(BaseModel):
    username: str
