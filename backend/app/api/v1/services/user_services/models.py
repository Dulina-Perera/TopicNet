from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base, engine
from sqlalchemy.dialects.postgresql import JSONB


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship with the File model
    files = relationship("File", back_populates="owner", cascade="all, delete-orphan")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, index=True)
    file_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship with the User model
    owner = relationship("User", back_populates="files")
    mindmaps = relationship("JSONModel", back_populates="file", cascade="all, delete-orphan")

class JSONModel(Base):
    __tablename__ = 'json_files'
    id = Column(Integer, primary_key=True)
    pdf_id = Column(Integer, ForeignKey('files.id'))
    json_content = Column(JSONB)  # Store JSON data in the database
    
    file = relationship("File", back_populates="mindmaps")
    

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)
