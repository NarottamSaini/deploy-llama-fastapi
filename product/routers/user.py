from fastapi import APIRouter
from fastapi import FastAPI, status, Response, HTTPException ## status : for adding status of api response, Response: For raising exception
from fastapi.params import Depends
from ..import schemas
from ..import models
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from passlib.context import CryptContext

router = APIRouter(tags=['User'],
                   prefix="/user")

## CryptContext for encoding/hashing the password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

@router.post('/', response_model=schemas.DisplayUser)
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_user = models.User(username = request.username, email = request.email, password = hashedpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
