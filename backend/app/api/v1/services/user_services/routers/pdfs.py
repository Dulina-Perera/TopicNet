import os
from typing import Annotated, List
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
  
  
@router.get("/pdfs/{username}", response_model=List[schemes.PdfResponce])
def get_pdfs(username: str,db:Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.username == username).first() 
  if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Index not found."
        )
  pdfs = db.query(models.File).filter(models.File.user_id == user.id).all()
  for pdf in pdfs:
    print(pdf.file_name)
  if not pdfs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Index not found."
        )
  return pdfs


@router.get("/mindmaps/{id}")
def get_post(id: int, db:Session = Depends(get_db)):
    mindmap = db.query(models.JSONModel).filter(models.JSONModel.pdf_id == id).first()
    if not mindmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Index not found."
        )
    return mindmap
  
@router.post("/uploadfile/{user_name}")
async def upload_user_file(user_name: str, file: UploadFile, db: Session = Depends(get_db)):
    
    user = get_user_by_username(db, user_name)
    
    if not user:   
        return {"error": "User not found"}

    user_id = user.id  
    result = create_file(db=db, file=file, user_id=user_id)
    return result

@router.post('/generate')
async def generate_mindmap_from_pdf(file_path: Annotated[str, Body()], db: Session = Depends(get_db)):

   
    # Check if the file exists
    if os.path.exists(file_path) and file_path.endswith('.pdf'):
        print("File exists and is a PDF.")
        file = db.query(models.File).filter(models.File.file_path == file_path).first()
        mindmap = db.query(models.JSONModel).filter(models.JSONModel.pdf_id == file.id).first()
        if mindmap:
            return mindmap
        
        Mindmap = models.JSONModel(
          pdf_id = file.id
          ,json_content = {
                            "file_name": file.file_name,
                             "nodes": [
                                        {
                                          "node_id": 0,
                                          "parent_id": None,
                                          "topic": "Advanced Techniques in Plant Growth and Photosynthesis Analysis",
                                          "content": "The document provides an overview of advanced techniques in analyzing plant growth and photosynthesis, which are critical for understanding plant biology and ecosystem sustainability. It details how modern botanical research integrates advanced imaging methods, genetic analysis, and environmental monitoring to study plant growth patterns, photosynthesis rates, and the impact of climate change on plant ecosystems. These techniques allow researchers to gain insights into how plants adapt to varying environmental conditions, helping in the development of sustainable agricultural practices. The presentation titled \"Lecture 10 - Advanced Plant Physiology\" serves as an educational resource to explore these concepts in depth."
                                        },
                                        {
                                          "node_id": 1,
                                          "parent_id": 0,
                                          "topic": "The Role of Photosynthesis in Plant Growth and Agricultural Applications",
                                          "content": "Photosynthesis plays a pivotal role in plant growth by converting sunlight into energy, making it one of the most essential processes in botany. By studying photosynthesis, researchers can optimize crop yields and improve agricultural productivity. This branch of plant science integrates knowledge from multiple fields such as molecular biology, genetics, and environmental science to uncover how plants utilize sunlight, carbon dioxide, and water to grow, providing vital insights into global food security."
                                        },
                                        {
                                          "node_id": 2,
                                          "parent_id": 0,
                                          "topic": "The Impact of Climate Change on Plant Growth and Ecosystem Health",
                                          "content": "Climate change is having a profound effect on plant growth and the health of ecosystems around the world. This section explores how rising temperatures, changing precipitation patterns, and increasing levels of carbon dioxide are influencing plant biology. Cognitive computing systems, alongside advanced environmental sensors, are being used to predict how plants will adapt to these changes and to develop strategies to protect biodiversity. These technologies offer a competitive edge in creating sustainable agricultural practices that can mitigate the adverse effects of climate change."
                                        }
                                      ]
                          }
        )
        db.add(Mindmap)
        db.commit()
        db.refresh(Mindmap)
        return Mindmap
        
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

    return {"message": "File not found"}
