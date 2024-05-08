from fastapi import APIRouter, Depends, status, HTTPException
# from ..schemas import login
from .. import schemas, database, models
from ..database import get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session 
from datetime import datetime, timedelta
from jose import jwt, JWTError
from ..schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin") ## where login is the name of the file generating token i.e login.py

## below 3 variables are for JWT token
SECRET_KEY = 'db7dabc6d6fac10f49bd73e6c98d8b877b04fe441047d3c08df9c89cb05ade0c'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

def generate_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    print("to_encode : ", to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# @router.post('/login')
@router.post('/signin')
# def login(request:schemas.login, db:Session=Depends(get_db)):
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == request.username).first()
    #print("Func:: login - user : ", user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found/Invalid User")
    if not pwd_context.verify(request.password , user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Incorrect Password entered. Please try again") 
    ##Generate JWT tokens
    access_token = generate_token(data = {
        'sub': user.username
    })
    #print("Func:: login - access_token : ", access_token)
    return {"access_token": access_token, "token_type": "bearer"}


## get details of the currently logged in user and check whether it has jwt token, will accept token
def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= "Invalid Auth credential",
        headers = {'WWW-Authenticate':"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        print("payload : ", payload)
        username:str = payload.get('sub') #payload['sub']
        if username is None:
            raise  credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception