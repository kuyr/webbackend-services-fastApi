from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import oauth2
from .. import models, schemas, utils
from fastapi import  Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
   tags=["Authentication"] 
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
   if not user:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials, BFFR")
   
   if not utils.verify(user_credentials.password, user.password):
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials, BFFR")
   
   access_token = oauth2.create_access_token(data={"user_id": user.id})
   return {"access_token": access_token, "token_type": "bearer"}
