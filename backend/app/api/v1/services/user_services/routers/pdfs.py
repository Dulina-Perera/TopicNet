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
from .users import get_user_by_username

router = APIRouter(
    
)

# Assume we have a folder named 'uploads' to store files
UPLOAD_DIR = r"app\routers\pdfs"

# File creation function
def create_file(db: Session, file: UploadFile, user_id: int):
    # Generate a unique file name using token_hex
    file_ext = file.filename.split('.').pop()
    file_name = f"{token_hex(6)}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Save the file to the local filesystem
    with open(file_path, "wb") as f:
        content = file.file.read()  # Reading file content
        f.write(content)

    # Save file metadata to the database
    db_file = models.File(file_name=file.filename, file_path=file_path, user_id=user_id)
    db.add(db_file)
    db.commit()

    return {"status": "File uploaded successfully!", "file_path": file_path}

@router.post("/uploadfile/{user_name}")
async def upload_user_file(user_name: str, file: UploadFile, db: Session = Depends(get_db)):
    
    user = get_user_by_username(db, user_name)
    
    if not user:   
        return {"error": "User not found"}

    user_id = user.id  
    result = create_file(db=db, file=file, user_id=user_id)
    return result

@router.post('/generate/')
async def generate_mindmap_from_pdf(file_path: Annotated[str, Body()]):

   
    # Check if the file exists
    if os.path.exists(file_path) and file_path.endswith('.pdf'):
        print("File exists and is a PDF.")
        
        # # Open and read the PDF using PyPDF2
        # reader = PdfReader(pdf_file_path)
        # number_of_pages = len(reader.pages)
        # print(f"The PDF has {number_of_pages} pages.")
        
        # Access specific pages (e.g., the first page)
        # page = reader.pages[0]
        # text = page.extract_text()
        # print(text)
    else:
        print("File not found or not a PDF.")

    return{
    "file_name": "005f605e8b76deeea52dbf1e7d477a57",
    "nodes": [
      {
        "node_id": 0,
        "parent_id": None,
        "topic": "Advanced Techniques in Cognitive Analytics for Unstructured Data Interpretation",
        "content": "The document provides an overview of Cognitive Analytics, a sophisticated technology that employs a variety of analytical methods to extract insights from extensive datasets, particularly focusing on unstructured data. It details how Cognitive Analytics integrates advanced visual perception techniques, speech recognition, decision-making frameworks, and Natural Language Processing (NLP) to effectively interpret and analyze previously underutilized information sources, including conversational logs, customer feedback, online reviews, and social media interactions. The aim is to derive meaningful insights that can inform decision-making processes, enhance understanding of consumer behavior, and leverage rich data sources for strategic advantage. The presentation titled \"Lecture 10 - Prescriptive and Cognitive Analytics\" serves as an educational resource to explore these concepts in depth."
      },
      {
        "node_id": 1,
        "parent_id": 0,
        "topic": "The Role of Cognitive Analytics in Enhancing Human Intelligence and Business Applications",
        "content": "Cognitive analytics represents a significant leap forward in data analysis, augmenting human capabilities rather than merely automating tasks as traditional AI systems do. It uncovers patterns and connections within data that simple analytics cannot, by leveraging human-like intelligence across a variety of tasks. This advanced form of analytics integrates multiple intelligent technologies such as semantics, artificial intelligence algorithms, deep learning, and machine learning."
      },
      {
        "node_id": 2,
        "parent_id": 0,
        "topic": "The Role and Impact of Cognitive Computing in Modern Business Applications",
        "content": "Cognitive computing represents a groundbreaking advancement in the field of artificial intelligence, designed to mimic human thought processes in complex decision-making. This technology leverages existing knowledge and continuously learns from new data, aiming to execute tasks traditionally performed by humans. Cognitive computing systems are crafted to solve intricate problems that were previously unattainable through static programming instructions, thus providing a significant competitive edge to businesses."
      }
    ]
  }
