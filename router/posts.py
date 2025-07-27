from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
import schemas
import models
from database import get_db
from starlette import status

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.CreatePost])
def test_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreatePost])
def create_post(post_post:schemas.CreatePost, db:Session = Depends(get_db)):
    new_post = models.Post(**post_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh

    return [new_post]