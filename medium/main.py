from fastapi import FastAPI

import auth
from routers import articles, users
from database import engine, metadata, database

metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router=articles.router)
app.include_router(router=users.router)
app.include_router(router=auth.router)
