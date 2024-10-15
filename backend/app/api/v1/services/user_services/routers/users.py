
import os
from typing import Annotated
from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..database import SessionLocal, engine, get_db
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from secrets import token_hex
from fastapi import FastAPI, UploadFile
from PyPDF2 import PdfReader
from .. import schemes, models
from ..utils import hash

router = APIRouter()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemes.UserCreate):
    user.password = hash(user.password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return "complete"

@router.post("/register")
def register_user(user: schemes.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)




