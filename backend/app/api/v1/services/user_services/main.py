# import os
# from typing import Annotated
# from fastapi import Body, FastAPI, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from .database import SessionLocal, engine, get_db
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from secrets import token_hex
# from fastapi import FastAPI, UploadFile
# from PyPDF2 import PdfReader
# from . import schemes, models
# from .utils import hash
# from .routers import auth, pdfs, users

# app = FastAPI()
# app.include_router(auth.router)
# app.include_router(pdfs.router)
# app.include_router(users.router)

# origins = [
#     "http://localhost:3000",  # Adjust the port if your frontend runs on a different one
#     "https://yourfrontenddomain.com",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Allows all origins from the list
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )


