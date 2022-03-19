from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
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


@app.get("/articles/{id}", response_model=GetArticleScheme)
def get_article(id: int, db: Session = Depends(get_db)):
    # article = db.query(models.Article).filter(models.Article.id == id).first()
    article = db.query(models.Article).get(id)
    if article:
        return article
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article Does Not Exist!")


@app.post("/articles/", status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleScheme, db: Session = Depends(get_db)):
    article = models.Article(title=article.title, description=article.description)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@app.put("/articles/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_article(id, article: ArticleScheme, db: Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).update(
        {'title': article.title, 'description': article.description}
    )
    db.commit()
    return article


@app.delete("/articles/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id, db: Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).delete(synchronize_session=False)
    db.commit()
