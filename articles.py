from typing import List

from fastapi import APIRouter
from fastapi import status, HTTPException

from database import Article, database
from schemas import ArticleScheme, GetArticleScheme

router = APIRouter(
    tags=["Articles"]
)


@router.post("/articles/", status_code=status.HTTP_201_CREATED)
async def insert_article(article: ArticleScheme):
    query = Article.insert().values(title=article.title, description=article.description)
    last_record_id = await database.execute(query)
    return {**article.dict(), "id": last_record_id}


@router.get("/articles/", response_model=List[GetArticleScheme])
async def get_articles():
    query = Article.select()
    return await database.fetch_all(query=query)


@router.get("/articles/{id}/", response_model=GetArticleScheme)
async def get_article(id: int):
    query = Article.select().where(Article.c.id == id)
    article = await database.fetch_one(query=query)

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    return article


@router.put("/articles/{id}/", response_model=ArticleScheme)
async def update_article(id: int, article: ArticleScheme):
    query = Article.update().where(Article.c.id == id).values(title=article.title, description=article.description)
    await database.execute(query=query)
    return {**article.dict(), "id": id}


@router.delete("/articles/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int):
    query = Article.delete().where(Article.c.id == id)
    await database.execute(query=query)
    return {"message": "Article deleted"}