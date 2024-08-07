from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SenssionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username: str
    fullname: str
    age: int


def get_db():
    db = SenssionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    isExist = db.query(models.User).filter(
        models.User.username == user.username).first()
    if isExist is not None:
        raise HTTPException(status_code=404, detail="User exist.")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all_user(db: db_dependency, page: int = 1, limit: int = 3):
    result = db.query(models.User).offset((page-1)*limit).limit(limit).all()
    return result


@app.get("/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found.')
    return user


@app.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: db_dependency):
    result = db.query(models.User).filter(models.User.id == user_id).update({
        models.User.username: user.username,
        models.User.fullname: user.fullname,
        models.User.age: user.age,
    })

    if result == 0:
        raise HTTPException(status_code=404, detail='User not found.')
    db.commit()


@app.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found.')
    db.delete(user)
    db.commit()
