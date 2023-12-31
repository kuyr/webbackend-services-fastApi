from typing import List

from .. import models, schemas, oauth2
from fastapi import  Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
   prefix="/posts",
   tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute("""SELECT * FROM posts""")
   # posts = cursor.fetchall()
   # posts = db.query(models.Post).all()
   posts = db.query(models.Post).filter(models.Post.user_id == current_user).all()
   return posts

@router.get("/latest", response_model=schemas.Post)
def get_latest_post(response: Response, db: Session = Depends(get_db)):
   # cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
   # post = cursor.fetchone()
   post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
   return post
   
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
   # cursor.execute("""SELECT * FROM posts WHERE id = %s""" , (str(id),))
   # post = cursor.fetchone()
   post = db.query(models.Post).filter(models.Post.id == id).first()
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail= f"post with id: {id} not found")
   return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   """
   Creates a new post in the database.

   Parameters:
       - post: The data for the new post to be created (schemas.PostCreate).
       - db: The database session (Session).
       - user_id: The ID of the current user (int).

   Returns:
       - The newly created post (schemas.Post).

   Raises:
       - None.
   """
   # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
   # new_post = cursor.fetchone()
   # conn.commit()
   new_post = models.Post(user_id = current_user.id, **post.model_dump())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
   # deleted_post = cursor.fetchone()
   # conn.commit()
   post_query = db.query(models.Post).filter(models.Post.id == id)
   post = post_query.first()

   if post == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail= f"post with id: {id} not found")
   
   if post.user_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail= f"Not authorized to perform requested action")
   
   post_query.delete(synchronize_session=False)
   db.commit()
   return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}" ) ####response_model=schemas.Post
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
   # updated_post = cursor.fetchone()
   # conn.commit()

   post_query = db.query(models.Post).filter(models.Post.id == id)
   post = post_query.first()

   if post == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,

                          detail=f"post with id: {id} not found")
   
   if post.user_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail= f"Not authorized to perform requested action")
   post_query.update(updated_post.model_dump(), synchronize_session=False)
   db.commit()
   return post_query.first()