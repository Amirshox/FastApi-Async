from typing import List

from fastapi import APIRouter, Depends
from fastapi import status, HTTPException

from passlib.hash import pbkdf2_sha256

from medium.database import User, database
from medium.schemas import UserSchema, GetUserSchema
from medium.token_ import get_current_user

router = APIRouter(tags=["Users"])


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def insert_user(user: UserSchema, current_user: UserSchema = Depends(get_current_user)):
    hashed_password = pbkdf2_sha256.hash(user.password)
    print(hashed_password, len(hashed_password))
    query = User.insert().values(username=user.username, password=hashed_password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@router.get("/users/", response_model=List[GetUserSchema])
async def get_users(current_user: UserSchema = Depends(get_current_user)):
    query = User.select()
    return await database.fetch_all(query=query)


@router.get("/users/{id}/", response_model=GetUserSchema)
async def get_user(id: int, current_user: UserSchema = Depends(get_current_user)):
    query = User.select().where(User.c.id == id)
    user = await database.fetch_one(query=query)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    return user


@router.put("/users/{id}/", response_model=UserSchema)
async def update_user(id: int, user: UserSchema, current_user: UserSchema = Depends(get_current_user)):
    query = User.update().where(User.c.id == id).values(username=user.username, password=user.password)
    await database.execute(query=query)
    return {**user.dict(), "id": id}


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, current_user: UserSchema = Depends(get_current_user)):
    query = User.delete().where(User.c.id == id)
    await database.execute(query=query)
    return {"message": "user deleted"}
