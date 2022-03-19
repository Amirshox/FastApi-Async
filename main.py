from typing import List

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from articles import models

from articles.schemas import ArticleScheme, GetArticleScheme

# models.Base.metedata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/articles/", response_model=List[GetArticleScheme])
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles


@app.post("/articles/", status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleScheme, db: Session = Depends(get_db)):
    article = models.Article(title=article.title, description=article.description)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article
