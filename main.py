from typing import List

from fastapi import FastAPI, Depends, status, HTTPException

from database import engine, metadata, database

from articles import models
from articles.schemas import ArticleScheme, GetArticleScheme

metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
