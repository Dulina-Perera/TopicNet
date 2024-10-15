from passlib.context import CryptContext
from . import models
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str)->str:
    return pwd_context.hash(password)

# Authenticate the user
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user