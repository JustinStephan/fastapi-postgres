from fastapi import APIRouter, Depends, HTTPException
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

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreatePost)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Refresh to get the updated object with DB-assigned fields

    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    
    if delete_post.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id} you requested does not exist")
    delete_post.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.CreatePost)
def update_post(update_post:schemas.PostBase, id:int, db:Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post ID: {id} does not exist")
    updated_post.update(update_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return updated_post.first()