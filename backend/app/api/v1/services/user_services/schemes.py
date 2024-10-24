from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    
class PdfResponce(BaseModel):
    id :int
    file_path :str
    file_name :str
    