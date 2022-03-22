from typing import List

from fastapi import FastAPI, status

from database import engine, metadata, database, Article
from schemas import ArticleScheme, GetArticleScheme

metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/articles/", status_code=status.HTTP_201_CREATED)
async def insert_article(article: ArticleScheme):
    query = Article.insert().values(title=article.title, description=article.description)
    last_record_id = await database.execute(query)
    return {**article.dict(), "id": last_record_id}


@app.get("/articles/", response_model=List[GetArticleScheme])
async def get_articles():
    query = Article.select()
    return await database.fetch_all(query=query)
