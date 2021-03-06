from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .logic import schemas
from .logic import database
from .logic import oauth2
from .logic import functions
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# sends all posts
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def send_posts(db: Session = Depends(database.get_db),
                    user_id: int = Depends(oauth2.get_current_user),
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str] = ""):
    
    return functions.retrieve_posts(db, user_id, limit, skip, search)


# sends post by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def send_post_by_id(id: int, 
                    user_id: int = Depends(oauth2.get_current_user),
                    db: Session = Depends(database.get_db)):

   return functions.retrieve_post_by_id(id, user_id, db)


# creates new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseNewPost)
def create_new_post(new_post: schemas.NewPost,
                    db: Session = Depends(database.get_db), 
                    user_id: int = Depends(oauth2.get_current_user)):
    
    return functions.save_new_post_to_db(new_post, db, user_id)


# updates post by id
@router.patch("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUpdatedPost)
def update_post_by_id(id: int, 
                    updated_post: schemas.UpdatedPost, 
                    db: Session = Depends(database.get_db),
                    user_id: int = Depends(oauth2.get_current_user)):

    return functions.save_updated_post_by_id(id, updated_post, db, user_id)


# likes a post
@router.patch("/like/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def like_post_by_id(id: int, 
                    db: Session = Depends(database.get_db),
                    user_id: int = Depends(oauth2.get_current_user)):

    return functions.save_post_like_to_db(id, db, user_id)


# deletes post by id
@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def delete_post_by_id(id: int, 
                    db: Session = Depends(database.get_db),
                    user_id: int = Depends(oauth2.get_current_user)):

    return functions.delete_post_from_db(id, db, user_id)
